"use client";

import React from "react";
import { Volume2, Check, Square } from "lucide-react";
import { YouTubeLecture } from "@/lib/roadmapStorage";

interface LessonCardProps {
  lecture: YouTubeLecture;
  index: number;
  isPlaying: boolean;
  isCompleted: boolean;
  onSelect: () => void;
  onToggleComplete: () => void;
}

export function LessonCard({
  lecture,
  index,
  isPlaying,
  isCompleted,
  onSelect,
  onToggleComplete,
}: LessonCardProps) {
  return (
    <div
      className={`p-3.5 rounded-2xl border transition-all flex items-center justify-between gap-3 select-none ${
        isPlaying
          ? "bg-gradient-to-r from-teal-950/50 to-[#1C0D17] border-teal-500 shadow-md"
          : isCompleted
          ? "bg-emerald-950/20 border-emerald-500/30 hover:bg-emerald-950/30"
          : "bg-black/40 border-white/10 hover:border-white/20 hover:bg-black/60"
      }`}
    >
      {/* Click to play */}
      <button
        type="button"
        onClick={onSelect}
        className="flex items-center gap-3 cursor-pointer flex-1 min-w-0 text-left bg-transparent border-0 p-0"
        aria-label={`Play lecture ${index + 1}: ${lecture.title}`}
      >
        <div
          className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 font-bold text-xs ${
            isPlaying
              ? "bg-teal-500 text-white shadow-md"
              : isCompleted
              ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
              : "bg-white/10 text-slate-300"
          }`}
        >
          {isPlaying ? (
            <Volume2 className="w-4 h-4 animate-bounce" />
          ) : (
            <span>#{index + 1}</span>
          )}
        </div>

        <div className="min-w-0 flex-1">
          <h4
            className={`text-xs sm:text-sm font-bold truncate ${
              isPlaying ? "text-teal-300" : isCompleted ? "text-emerald-200" : "text-white"
            }`}
          >
            {lecture.title}
          </h4>
          <span className="text-[11px] text-slate-400 block truncate">
            {lecture.channel_title || "YouTube Course"}
          </span>
        </div>
      </button>

      {/* Mark completed button */}
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          onToggleComplete();
        }}
        aria-label={isCompleted ? `Mark lecture ${index + 1} as incomplete` : `Mark lecture ${index + 1} as complete`}
        className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
          isCompleted
            ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30"
            : "bg-[#281321] hover:bg-[#351E2D] border border-white/10 text-slate-400 hover:text-white"
        }`}
      >
        {isCompleted ? (
          <>
            <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[3]" />
            <span>Done</span>
          </>
        ) : (
          <>
            <Square className="w-3.5 h-3.5 text-slate-400" />
            <span>Mark Done</span>
          </>
        )}
      </button>
    </div>
  );
}
