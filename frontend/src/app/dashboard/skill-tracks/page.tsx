"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, useReducedMotion } from "framer-motion";
import { PageLoader } from "@/components/common/BoxLoader";
import {
  ArrowLeft,
  Briefcase,
  ExternalLink,
  ArrowRight,
  ListChecks,
  RefreshCw,
  Loader2,
  X,
  Tv,
  GraduationCap,
  FolderOpen,
} from "lucide-react";

import { useCourseProgress } from "./hooks/useCourseProgress";
import { ProgressTracker } from "./components/ProgressTracker";
import { LessonCard } from "./components/LessonCard";
import { VideoPlayerModal } from "./components/VideoPlayerModal";
import { RoadmapList } from "./components/RoadmapList";

function SkillTracksPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const studentId = searchParams.get("student_id");
  const shouldReduceMotion = useReducedMotion();

  const [activeSection, setActiveSection] = useState<"req" | "saved" | "lectures">("req");

  const {
    roadmaps,
    isLoaded,
    selectedRoadmapId,
    selectedTopic,
    activeLectureVideoId,
    setActiveLectureVideoId,
    loadingTopic,
    setLoadingTopic,
    videoNotice,
    setVideoNotice,
    loadRoadmaps,
    handleDelete,
    fetchYouTubeData,
    handleTopicClickAndRedirect,
    handleToggleLecture,
    currentRoadmap,
    currentTopicName,
    currentPlaylistData,
    currentLectures,
    totalLecturesCount,
    completedLecturesList,
    completedCount,
    progressPercent,
    currentPlayingLecture,
  } = useCourseProgress(studentId);

  // Auto-heal / fetch playlist lectures if active section is lectures and topic has <= 1 video cached
  useEffect(() => {
    if (activeSection === "lectures" && currentRoadmap && currentTopicName) {
      const pData = currentRoadmap.yt_playlists?.[currentTopicName];
      if (!pData || !pData.lectures || pData.lectures.length <= 1) {
        setLoadingTopic(currentTopicName);
        fetchYouTubeData(currentRoadmap.id, currentTopicName).then((fetched) => {
          setLoadingTopic(null);
          if (fetched?.lectures && fetched.lectures.length > 0) {
            setActiveLectureVideoId(fetched.lectures[0].video_id);
          }
        });
      }
    }
  }, [activeSection, currentTopicName, currentRoadmap?.id]);

  // Keep activeLectureVideoId aligned with current playing lecture
  useEffect(() => {
    if (currentPlayingLecture && currentPlayingLecture.video_id !== activeLectureVideoId) {
      setActiveLectureVideoId(currentPlayingLecture.video_id);
    }
  }, [currentPlayingLecture?.video_id]);

  const onTopicSelect = (
    roadmapId: string,
    rawTopic: string,
    existingPlaylist?: any
  ) => {
    setActiveSection("lectures");
    handleTopicClickAndRedirect(roadmapId, rawTopic, existingPlaylist);
  };

  return (
    <motion.div
      initial={shouldReduceMotion ? { opacity: 1 } : { opacity: 0, x: 25 }}
      animate={{ opacity: 1, x: 0 }}
      exit={shouldReduceMotion ? { opacity: 1 } : { opacity: 0, x: -25 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3, ease: "easeOut" }}
      className="max-w-4xl mx-auto px-4 sm:px-6 py-6 w-full space-y-6 pb-24"
    >
      {/* 1. TOP NAVIGATION BAR */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => router.push(studentId ? `/dashboard?student_id=${studentId}` : "/dashboard")}
          className="w-11 h-11 rounded-full bg-[#181822] border border-[#262634] text-white flex items-center justify-center hover:bg-[#222230] transition-transform hover:scale-105 cursor-pointer shadow-md"
          title="Back to Dashboard"
          aria-label="Back to Dashboard"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <span className="px-3.5 py-1 rounded-full text-xs font-bold bg-teal-500/15 border border-teal-500/30 text-teal-300">
            {roadmaps.length} Saved {roadmaps.length === 1 ? "Role" : "Roles"}
          </span>
        </div>

        <button
          type="button"
          onClick={loadRoadmaps}
          className="w-11 h-11 rounded-full bg-[#181822] border border-[#262634] text-[#8E8E9C] hover:text-white flex items-center justify-center transition-transform hover:scale-105 cursor-pointer shadow-md"
          title="Reload Saved Roadmaps"
          aria-label="Reload Saved Roadmaps"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* 2. BIG BOLD PAGE HEADING */}
      <div className="pt-2">
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white leading-[1.05]">
          Skill <br />
          <span className="font-light text-teal-200">Tracks</span>
        </h1>
        <p className="text-xs text-[#8E8E9C] mt-2">
          Your saved jobs, verified skills, recruiter requirements, and interactive lecture tracking system.
        </p>
      </div>

      {/* 3. SECTION SELECTOR / TABS: REQ, SAVED, AND LEARNING LECTURES */}
      <div className="flex items-center gap-2 p-1.5 bg-[#14141C] border border-[#262634] rounded-2xl flex-wrap">
        <button
          type="button"
          onClick={() => setActiveSection("req")}
          aria-pressed={activeSection === "req"}
          className={`px-4 sm:px-5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 ${
            activeSection === "req"
              ? "bg-gradient-to-r from-amber-600 to-rose-600 text-white shadow-lg shadow-rose-500/25 font-extrabold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <ListChecks className="w-4 h-4 text-rose-400" />
          <span>REQ (Job Requirements &amp; What to Learn)</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveSection("saved")}
          aria-pressed={activeSection === "saved"}
          className={`px-4 sm:px-5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 ${
            activeSection === "saved"
              ? "bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/25 font-extrabold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <Briefcase className="w-4 h-4 text-purple-400" />
          <span>SAVED (Saved Jobs &amp; My Skills)</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveSection("lectures")}
          aria-pressed={activeSection === "lectures"}
          className={`px-4 sm:px-5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 ${
            activeSection === "lectures"
              ? "bg-gradient-to-r from-teal-500 to-emerald-600 text-white shadow-lg shadow-teal-500/25 font-extrabold"
              : "text-slate-400 hover:text-white"
          }`}
        >
          <GraduationCap className="w-4 h-4 text-teal-400" />
          <span>LEARNING LECTURES</span>
          {completedCount > 0 && (
            <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-black/40 text-emerald-300 border border-emerald-500/40">
              {completedCount}/{totalLecturesCount}
            </span>
          )}
        </button>
      </div>

      {videoNotice && (
        <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-center justify-between">
          <span>{videoNotice}</span>
          <button
            onClick={() => setVideoNotice(null)}
            className="text-amber-400 hover:text-white"
            aria-label="Dismiss notice"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* 4. CONTENT LIST */}
      <div className="space-y-6">
        {!isLoaded ? (
          <PageLoader
            title="Loading Skill Tracks..."
            subtitle="Fetching curriculum modules, saved job tracks, and curated video courses"
            size={72}
          />
        ) : roadmaps.length === 0 ? (
          <div className="py-20 px-4 text-center flex flex-col items-center justify-center rounded-3xl bg-[#14141C] border border-[#262634]">
            <div className="w-16 h-16 rounded-2xl bg-[#1D1D28] border border-white/10 flex items-center justify-center text-teal-400 mb-4 shadow-md">
              <FolderOpen className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-white mb-1">
              No Saved Jobs in Skill Tracks Yet
            </h3>
            <p className="text-xs text-slate-400 max-w-sm mb-6 leading-relaxed">
              Explore Job Pathways, click on any role fit analysis, and hit <strong>Save Roadmap</strong> to track your job details, skills, and requirements right here.
            </p>
            <button
              type="button"
              onClick={() => router.push("/jobs")}
              className="px-6 py-3 rounded-full bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-white text-xs font-bold shadow-lg shadow-teal-500/20 flex items-center gap-2 transition-all cursor-pointer hover:scale-105"
            >
              <span>Explore Jobs &amp; Roadmaps</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <>
            {/* LECTURES SECTION */}
            {activeSection === "lectures" && currentRoadmap && (
              <div className="rounded-3xl bg-[#140A12] border border-teal-500/40 p-6 space-y-6 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-80 h-80 bg-teal-500/10 blur-3xl pointer-events-none" />
                <div className="absolute bottom-0 left-0 w-60 h-60 bg-emerald-900/15 blur-3xl pointer-events-none" />

                {/* Header: Role & Topic Selector */}
                <div className="flex items-start justify-between gap-4 pb-4 border-b border-[#281321] flex-wrap relative z-10">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-md bg-teal-600 text-white text-[10px] font-black uppercase tracking-wider">
                        LECTURES SYSTEM
                      </span>
                      <span className="text-xs text-teal-300 font-bold">
                        {currentRoadmap.job.title} · {currentRoadmap.job.company}
                      </span>
                    </div>
                    <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                      Learning Lectures: <span className="text-teal-300">{currentTopicName || "Select a Skill"}</span>
                    </h2>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveSection("req")}
                    className="px-3.5 py-1.5 rounded-xl bg-[#281321] hover:bg-[#351E2D] border border-[#4A2848] text-xs font-bold text-slate-300 hover:text-white flex items-center gap-1.5 transition-colors cursor-pointer"
                  >
                    <span>Back to REQ Roadmap</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Skill Step Selector Pills */}
                <div className="space-y-2 relative z-10">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                    Choose Skill Roadmap Topic:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {currentRoadmap.whatToLearn?.learningSteps?.map((step, idx) => {
                      const isSelected = currentTopicName.toLowerCase() === step.skill.toLowerCase();
                      const topicData = currentRoadmap.yt_playlists?.[step.skill];
                      const comp = topicData?.completed_videos?.length || 0;
                      const tot = topicData?.total_videos || topicData?.lectures?.length || 0;

                      return (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => onTopicSelect(currentRoadmap.id, step.skill, topicData)}
                          aria-label={`Select skill topic: ${step.skill}`}
                          className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 border ${
                            isSelected
                              ? "bg-gradient-to-r from-teal-500 to-emerald-600 text-white border-teal-400 shadow-md scale-105"
                              : "bg-[#20101D] hover:bg-[#2C1729] text-slate-300 border-[#351E2D]"
                          }`}
                        >
                          <span>{step.skill}</span>
                          {tot > 0 && (
                            <span
                              className={`px-1.5 py-0.2 rounded text-[10px] font-mono ${
                                comp === tot && tot > 0
                                  ? "bg-emerald-400/30 text-emerald-200"
                                  : "bg-black/40 text-slate-300"
                              }`}
                            >
                              {comp}/{tot}
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Progress Tracker */}
                <ProgressTracker
                  currentTopicName={currentTopicName}
                  totalLecturesCount={totalLecturesCount}
                  completedCount={completedCount}
                  progressPercent={progressPercent}
                  loadingTopic={loadingTopic}
                  onResync={async () => {
                    setLoadingTopic(currentTopicName);
                    const fetched = await fetchYouTubeData(currentRoadmap.id, currentTopicName);
                    setLoadingTopic(null);
                    if (fetched?.lectures && fetched.lectures.length > 0) {
                      setActiveLectureVideoId(fetched.lectures[0].video_id);
                    }
                  }}
                />

                {/* Active Video Player */}
                <VideoPlayerModal
                  currentPlayingLecture={currentPlayingLecture}
                  currentPlaylistData={currentPlaylistData}
                  currentTopicName={currentTopicName}
                  totalLecturesCount={totalLecturesCount}
                  completedLecturesList={completedLecturesList}
                  activeLectureVideoId={activeLectureVideoId}
                  onToggleComplete={() => {
                    if (currentPlayingLecture) {
                      handleToggleLecture(currentRoadmap.id, currentTopicName, currentPlayingLecture.video_id);
                    }
                  }}
                />

                {/* Lectures List */}
                <div className="space-y-3 relative z-10">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-black uppercase tracking-wider text-white flex items-center gap-2">
                      <Tv className="w-4 h-4 text-teal-400" />
                      <span>All Video Lectures ({currentLectures.length})</span>
                    </h3>
                    <span className="text-xs text-slate-400">
                      Click any lecture to play or mark completed
                    </span>
                  </div>

                  {currentLectures.length === 0 ? (
                    <div className="p-8 text-center bg-black/40 rounded-2xl border border-white/5 space-y-2">
                      <Loader2 className="w-6 h-6 animate-spin text-teal-400 mx-auto" />
                      <p className="text-xs text-slate-300">Fetching lecture playlist for {currentTopicName}...</p>
                    </div>
                  ) : (
                    <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
                      {currentLectures.map((lec, lIdx) => (
                        <LessonCard
                          key={lec.id || lIdx}
                          lecture={lec}
                          index={lIdx}
                          isPlaying={(activeLectureVideoId || currentLectures[0].video_id) === lec.video_id}
                          isCompleted={completedLecturesList.includes(lec.video_id)}
                          onSelect={() => setActiveLectureVideoId(lec.video_id)}
                          onToggleComplete={() =>
                            handleToggleLecture(currentRoadmap.id, currentTopicName, lec.video_id)
                          }
                        />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* REQ & SAVED SECTIONS */}
            {activeSection !== "lectures" && (
              <RoadmapList
                roadmaps={roadmaps}
                activeSection={activeSection}
                onDelete={handleDelete}
                onTopicClick={onTopicSelect}
              />
            )}
          </>
        )}
      </div>
    </motion.div>
  );
}

export default function SkillTracksPage() {
  return (
    <Suspense
      fallback={
        <PageLoader
          title="Loading Skill Tracks..."
          size={84}
        />
      }
    >
      <SkillTracksPageContent />
    </Suspense>
  );
}
