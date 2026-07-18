import { useState } from "react";
import UploadView from "./components/UploadView";
import ScanView from "./components/ScanView";
import ResultView from "./components/ResultView";
import { TILE_ATTRIBUTION } from "./lib/config";
import type { MatchResult } from "./lib/matcher";

type Phase =
  | { name: "upload" }
  | { name: "scan"; image: ImageBitmap; imageUrl: string }
  | { name: "result"; image: ImageBitmap; imageUrl: string; matches: MatchResult[] };

export default function App() {
  const [phase, setPhase] = useState<Phase>({ name: "upload" });

  return (
    <div className="app">
      <header className="app-header">
        <button
          className="app-title-btn"
          onClick={() => setPhase({ name: "upload" })}
          aria-label="最初に戻る"
        >
          <span className="survey-label">FACE ⇄ EARTH SURVEY</span>
          <span className="app-title">FaceEarth</span>
        </button>
      </header>

      <main className="app-main">
        {phase.name === "upload" && (
          <UploadView
            onSelect={(image, imageUrl) => setPhase({ name: "scan", image, imageUrl })}
          />
        )}
        {phase.name === "scan" && (
          <ScanView
            image={phase.image}
            onDone={(matches) =>
              setPhase({ name: "result", image: phase.image, imageUrl: phase.imageUrl, matches })
            }
            onError={() => setPhase({ name: "upload" })}
          />
        )}
        {phase.name === "result" && (
          <ResultView
            image={phase.image}
            imageUrl={phase.imageUrl}
            matches={phase.matches}
            onRestart={() => setPhase({ name: "upload" })}
          />
        )}
      </main>

      <footer className="app-footer">
        <span dangerouslySetInnerHTML={{ __html: TILE_ATTRIBUTION }} />
        <span className="app-footer-note">解析はすべてこの端末の中で行われます。</span>
      </footer>
    </div>
  );
}
