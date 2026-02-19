import { useState, useRef, useCallback } from "react";

interface UploadPanelProps {
  onSolve: (file: File, question?: string) => void;
  loading: boolean;
  error: string | null;
}

export default function UploadPanel({ onSolve, loading, error }: UploadPanelProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [hasFile, setHasFile] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [question, setQuestion] = useState("");
  const fileRef = useRef<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((file: File) => {
    fileRef.current = file;
    setHasFile(true);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(file);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith("image/")) handleFile(file);
    },
    [handleFile],
  );

  const handleSubmit = () => {
    if (!fileRef.current) return;
    onSolve(fileRef.current, question.trim() || undefined);
  };

  return (
    <section className="panel">
      <p className="panel-title">입력</p>

      <div
        id="upload-area"
        className={dragOver ? "drag-over" : ""}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        {preview ? (
          <img src={preview} alt="미리보기" id="preview-img" style={{ display: "block" }} />
        ) : (
          <>
            <span className="upload-icon">📷</span>
            <p className="upload-hint">이미지를 드래그하거나 클릭해서 업로드</p>
            <p className="upload-sub">PNG, JPG, WEBP 지원</p>
          </>
        )}
        <input
          type="file"
          ref={inputRef}
          id="file-input"
          accept="image/*"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
          }}
        />
      </div>

      <label htmlFor="question" style={{ fontSize: "0.875rem", fontWeight: 600, color: "var(--muted)" }}>
        추가 질문 (선택)
      </label>
      <textarea
        id="question"
        placeholder="예: 이 방정식을 x에 대해 풀어줘"
        rows={3}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      {error && <p className="error-msg">{error}</p>}

      <button id="solve-btn" disabled={loading || !hasFile} onClick={handleSubmit}>
        {loading && <div className="spinner" style={{ display: "block" }} />}
        <span>{loading ? "풀이 중..." : "문제 풀기"}</span>
      </button>
    </section>
  );
}
