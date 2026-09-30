"use client";

import React from "react";
import { Play, Check, CheckSquare, ExternalLink, Info } from "lucide-react";
import { SavedYouTubePlaylist, YouTubeLecture } from "@/lib/roadmapStorage";

interface VideoPlayerModalProps {
  currentPlayingLecture?: YouTubeLecture;
  currentPlaylistData?: SavedYouTubePlaylist;
  currentTopicName: string;
  totalLecturesCount: number;
  completedLecturesList: string[];
  activeLectureVideoId: string | null;
  onToggleComplete: () => void;
}

export function VideoPlayerModal({
  currentPlayingLecture,
  currentPlaylistData,
  currentTopicName,
  totalLecturesCount,
  completedLecturesList,
  activeLectureVideoId,
  onToggleComplete,
}: VideoPlayerModalProps) {
  const isCurrentDone = currentPlayingLecture
    ? completedLecturesList.includes(currentPlayingLecture.video_id)
    : false;

  const embedSrc =
    currentPlayingLecture?.embed_url ||
    (activeLectureVideoId
      ? `https://www.youtube-nocookie.com/embed/${activeLectureVideoId}?autoplay=1&enablejsapi=1`
      : currentPlaylistData?.embedUrl || "https://www.youtube-nocookie.com/embed");

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-[#1C0D17] via-black to-[#140A12] border border-white/15 shadow-2xl space-y-4 relative z-10">
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-2.5">
          <span className="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center text-white shadow-md">
            <Play className="w-4 h-4 fill-white" />
          </span>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-black uppercase text-red-400 tracking-wider">
                Now Watching
              </span>
              {currentPlayingLecture && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30">
                  Lecture {currentPlayingLecture.position + 1} of {totalLecturesCount}
                </span>
              )}
            </div>
            <h4 className="text-sm sm:text-base font-extrabold text-white line-clamp-1">
              {currentPlayingLecture?.title || currentPlaylistData?.title || `${currentTopicName} Course`}
            </h4>
          </div>
        </div>

        {/* Quick Toggle Done for active video */}
        {currentPlayingLecture && (
          <button
            type="button"
            onClick={onToggleComplete}
            aria-label={isCurrentDone ? "Mark lecture incomplete" : "Mark lecture completed"}
            className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-md ${
              isCurrentDone
                ? "bg-emerald-600 text-white hover:bg-emerald-500"
                : "bg-[#281321] hover:bg-[#351E2D] border border-teal-500/40 text-teal-300 hover:text-white"
            }`}
          >
            {isCurrentDone ? (
              <>
                <Check className="w-4 h-4 stroke-[3]" />
                <span>Completed ✓</span>
              </>
            ) : (
              <>
                <CheckSquare className="w-4 h-4" />
                <span>Mark Lecture Completed</span>
              </>
            )}
          </button>
        )}
      </div>

      {/* YOUTUBE IFRAME */}
      <div className="relative w-full aspect-video rounded-xl overflow-hidden border border-white/15 bg-black shadow-2xl">
        <iframe
          src={embedSrc}
          title={currentPlayingLecture?.title || "Course Video"}
          className="w-full h-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400 pt-1 flex-wrap gap-2">
        <span className="text-slate-300">
          <strong>Channel:</strong> {currentPlayingLecture?.channel_title || currentPlaylistData?.channelTitle || "YouTube"}
        </span>
        <div className="flex items-center gap-3 flex-wrap">
          {currentPlayingLecture?.video_id && (
            <a
              href={`https://www.youtube.com/watch?v=${currentPlayingLecture.video_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-2.5 py-1 rounded-lg bg-red-600/20 hover:bg-red-600/30 text-red-300 hover:text-red-200 border border-red-500/30 flex items-center gap-1.5 font-bold transition-all text-xs"
            >
              <span>Open Video in YouTube</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
          {currentPlaylistData?.playlistId && (
            <a
              href={`https://www.youtube.com/playlist?list=${currentPlaylistData.playlistId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-teal-400 hover:text-teal-300 flex items-center gap-1 font-semibold"
            >
              <span>Open Complete Playlist</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>

      {/* Privacy & Browser note */}
      <div className="flex items-center gap-2 p-2.5 rounded-xl bg-[#20101D] border border-teal-500/20 text-[11px] text-slate-300">
        <Info className="w-4 h-4 text-teal-400 shrink-0" />
        <span>
          <strong className="text-teal-300">Brave Shields / Adblock note:</strong> YouTube Privacy-Enhanced mode is active. If your browser shields block player telemetry, videos still play or you can use the direct YouTube link above.
        </span>
      </div>
    </div>
  );
}
