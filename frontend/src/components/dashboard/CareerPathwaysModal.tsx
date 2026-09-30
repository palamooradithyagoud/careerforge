"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Compass,
  Sparkles,
  Briefcase,
  GraduationCap,
  Award,
  Clock,
  ArrowRight,
  ShieldCheck,
  Zap
} from "lucide-react";

interface CareerPathwaysModalProps {
  isOpen: boolean;
  onClose: () => void;
  educationStage?: "class_10" | "intermediate" | "b_tech" | string | null;
  onSelectStreamForScholarships?: (streamName: string) => void;
}

export default function CareerPathwaysModal({
  isOpen,
  onClose,
  educationStage
}: CareerPathwaysModalProps) {
  if (!isOpen) return null;

  const previewHighlights = [
    {
      icon: Sparkles,
      color: "#F59E0B",
      borderColor: "rgba(245, 158, 11, 0.3)",
      bgColor: "rgba(245, 158, 11, 0.08)",
      title: "AI Profile Roadmapping",
      tag: "Personalized",
      description:
        "Adaptive career trajectories that dynamically match your academic performance, verifiable skills, and aspirational goals."
    },
    {
      icon: Briefcase,
      color: "#10B981",
      borderColor: "rgba(16, 185, 129, 0.3)",
      bgColor: "rgba(16, 185, 129, 0.08)",
      title: "Real-Time Labor Telemetry",
      tag: "Market Intel",
      description:
        "Live market demand, emerging technology stacks, and realistic compensation benchmarks directly mapped to your target career."
    },
    {
      icon: GraduationCap,
      color: "#3B82F6",
      borderColor: "rgba(59, 130, 246, 0.3)",
      bgColor: "rgba(59, 130, 246, 0.08)",
      title: "Curated Academic Milestones",
      tag: "Institutional",
      description:
        "Precise prerequisites, entrance examination score matrices, and premier institutional pathways tailored to your state."
    },
    {
      icon: Award,
      color: "#EC4899",
      borderColor: "rgba(236, 72, 153, 0.3)",
      bgColor: "rgba(236, 72, 153, 0.08)",
      title: "Integrated Scholarship Matches",
      tag: "Funding First",
      description:
        "Directly links vetted institutional aid, corporate sponsorships, and merit scholarships with every stage of your roadmap."
    }
  ];

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/80 backdrop-blur-md overflow-y-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.94, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.94, y: 15 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="bg-[#12121A] border border-[#2B2B3C] rounded-3xl w-full max-w-2xl max-h-[92vh] flex flex-col shadow-[0_20px_60px_rgba(0,0,0,0.85)] relative overflow-hidden"
        >
          {/* Symmetrical ambient gradient accent bar */}
          <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-pink-500 via-amber-400 to-indigo-500" />

          {/* Modal Header */}
          <div className="p-4 sm:p-5 border-b border-[#20202C] flex items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-pink-500/15 border border-pink-500/30 flex items-center justify-center text-pink-400 shrink-0">
                <Compass className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <h2 className="text-base sm:text-lg font-bold text-white tracking-tight">
                    Career Pathways
                  </h2>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>Coming Soon</span>
                  </span>
                </div>
                <p className="text-xs text-[#8E8E9C] mt-0.5">
                  AI-Powered Student Career & Education Navigation Engine
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="p-2 text-[#8E8E9C] hover:text-white hover:bg-[#1E1E2C] rounded-full transition-colors cursor-pointer"
              title="Close modal"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Modal Scrollable Body */}
          <div className="p-5 sm:p-6 overflow-y-auto space-y-6 flex-1 custom-scrollbar">
            {/* Symmetrical Hero Announcement Card */}
            <div className="relative rounded-2xl bg-gradient-to-br from-[#161624] via-[#141420] to-[#101018] border border-amber-500/30 p-6 sm:p-8 text-center space-y-4 shadow-xl overflow-hidden ring-1 ring-amber-500/20">
              {/* Subtle background glow */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

              {/* Centered glowing animated icon */}
              <div className="mx-auto w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500/20 to-pink-500/20 border border-amber-500/40 flex items-center justify-center text-amber-300 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
                <Compass className="w-8 h-8 animate-pulse" />
              </div>

              <div className="space-y-2 max-w-lg mx-auto">
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30 shadow-xs">
                  <Zap className="w-3.5 h-3.5" />
                  <span>Phase 2.0 Feature In Development</span>
                </div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                  Next-Gen Career Pathways Engine
                </h3>
                <p className="text-xs sm:text-sm text-[#A6A6BC] leading-relaxed">
                  We are re-engineering the Career Pathways module with dynamic AI labor market intelligence, automated skill graphs, and personalized milestone verification.
                </p>
              </div>

              {/* Status pill */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#101018] border border-[#2B2B3C] text-xs text-[#8E8E9C]">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Core intelligence models and roadmap pipelines currently in training</span>
              </div>
            </div>

            {/* Symmetrical 2x2 Feature Preview Grid */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-[#8E8E9C]">
                  What&apos;s Coming in Phase 2.0
                </span>
                <span className="text-[11px] text-amber-400 font-semibold font-mono">
                  4 Core Modules
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {previewHighlights.map((item, idx) => {
                  const Icon = item.icon;
                  return (
                    <motion.div
                      key={idx}
                      whileHover={{ scale: 1.015 }}
                      transition={{ duration: 0.2 }}
                      className="p-4 rounded-2xl bg-[#161622] border border-[#2B2B3C] hover:border-[#3E3E56] transition-all flex flex-col justify-between gap-3 shadow-sm"
                      style={{
                        borderLeftColor: item.color,
                        borderLeftWidth: "3px"
                      }}
                    >
                      <div className="flex items-start gap-3">
                        <div
                          className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border"
                          style={{
                            backgroundColor: item.bgColor,
                            borderColor: item.borderColor,
                            color: item.color
                          }}
                        >
                          <Icon className="w-5 h-5" />
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <h4 className="font-bold text-sm text-white">
                              {item.title}
                            </h4>
                            <span
                              className="text-[9px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-wider"
                              style={{
                                color: item.color,
                                backgroundColor: item.bgColor,
                                border: `1px solid ${item.borderColor}`
                              }}
                            >
                              {item.tag}
                            </span>
                          </div>
                          <p className="text-xs text-[#8E8E9C] mt-1 leading-relaxed">
                            {item.description}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Symmetrical Modal Footer */}
          <div className="p-4 sm:p-5 border-t border-[#20202C] bg-[#0E0E14] flex items-center justify-between gap-3 flex-wrap">
            <span className="text-xs text-[#6E6E82]">
              Stay tuned for platform updates & roadmap releases.
            </span>
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-extrabold text-xs transition-all shadow-md hover:shadow-amber-500/25 flex items-center gap-1.5 cursor-pointer ml-auto"
            >
              <span>Explore Active Scholarships</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
