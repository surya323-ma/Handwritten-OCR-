"use client";

import { FileCheck2 } from "lucide-react";
import type { ExtractedAnswer } from "@/lib/api";

export default function AnswerCard({ answer, index }: { answer: ExtractedAnswer; index: number }) {
  const pct = Math.round(answer.confidence * 100);
  const barColor = pct >= 90 ? "bg-emerald-500" : pct >= 70 ? "bg-yellow-500" : "bg-red-500";

  return (
    <div className="bg-panelLight border border-border rounded-lg p-4 mb-3">
      <div className="flex items-center gap-2 mb-2">
        <FileCheck2 size={16} className="text-accent" />
        <span className="text-sm font-medium text-slate-200">Q# {String(answer.question_number).padStart(2, "0")}</span>
        <span className="ml-auto text-[11px] text-slate-500">#{index + 1}</span>
      </div>
      <p className="text-sm text-slate-300 leading-relaxed mb-3">{answer.text}</p>
      <div className="flex items-center gap-2">
        <span className="text-[11px] text-slate-500 w-16 shrink-0">Confidence</span>
        <div className="flex-1 h-1.5 rounded-full bg-slate-700 overflow-hidden">
          <div className={`h-full ${barColor}`} style={{ width: `${pct}%` }} />
        </div>
        <span className="text-[11px] text-slate-400 w-9 text-right">{pct}%</span>
      </div>
    </div>
  );
}
