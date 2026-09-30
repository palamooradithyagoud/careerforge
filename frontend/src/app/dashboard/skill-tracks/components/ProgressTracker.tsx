"use client";

import React from "react";
import { motion } from "framer-motion";
import { Award, RefreshCw, CheckCircle2 } from "lucide-react";

interface ProgressTrackerProps {
  currentTopicName: string;
  totalLecturesCount: number;
  completedCount: number;
  progressPercent: number;
  loadingTopic: string | null;
  onResync: () => void;
}

export function ProgressTracker({
  currentTopicName,
  totalLecturesCount,
  completedCount,
  progressPercent,
  loadingTopic,
  onResync,
}: ProgressTrackerProps) {
  const isSyncing = loadingTopic === currentTopicName;

  return (
    <div className="p-5 rounded-2xl bg-[#1C0D17]/90 border border-teal-500/30 space-y-4 shadow-inner relative z-10">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-2">
          <Award className="w-5 h-5 text-teal-400" />
          <h3 className="text-sm font-black uppercase tracking-wider text-white">
            Course Progress Tracker
          </h3>
          <button
            type="button"
            onClick={onResync}
            disabled={isSyncing}
            className="ml-2 px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/15 text-slate-300 hover:text-white text-[11px] font-bold flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
            title="Re-sync full playlist from YouTube"
            aria-label="Re-sync playlist from YouTube"
          >
            <RefreshCw className={`w-3 h-3 ${isSyncing ? "animate-spin text-teal-400" : ""}`} />
            <span>{isSyncing ? "Syncing..." : "Re-sync"}</span>
          </button>
        </div>

        <div className="flex items-center gap-4 text-xs">
          <span className="text-slate-300">
            Total Videos: <strong className="text-white font-bold">{totalLecturesCount}</strong>
          </span>
          <span className="text-emerald-400">
            Completed: <strong className="font-bold">{completedCount}</strong>
          </span>
          <span className="text-slate-400">
            Remaining: <strong className="font-bold">{Math.max(0, totalLecturesCount - completedCount)}</strong>
          </span>
        </div>
      </div>

      {/* Visual Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs font-bold text-slate-300">
          <span>Completion Rate</span>
          <span className="text-teal-300">{progressPercent}%</span>
        </div>
        <div
          className="w-full h-3 rounded-full bg-black/60 border border-white/10 overflow-hidden p-0.5"
          role="progressbar"
          aria-valuenow={progressPercent}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Course completion progress: ${progressPercent}%`}
        >
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progressPercent}%` }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="h-full rounded-full bg-gradient-to-r from-teal-500 via-emerald-500 to-cyan-400 shadow-lg"
          />
        </div>
      </div>

      {progressPercent === 100 && totalLecturesCount > 0 && (
        <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>Congratulations! You have completed all lecture videos for this skill!</span>
        </div>
      )}
    </div>
  );
}
