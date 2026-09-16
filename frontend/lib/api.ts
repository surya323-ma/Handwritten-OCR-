export interface ExtractedAnswer {
  question_number: number;
  text: string;
  confidence: number;
}

export interface PageResult {
  page_number: number;
  raw_text: string;
  answers: ExtractedAnswer[];
}

export interface ProcessResponse {
  file_id: string;
  filename: string;
  pages: PageResult[];
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  num_pages: number;
  status: string;
}

export async function uploadPdf(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/upload", { method: "POST", body: formData });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function processPdf(fileId: string, filename: string): Promise<ProcessResponse> {
  const res = await fetch(`/api/process/${fileId}?filename=${encodeURIComponent(filename)}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Processing failed: ${res.status}`);
  return res.json();
}
