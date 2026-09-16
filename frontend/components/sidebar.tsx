"use client";

import { FileText, Upload } from "lucide-react";
import { useRef } from "react";

export interface FileItem {
  file_id: string;
  filename: string;
  uploadedAt: string;
}

interface SidebarProps {
  files: FileItem[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onUpload: (file: File) => void;
  uploading: boolean;
}

export default function Sidebar({ files, activeId, onSelect, onUpload, uploading }: SidebarProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <aside className="w-64 shrink-0 bg-panel border-r border-border h-full flex flex-col">
      <div className="p-3 border-b border-border">
        <button
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="w-full flex items-center justify-center gap-2 rounded-md bg-accent/10 hover:bg-accent/20 text-accent text-sm font-medium py-2 transition-colors disabled:opacity-50"
        >
          <Upload size={16} />
          {uploading ? "Uploading..." : "Upload PDF"}
        </button>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) onUpload(f);
            e.target.value = "";
          }}
        />
      </div>

      <div className="flex-1 overflow-y-auto">
        {files.length === 0 && (
          <p className="text-xs text-slate-500 p-4 text-center">No files yet — upload a scanned answer sheet PDF.</p>
        )}
        {files.map((f) => (
          <button
            key={f.file_id}
            onClick={() => onSelect(f.file_id)}
            className={`w-full text-left px-4 py-3 border-b border-border/60 hover:bg-panelLight transition-colors flex items-start gap-2 ${
              activeId === f.file_id ? "bg-panelLight border-l-2 border-l-accent" : ""
            }`}
          >
            <FileText size={16} className="text-accent mt-0.5 shrink-0" />
            <div className="min-w-0">
              <p className="text-sm text-slate-200 truncate">{f.filename}</p>
              <p className="text-[11px] text-slate-500">{f.uploadedAt}</p>
            </div>
          </button>
        ))}
      </div>
    </aside>
  );
}
