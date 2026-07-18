import type { MatchResult } from "../lib/matcher";
import { formatDMS, tileUrl } from "../lib/tiles";

interface Props {
  image: ImageBitmap;
  imageUrl: string;
  matches: MatchResult[];
  onRestart: () => void;
}

export default function ResultView({ imageUrl, matches, onRestart }: Props) {
  const best = matches[0];
  if (!best) return null;

  return (
    <section className="result">
      <div className="result-head">
        <p className="survey-label">SURVEY RESULT — 照合結果</p>
        <h2 className="result-headline">
          あなたに似た土地は、
          <br />
          {placeName(best)} でした。
        </h2>
      </div>

      <div className="result-pair">
        <figure className="result-face">
          <img src={imageUrl} alt="あなたの顔写真" />
          <figcaption className="mono">YOU</figcaption>
        </figure>
        <span className="result-pair-link mono">⇄</span>
        <figure className="result-tile">
          <img
            src={tileUrl(best.meta.z, best.meta.x, best.meta.y)}
            alt={`${placeName(best)} の衛星画像`}
          />
          <figcaption className="mono">{formatDMS(best.meta.lat, best.meta.lng)}</figcaption>
        </figure>
      </div>

      <ol className="result-list">
        {matches.map((m) => (
          <li key={m.meta.i} className="result-card">
            <img
              src={tileUrl(m.meta.z, m.meta.x, m.meta.y)}
              alt={`${placeName(m)} の衛星画像`}
              loading="lazy"
            />
            <div className="result-card-body">
              <span className="survey-label">NO.{String(m.rank).padStart(2, "0")}</span>
              <h3>{placeName(m)}</h3>
              <p className="mono result-card-coords">{formatDMS(m.meta.lat, m.meta.lng)}</p>
              <p className="mono result-card-score">
                共鳴度 {m.resonance.toFixed(1)}
                <span className="result-card-score-note">*</span>
              </p>
            </div>
          </li>
        ))}
      </ol>
      <p className="result-footnote">* 共鳴度は今回の照合内での相対値です。</p>

      <button className="upload-button" onClick={onRestart}>
        別の写真で観測する
      </button>
    </section>
  );
}

export function placeName(m: MatchResult): string {
  const { country, region } = m.meta;
  if (country && region) return `${country}・${region}`;
  if (country) return country;
  return "名もなき海域";
}
