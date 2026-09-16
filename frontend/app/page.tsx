"use client";

import { useState } from "react";
import Sidebar, { FileItem } from "@/components/Sidebar";
import PdfViewer from "@/components/PdfViewer";
import AnswerCard from "@/components/AnswerCard";
import { uploadPdf, processPdf, ProcessResponse } from "@/lib/api";
import { Loader2 } from "lucide-react";

export default function Home() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [pdfUrls, setPdfUrls] = useState<Record<string, string>>({});
  const [results, setResults] = useState<Record<string, ProcessResponse>>({});
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload(file: File) {
    setUploading(true);
    setError(null);
    try {
      const uploadRes = await uploadPdf(file);
      const localUrl = URL.createObjectURL(file);

      setFiles((prev) => [
        { file_id: uploadRes.file_id, filename: uploadRes.filename, uploadedAt: new Date().toLocaleDateString() },
        ...prev,
      ]);
      setPdfUrls((prev) => ({ ...prev, [uploadRes.file_id]: localUrl }));
      setActiveId(uploadRes.file_id);

      setProcessing(true);
      const processRes = await processPdf(uploadRes.file_id, uploadRes.filename);
      setResults((prev) => ({ ...prev, [uploadRes.file_id]: processRes }));
    } catch (e: any) {
      setError(e.message || "Something went wrong");
    } finally {
      setUploading(false);
      setProcessing(false);
    }
  }

  const activeFile = files.find((f) => f.file_id === activeId) || null;
  const activeResult = activeId ? results[activeId] : null;
  const allAnswers = activeResult?.pages.flatMap((p) => p.answers) ?? [];

  return (
    <div className="flex h-full">
      <Sidebar
        files={files}
        activeId={activeId}
        onSelect={setActiveId}
        onUpload={handleUpload}
        uploading={uploading}
      />

      <PdfViewer fileUrl={activeId ? pdfUrls[activeId] ?? null : null} filename={activeFile?.filename ?? null} />

      <aside className="w-96 shrink-0 border-l border-border bg-panel h-full overflow-y-auto p-4">
        <h2 className="text-sm font-semibold text-slate-300 mb-3">Extracted Answers</h2>

        {error && <p className="text-xs text-red-400 mb-3">{error}</p>}

        {processing && (
          <div className="flex items-center gap-2 text-sm text-slate-400 py-6 justify-center">
            <Loader2 size={16} className="animate-spin" />
            Running OCR pipeline...
          </div>
        )}

        {!processing && allAnswers.length === 0 && !error && (
          <p className="text-xs text-slate-500">Extracted questions and answers will appear here after processing.</p>
        )}

        {allAnswers.map((a, i) => (
          <AnswerCard key={`${a.question_number}-${i}`} answer={a} index={i} />
        ))}
      </aside>
    </div>
  );
}
