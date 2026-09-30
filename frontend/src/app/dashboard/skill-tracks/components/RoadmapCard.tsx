"use client";

import React from "react";
import {
  Building,
  MapPin,
  ExternalLink,
  Trash2,
  ListChecks,
  XCircle,
  AlertTriangle,
  Sparkles,
  GraduationCap,
  Code2,
  Briefcase,
  CheckCircle2,
} from "lucide-react";
import { SavedSkillRoadmap, SavedYouTubePlaylist } from "@/lib/roadmapStorage";

interface RoadmapCardProps {
  item: SavedSkillRoadmap;
  activeSection: "req" | "saved";
  onDelete: (id: string, e: React.MouseEvent) => void;
  onTopicClick: (
    roadmapId: string,
    rawTopic: string,
    existingPlaylist?: SavedYouTubePlaylist
  ) => void;
}

export function RoadmapCard({
  item,
  activeSection,
  onDelete,
  onTopicClick,
}: RoadmapCardProps) {
  return (
    <div className="rounded-3xl bg-[#140A12] border border-[#351E2D] p-6 space-y-6 shadow-xl relative overflow-hidden">
      {/* Ambient Lighting */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-teal-500/5 blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-60 h-60 bg-purple-900/10 blur-3xl pointer-events-none" />

      {/* Card Header: Role info, Apply & Delete */}
      <div className="flex items-start justify-between gap-4 pb-4 border-b border-[#281321] flex-wrap relative z-10">
        <div className="space-y-1">
          <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
            {item.job.title}
          </h2>
          <div className="flex items-center gap-3 text-xs text-slate-300 flex-wrap">
            <span className="flex items-center gap-1.5 text-slate-200 font-bold">
              <Building className="w-4 h-4 text-amber-400" />
              {item.job.company}
            </span>
            {item.job.location && (
              <span className="flex items-center gap-1.5 text-slate-400">
                <MapPin className="w-4 h-4 text-slate-500" />
                {item.job.location}
              </span>
            )}
            {item.job.salary && (
              <span className="px-2.5 py-0.5 rounded-md bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-[11px] font-bold">
                {item.job.salary}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {item.job.applyLink && (
            <a
              href={item.job.applyLink}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Apply for ${item.job.title} at ${item.job.company}`}
              className="px-4 py-2 rounded-xl bg-[#281321] hover:bg-[#351E2D] border border-[#4A2848] text-xs font-bold text-white flex items-center gap-1.5 transition-all shadow-sm"
            >
              <span>Apply on Jooble</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
            </a>
          )}

          <button
            type="button"
            onClick={(e) => onDelete(item.id, e)}
            title="Remove saved job"
            aria-label={`Remove saved role: ${item.job.title}`}
            className="p-2 rounded-xl bg-rose-950/30 hover:bg-rose-950/60 border border-rose-800/30 text-rose-400 hover:text-rose-300 transition-colors cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* SECTION 1: REQ */}
      {activeSection === "req" && (
        <div className="p-5 rounded-2xl bg-[#1C0D17]/90 border border-amber-500/30 space-y-5 shadow-inner relative z-10">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-md bg-amber-600 text-white text-[10px] font-black uppercase tracking-wider">
                SECTION 1
              </span>
              <h3 className="text-sm font-black uppercase tracking-wider text-amber-300 flex items-center gap-1.5">
                <ListChecks className="w-4 h-4 text-amber-400" />
                <span>REQ (Job Requirements &amp; What to Learn)</span>
              </h3>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              Recruiter Requirements Sync
            </span>
          </div>

          {/* All Job Skill Requirements */}
          {item.requirements?.allRequiredSkills && item.requirements.allRequiredSkills.length > 0 && (
            <div className="space-y-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-300 block">
                Full Job Skill Requirements:
              </span>
              <div className="flex flex-wrap gap-2">
                {item.requirements.allRequiredSkills.map((req, rIdx) => (
                  <span
                    key={rIdx}
                    className="px-3 py-1 rounded-xl bg-black/40 border border-white/10 text-slate-300 text-xs font-medium"
                  >
                    • {req}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* WHAT TO LEARN: Missing Requirements */}
          {item.whatToLearn.missingSkills && item.whatToLearn.missingSkills.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400">
                  <XCircle className="w-4 h-4 text-rose-400" />
                  <span>WHAT TO LEARN: Missing Requirements</span>
                </div>
                <span className="text-[10px] text-slate-400">
                  Click any skill to open lectures
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {item.whatToLearn.missingSkills.map((mSkill, mIdx) => {
                  const cleanName = mSkill.replace(/^[×⚠✓\s]+/, "").replace(/\s*\([^)]*\)/g, "").trim();
                  return (
                    <button
                      key={mIdx}
                      type="button"
                      onClick={() => onTopicClick(item.id, mSkill, item.yt_playlists?.[cleanName])}
                      aria-label={`Open lectures for missing skill: ${mSkill}`}
                      className="px-3 py-1.5 rounded-xl border text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all cursor-pointer bg-rose-950/50 hover:bg-rose-900/60 border-rose-500/40 text-rose-300 hover:scale-105"
                    >
                      <span className="text-rose-400 font-black">×</span>
                      <span>{mSkill}</span>
                      <GraduationCap className="w-3 h-3 text-teal-400 ml-0.5" />
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Needs Development */}
          {item.whatToLearn.needsDevelopment && item.whatToLearn.needsDevelopment.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span>Proficiency Gaps (Needs Development)</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {item.whatToLearn.needsDevelopment.map((pSkill, pIdx) => {
                  const cleanName = pSkill.replace(/^[×⚠✓\s]+/, "").replace(/\s*\([^)]*\)/g, "").trim();
                  return (
                    <button
                      key={pIdx}
                      type="button"
                      onClick={() => onTopicClick(item.id, cleanName, item.yt_playlists?.[cleanName])}
                      aria-label={`Open lectures for proficiency gap: ${pSkill}`}
                      className="px-3 py-1.5 rounded-xl bg-amber-950/50 hover:bg-amber-900/60 border border-amber-500/40 text-amber-300 text-xs font-bold flex items-center gap-1.5 shadow-sm cursor-pointer transition-all hover:scale-105"
                    >
                      <span className="text-amber-400 font-black">⚠</span>
                      <span>{pSkill}</span>
                      <GraduationCap className="w-3 h-3 text-teal-400 ml-0.5" />
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEPWISE LEARNING ROADMAP (CLICK TO REDIRECT TO LECTURES) */}
          {item.whatToLearn.learningSteps && item.whatToLearn.learningSteps.length > 0 && (
            <div className="space-y-3 pt-2 border-t border-[#281321]">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <span className="text-xs font-bold uppercase text-cyan-300 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-cyan-400" />
                  <span>Step-by-Step Learning Roadmap (Click to Open Lectures):</span>
                </span>
                <span className="text-[11px] text-teal-300 font-semibold flex items-center gap-1">
                  <GraduationCap className="w-3.5 h-3.5" />
                  <span>Opens Learning Lectures &amp; Tracker</span>
                </span>
              </div>

              <div className="space-y-2.5">
                {item.whatToLearn.learningSteps.map((step, stIdx) => {
                  const pData = item.yt_playlists?.[step.skill];
                  const comp = pData?.completed_videos?.length || 0;
                  const tot = pData?.total_videos || pData?.lectures?.length || 0;

                  return (
                    <div
                      key={stIdx}
                      onClick={() => onTopicClick(item.id, step.skill, item.yt_playlists?.[step.skill])}
                      role="button"
                      tabIndex={0}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ") {
                          onTopicClick(item.id, step.skill, item.yt_playlists?.[step.skill]);
                        }
                      }}
                      aria-label={`Open lectures for step ${step.sequence || stIdx + 1}: ${step.skill}`}
                      className="p-4 rounded-2xl border border-white/10 hover:border-teal-400 bg-black/40 hover:bg-black/70 transition-all cursor-pointer select-none group shadow-sm hover:scale-[1.01]"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-start gap-3">
                          <div className="w-7 h-7 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-black text-xs flex items-center justify-center shrink-0 mt-0.5">
                            {step.sequence || stIdx + 1}
                          </div>

                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="font-extrabold text-sm text-white group-hover:text-teal-300 transition-colors">
                                {step.skill}
                              </span>
                              {tot > 0 && (
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                                  {comp}/{tot} Completed
                                </span>
                              )}
                            </div>
                            {step.focus && step.focus.length > 0 && (
                              <p className="text-xs text-slate-300 leading-relaxed">
                                <strong className="text-cyan-400 font-semibold">Focus:</strong>{" "}
                                {step.focus.join(", ")}
                              </p>
                            )}
                          </div>
                        </div>

                        <div className="shrink-0 flex items-center gap-1.5">
                          <span className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-teal-500/15 text-teal-300 border border-teal-500/40 group-hover:bg-gradient-to-r group-hover:from-teal-500 group-hover:to-emerald-600 group-hover:text-white transition-all flex items-center gap-1.5 shadow-sm">
                            <GraduationCap className="w-3.5 h-3.5" />
                            <span>Open Lectures →</span>
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Recommended Bridge Project */}
          {item.whatToLearn.projectRecommendation && (
            <div className="p-3.5 rounded-xl bg-purple-950/25 border border-purple-500/30 text-xs text-slate-200 space-y-1.5">
              <span className="text-xs font-bold uppercase text-purple-300 flex items-center gap-1.5">
                <Code2 className="w-4 h-4 text-purple-400" />
                <span>Recommended Portfolio Project to Bridge Requirements:</span>
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {item.whatToLearn.projectRecommendation}
              </p>
            </div>
          )}
        </div>
      )}

      {/* SECTION 2: SAVED */}
      {activeSection === "saved" && (
        <div className="p-5 rounded-2xl bg-[#20101D]/90 border border-purple-500/30 space-y-4 shadow-inner relative z-10">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-md bg-purple-600 text-white text-[10px] font-black uppercase tracking-wider">
                SECTION 2
              </span>
              <h3 className="text-sm font-black uppercase tracking-wider text-purple-300 flex items-center gap-1.5">
                <Briefcase className="w-4 h-4 text-purple-400" />
                <span>SAVED (Saved Job &amp; My Skills)</span>
              </h3>
            </div>
            <span className="text-xs text-slate-400">
              Saved Role Overview
            </span>
          </div>

          {/* Summary Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs bg-black/40 p-3.5 rounded-xl border border-white/5">
            <div>
              <span className="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Job Role</span>
              <span className="font-semibold text-white text-xs">{item.job.title}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Hiring Company</span>
              <span className="font-semibold text-white text-xs">{item.job.company}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block font-bold uppercase tracking-wider">Work Location</span>
              <span className="font-semibold text-white text-xs">{item.job.location || "India"}</span>
            </div>
          </div>

          {/* WHAT SKILLS I HAVE */}
          <div className="space-y-2 pt-1">
            <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>WHAT SKILLS I HAVE (Verified Strengths)</span>
            </div>

            {item.skillsIHave && item.skillsIHave.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {item.skillsIHave.map((skill, sIdx) => (
                  <span
                    key={sIdx}
                    className="px-3 py-1.5 rounded-xl bg-emerald-950/50 border border-emerald-500/40 text-emerald-300 text-xs font-bold flex items-center gap-1.5 shadow-sm"
                  >
                    <span className="text-emerald-400 font-black">✓</span>
                    <span>{skill}</span>
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic">No verified skills recorded.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
