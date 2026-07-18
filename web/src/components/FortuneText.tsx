import { useEffect, useRef, useState } from "react";

/** 占いテキストをタイプライター風に表示する */
export default function FortuneText({ text }: { text: string }) {
  const [shown, setShown] = useState(0);
  const doneRef = useRef(false);

  useEffect(() => {
    setShown(0);
    doneRef.current = false;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setShown(text.length);
      return;
    }
    let i = 0;
    const timer = window.setInterval(() => {
      i += 2;
      setShown(i);
      if (i >= text.length) window.clearInterval(timer);
    }, 40);
    return () => window.clearInterval(timer);
  }, [text]);

  return (
    <div className="fortune">
      <p className="survey-label">READING — この土地との縁</p>
      <p className="fortune-text" aria-label={text}>
        {text.slice(0, shown)}
        {shown < text.length && <span className="fortune-cursor">▏</span>}
      </p>
    </div>
  );
}
