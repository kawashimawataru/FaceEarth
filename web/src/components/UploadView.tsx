import { useCallback, useEffect, useRef, useState } from "react";
import { clipEngine } from "../lib/clip";
import { loadCorpus } from "../lib/matcher";

interface Props {
  onSelect: (image: ImageBitmap, imageUrl: string) => void;
}

export default function UploadView({ onSelect }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // アップロード画面を眺めている間にモデルとコーパスを先読みしておく
  useEffect(() => {
    clipEngine.load().catch(() => {});
    loadCorpus().catch(() => {});
  }, []);

  const handleFile = useCallback(
    async (file: File | undefined) => {
      if (!file) return;
      if (!file.type.startsWith("image/")) {
        setError("画像ファイルを選んでください。");
        return;
      }
      try {
        const image = await createImageBitmap(file);
        onSelect(image, URL.createObjectURL(file));
      } catch {
        setError("この画像は読み込めませんでした。別の写真で試してください。");
      }
    },
    [onSelect],
  );

  return (
    <section className="upload">
      <div className="upload-hero">
        <p className="survey-label">OBSERVATION 01 — 見立て</p>
        <h2 className="upload-headline">
          あなたの顔は、
          <br />
          地球のどこかに似ている。
        </h2>
        <p className="upload-lede">
          顔写真を 1 枚。AI が地球全体の衛星画像と照合し、
          あなたと響き合う土地を見つけます。
          「似ている」と言われた場所のことは、なぜか知りたくなるものです。
        </p>
      </div>

      <div
        className={`upload-drop${dragging ? " is-dragging" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFile(e.dataTransfer.files[0]);
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          hidden
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
        <button className="upload-button" onClick={() => inputRef.current?.click()}>
          顔写真を選ぶ
        </button>
        <p className="upload-hint">またはここにドロップ</p>
        {error && <p className="upload-error">{error}</p>}
      </div>

      <p className="upload-privacy">
        写真はこの端末の中だけで解析され、どこにも送信されません。
        初回のみ AI モデル(約 90MB)をダウンロードします。
      </p>
    </section>
  );
}
