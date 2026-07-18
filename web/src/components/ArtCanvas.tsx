import { useEffect, useRef, useState } from "react";
import {
  buildLandField,
  findSimilarLandPoint,
  seededRandom,
  type Pt,
} from "../lib/correspondence";
import { detectFace, FACE_OVAL_INDICES } from "../lib/landmarks";
import type { MatchResult } from "../lib/matcher";
import { tileUrl } from "../lib/tiles";

interface Props {
  image: ImageBitmap;
  match: MatchResult;
}

const SIZE = 360; // 顔・タイル各パネルの一辺
const GAP = 24;
const N_POINTS = 22;

/** 対応線の色: テーマのアンバー〜氷〜砂のグラデーション */
const PALETTE = ["#e0a458", "#dce3e8", "#c89b6d", "#f0c987", "#a8b8c8"];

/**
 * 顔ランドマークと衛星タイルの「似ている点」を線で結ぶアートワーク。
 * 点の対応は座標の近さ + 色の近さ + 地形勾配 (海岸線・尾根) で決まり、
 * 乱数はタイル ID シードなので同じ顔×同じ場所なら同じ絵になる。
 */
export default function ArtCanvas({ image, match }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [status, setStatus] = useState<"loading" | "no-face" | "error" | "done">("loading");

  useEffect(() => {
    let cancelled = false;
    let raf = 0;

    (async () => {
      const canvas = canvasRef.current!;
      const W = SIZE * 2 + GAP;
      canvas.width = W;
      canvas.height = SIZE;
      const ctx = canvas.getContext("2d")!;
      ctx.fillStyle = "#0d1119";
      ctx.fillRect(0, 0, W, SIZE);

      // 1) 顔を正方形 (cover) で左パネルへ
      const faceCanvas = new OffscreenCanvas(SIZE, SIZE);
      const fctx = faceCanvas.getContext("2d")!;
      const scale = Math.max(SIZE / image.width, SIZE / image.height);
      fctx.drawImage(
        image,
        (SIZE - image.width * scale) / 2,
        (SIZE - image.height * scale) / 2,
        image.width * scale,
        image.height * scale,
      );
      const faceData = fctx.getImageData(0, 0, SIZE, SIZE);

      // 2) 顔ランドマーク検出 (正方形化した画像に対して)
      const squareBitmap = await createImageBitmap(faceCanvas);
      const face = await detectFace(squareBitmap);
      if (cancelled) return;
      if (!face) {
        setStatus("no-face");
        return;
      }

      // 3) タイル画像を右パネルへ (CORS 付きで読み、画素を取る)
      const tile = new Image();
      tile.crossOrigin = "anonymous";
      tile.src = tileUrl(match.meta.z, match.meta.x, match.meta.y);
      try {
        await tile.decode();
      } catch {
        setStatus("error");
        return;
      }
      if (cancelled) return;
      const landCanvas = new OffscreenCanvas(SIZE, SIZE);
      const lctx = landCanvas.getContext("2d")!;
      lctx.drawImage(tile, 0, 0, SIZE, SIZE);
      const land = buildLandField(lctx.getImageData(0, 0, SIZE, SIZE));

      ctx.drawImage(faceCanvas, 0, 0);
      ctx.drawImage(landCanvas, SIZE + GAP, 0);

      // 4) ランドマークをシード付きでサンプリングし、対応点を探す
      const rng = seededRandom(match.meta.i * 104729 + 7);
      const indices = new Set<number>();
      while (indices.size < N_POINTS) {
        indices.add(Math.floor(rng() * face.points.length));
      }
      const colorAt = (p: Pt): [number, number, number] => {
        const x = Math.min(SIZE - 1, Math.max(0, Math.round(p.x)));
        const y = Math.min(SIZE - 1, Math.max(0, Math.round(p.y)));
        const i = (y * SIZE + x) * 4;
        return [faceData.data[i], faceData.data[i + 1], faceData.data[i + 2]];
      };
      const pairs = [...indices].map((idx) => {
        const fp = face.points[idx];
        const lp = findSimilarLandPoint(fp.x, fp.y, colorAt(fp), land);
        return { fp, lp, color: PALETTE[Math.floor(rng() * PALETTE.length)] };
      });

      // 5) 顔輪郭 (face oval) → 土地側の対応輪郭
      const oval = FACE_OVAL_INDICES.map((i) => face.points[i]);
      const ovalLand = oval.map((p) => findSimilarLandPoint(p.x, p.y, colorAt(p), land));

      // 6) rAF で線を描き込む
      const started = performance.now();
      const DURATION = 2600;
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      const drawFrame = (now: number) => {
        const t = reduceMotion ? 1 : Math.min(1, (now - started) / DURATION);
        ctx.drawImage(faceCanvas, 0, 0);
        ctx.drawImage(landCanvas, SIZE + GAP, 0);

        // 対応線 (t に応じて 1 本ずつ伸びる)
        pairs.forEach(({ fp, lp, color }, k) => {
          const lineT = Math.min(1, Math.max(0, t * pairs.length - k));
          if (lineT <= 0) return;
          const x2 = SIZE + GAP + lp.x;
          const mx = fp.x + (x2 - fp.x) * lineT;
          const my = fp.y + (lp.y - fp.y) * lineT;
          ctx.strokeStyle = color;
          ctx.globalAlpha = 0.65;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(fp.x, fp.y);
          ctx.lineTo(mx, my);
          ctx.stroke();
          ctx.globalAlpha = 1;
          ctx.fillStyle = color;
          ctx.beginPath();
          ctx.arc(fp.x, fp.y, 2.2, 0, Math.PI * 2);
          ctx.fill();
          if (lineT >= 1) {
            ctx.beginPath();
            ctx.arc(x2, lp.y, 2.2, 0, Math.PI * 2);
            ctx.fill();
          }
        });

        // 輪郭線 (両側)
        if (t > 0.4) {
          const ovalT = Math.min(1, (t - 0.4) / 0.6);
          const nPts = Math.max(2, Math.floor(oval.length * ovalT));
          ctx.strokeStyle = "#e0a458";
          ctx.lineWidth = 1.6;
          ctx.globalAlpha = 0.9;
          ctx.beginPath();
          oval.slice(0, nPts).forEach((p, i) => (i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y)));
          ctx.stroke();
          ctx.beginPath();
          ovalLand
            .slice(0, nPts)
            .forEach((p, i) =>
              i ? ctx.lineTo(SIZE + GAP + p.x, p.y) : ctx.moveTo(SIZE + GAP + p.x, p.y),
            );
          ctx.stroke();
          ctx.globalAlpha = 1;
        }

        if (t < 1 && !cancelled) {
          raf = requestAnimationFrame(drawFrame);
        } else {
          setStatus("done");
        }
      };
      raf = requestAnimationFrame(drawFrame);
    })().catch(() => setStatus("error"));

    return () => {
      cancelled = true;
      cancelAnimationFrame(raf);
    };
  }, [image, match]);

  const save = () => {
    canvasRef.current?.toBlob((blob) => {
      if (!blob) return;
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `faceearth_${match.meta.z}-${match.meta.x}-${match.meta.y}.png`;
      a.click();
      URL.revokeObjectURL(a.href);
    });
  };

  return (
    <div className="art">
      <p className="survey-label">CORRESPONDENCE — 顔と大地の対応</p>
      {status === "no-face" ? (
        <p className="art-message">
          この写真からは顔を検出できませんでした。正面を向いた顔写真だと対応図が描けます。
        </p>
      ) : status === "error" ? (
        <p className="art-message">対応図の描画に失敗しました。</p>
      ) : (
        <>
          <canvas ref={canvasRef} className="art-canvas" />
          {status === "done" && (
            <button className="art-save" onClick={save}>
              この観測図を保存する
            </button>
          )}
        </>
      )}
    </div>
  );
}
