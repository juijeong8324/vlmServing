import ReactMarkdown from "react-markdown";
import type { SolveResponse } from "../types";

interface ResultPanelProps {
  result: SolveResponse | null;
}

export default function ResultPanel({ result }: ResultPanelProps) {
  return (
    <section className="panel">
      <p className="panel-title">풀이 결과</p>

      {result && (
        <div id="result-meta">
          <span className="latency-badge">{Math.round(result.latency_ms)} ms</span>
          <span className="model-tag">{result.model}</span>
        </div>
      )}

      <div id="result-content" className={result ? "" : "empty"}>
        {result ? (
          <ReactMarkdown>{result.answer}</ReactMarkdown>
        ) : (
          "풀이 결과가 여기에 표시됩니다."
        )}
      </div>
    </section>
  );
}
