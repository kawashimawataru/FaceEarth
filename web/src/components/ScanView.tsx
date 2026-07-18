import { useEffect, useRef, useState } from "react";
import { clipEngine } from "../lib/clip";
import { loadCorpus, match, type MatchResult } from "../lib/matcher";

interface Props {
  image: ImageBitmap;
  onDone: (matches: MatchResult[]) => void;
  onError: () => void;
}

export default function ScanView({ image, onDone, onError }: Props) {
  const [status, setStatus] = useState("観測機を準備しています…");
  const [percent, setPercent] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return; // StrictMode の二重実行を防ぐ
    started.current = true;

    const offProgress = clipEngine.onProgress((p) => {
      if (p.file.endsWith(".onnx")) {
        setStatus("AI モデルをダウンロード中(初回のみ)");
        setPercent(p.percent);
      }
    });

    (async () => {
      const [corpus] = await Promise.all([loadCorpus(), clipEngine.load()]);
      setPercent(null);
      setStatus("あなたの顔を読み取っています…");
      const vector = await clipEngine.embed(image);
      setStatus("地球と照合しています…");
      const matches = match(vector, corpus);
      // 演出: 照合の瞬間が一瞬で終わると呆気ないため、少しだけ間を置く
      await new Promise((r) => setTimeout(r, 1200));
      onDone(matches);
    })().catch((e) => {
      setError(e instanceof Error ? e.message : String(e));
    });

    return offProgress;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <section className="scan">
      <p className="survey-label">SCANNING</p>
      <div className="scan-stage">
        <ScanPortrait image={image} />
      </div>
      <p className="scan-status" aria-live="polite">
        {status}
      </p>
      {percent != null && (
        <div
          className="scan-progress"
          role="progressbar"
          aria-valuenow={Math.round(percent)}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div className="scan-progress-bar" style={{ width: `${percent}%` }} />
        </div>
      )}
      {error && (
        <div className="scan-error">
          <p>解析に失敗しました: {error}</p>
          <button className="upload-button" onClick={onError}>
            最初からやり直す
          </button>
        </div>
      )}
    </section>
  );
}

/** アップロードされた顔をキャンバスに描き、走査線を重ねる */
function ScanPortrait({ image }: { image: ImageBitmap }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const size = 320;
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext("2d")!;
    // cover で中央に描画
    const scale = Math.max(size / image.width, size / image.height);
    const w = image.width * scale;
    const h = image.height * scale;
    ctx.drawImage(image, (size - w) / 2, (size - h) / 2, w, h);
  }, [image]);

  return (
    <div className="scan-portrait">
      <canvas ref={canvasRef} />
      <div className="scan-line" />
    </div>
  );
}
