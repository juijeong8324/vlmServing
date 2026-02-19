import type { SolveResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

export async function solveImage(
  image: File,
  question?: string,
): Promise<SolveResponse> {
  const formData = new FormData();
  formData.append("image", image);
  if (question) {
    formData.append("question", question);
  }

  const res = await fetch(`${API_BASE}/api/v1/solve`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({
      detail: "서버 오류가 발생했습니다.",
    }));
    throw new Error(err.detail || "서버 오류");
  }

  return res.json();
}
