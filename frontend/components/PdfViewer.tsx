"use client";

interface PdfViewerProps {
  fileUrl: string | null;
  filename: string | null;
}

export default function PdfViewer({ fileUrl, filename }: PdfViewerProps) {
  if (!fileUrl) {
    return (
      <div className="flex-1 flex items-center justify-center text-slate-500 text-sm bg-[#0b0f1a]">
        Select or upload a PDF to preview it here.
      </div>
    );
  }

  return (
    <div className="flex-1 bg-[#0b0f1a] flex flex-col">
      <div className="px-4 py-2 border-b border-border text-xs text-slate-400 truncate">{filename}</div>
      <iframe src={fileUrl} title="PDF preview" className="flex-1 w-full" />
    </div>
  );
}
