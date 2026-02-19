import { useState, useCallback } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultPanel from "./components/ResultPanel";
import { solveImage } from "./api/solve";
import type { SolveResponse } from "./types";
import "./App.css";

export default function App() {
  const [result, setResult] = useState<SolveResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSolve = useCallback(async (file: File, question?: string) => {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const data = await solveImage(file, question);
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <>
      <header>
        <span style={{ fontSize: "1.4rem" }}>🧠</span>
        <h1>VLM 문제 풀이</h1>
        <span className="model-badge">Qwen2.5-VL-3B</span>
      </header>
      <main>
        <UploadPanel onSolve={handleSolve} loading={loading} error={error} />
        <ResultPanel result={result} />
      </main>
    </>
  );
}
