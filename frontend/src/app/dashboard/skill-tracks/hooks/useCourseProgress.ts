"use client";

import { useState, useEffect } from "react";
import {
  SavedSkillRoadmap,
  SavedYouTubePlaylist,
  YouTubeLecture,
  getSavedRoadmaps,
  removeRoadmap,
  updateRoadmapYouTubePlaylist,
  toggleVideoCompletion,
} from "@/lib/roadmapStorage";
import { api } from "@/lib/api";

export function useCourseProgress(studentId: string | null) {
  const [roadmaps, setRoadmaps] = useState<SavedSkillRoadmap[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [selectedRoadmapId, setSelectedRoadmapId] = useState<string | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [activeLectureVideoId, setActiveLectureVideoId] = useState<string | null>(null);
  const [loadingTopic, setLoadingTopic] = useState<string | null>(null);
  const [videoNotice, setVideoNotice] = useState<string | null>(null);

  const loadRoadmaps = () => {
    const list = getSavedRoadmaps();
    setRoadmaps(list);
    setIsLoaded(true);

    if (list.length > 0 && !selectedRoadmapId) {
      setSelectedRoadmapId(list[0].id);
      const firstStep = list[0].whatToLearn?.learningSteps?.[0]?.skill;
      if (firstStep) {
        setSelectedTopic(firstStep);
      }
    }
  };

  useEffect(() => {
    loadRoadmaps();
    const handleStorage = () => loadRoadmaps();
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  const handleDelete = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (selectedRoadmapId === id) {
      const remaining = roadmaps.filter((r) => r.id !== id);
      setSelectedRoadmapId(remaining.length > 0 ? remaining[0].id : null);
    }
    removeRoadmap(id);
    loadRoadmaps();
  };

  const fetchYouTubeData = async (
    roadmapId: string,
    rawTopic: string
  ): Promise<SavedYouTubePlaylist | null> => {
    const topic = rawTopic.replace(/^[×⚠✓\s]+/, "").replace(/\s*\([^)]*\)/g, "").trim();
    if (!topic) return null;

    let playlistData: SavedYouTubePlaylist | null = null;

    try {
      const res = await api.skillTracks.getYouTubePlaylist({
        topic,
        job_id: roadmapId,
        student_id: studentId || undefined,
      });

      if (res && res.success && res.playlist) {
        playlistData = {
          topic,
          playlistId: res.playlist.playlist_id,
          title: res.playlist.title,
          channelTitle: res.playlist.channel_title,
          embedUrl: res.playlist.embed_url,
          thumbnail: res.playlist.thumbnail,
          isPlaylist: res.playlist.is_playlist,
          total_videos: (res.playlist as any).total_videos || (res.playlist as any).lectures?.length || 1,
          lectures: (res.playlist as any).lectures || [],
          completed_videos: (res.playlist as any).completed_videos || [],
        };
      }
    } catch (backendErr) {
      console.warn("Backend YouTube endpoint fallback to client fetch:", backendErr);
    }

    if (!playlistData) {
      const YT_KEY = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY || "";
      const query = encodeURIComponent(`${topic} full course tutorial playlist`);
      try {
        const ytRes = await fetch(
          `https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&q=${query}&maxResults=1&key=${YT_KEY}`
        );

        if (ytRes.ok) {
          const ytJson = await ytRes.json();
          if (ytJson.items && ytJson.items.length > 0) {
            const item = ytJson.items[0];
            const playlistId = item.id.playlistId;

            let lectures: YouTubeLecture[] = [];
            try {
              const plRes = await fetch(
                `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId=${playlistId}&maxResults=25&key=${YT_KEY}`
              );
              if (plRes.ok) {
                const plJson = await plRes.json();
                lectures = (plJson.items || []).map((pItem: any, idx: number) => ({
                  id: pItem.id || `lec-${idx}`,
                  video_id: pItem.snippet?.resourceId?.videoId,
                  title: pItem.snippet?.title || `Lecture ${idx + 1}`,
                  position: pItem.snippet?.position ?? idx,
                  thumbnail: pItem.snippet?.thumbnails?.high?.url || pItem.snippet?.thumbnails?.default?.url,
                  channel_title: pItem.snippet?.channelTitle || item.snippet.channelTitle,
                  embed_url: `https://www.youtube-nocookie.com/embed/${pItem.snippet?.resourceId?.videoId}?autoplay=1&enablejsapi=1`,
                })).filter((l: YouTubeLecture) => l.video_id);
              }
            } catch (pErr) {
              console.error("Error fetching playlist items client-side:", pErr);
            }

            playlistData = {
              topic,
              playlistId,
              title: item.snippet.title,
              channelTitle: item.snippet.channelTitle,
              embedUrl: `https://www.youtube-nocookie.com/embed/videoseries?list=${playlistId}&autoplay=1&enablejsapi=1`,
              thumbnail: item.snippet.thumbnails?.high?.url || item.snippet.thumbnails?.default?.url,
              isPlaylist: true,
              total_videos: lectures.length > 0 ? lectures.length : 1,
              lectures,
              completed_videos: [],
            };
          }
        }

        if (!playlistData) {
          const vQuery = encodeURIComponent(`${topic} full course tutorial`);
          const vRes = await fetch(
            `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=${vQuery}&maxResults=1&key=${YT_KEY}`
          );
          if (vRes.ok) {
            const vJson = await vRes.json();
            if (vJson.items && vJson.items.length > 0) {
              const vItem = vJson.items[0];
              const videoId = vItem.id.videoId;
              playlistData = {
                topic,
                playlistId: videoId,
                title: vItem.snippet.title,
                channelTitle: vItem.snippet.channelTitle,
                embedUrl: `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&enablejsapi=1`,
                thumbnail: vItem.snippet.thumbnails?.high?.url,
                isPlaylist: false,
                total_videos: 1,
                lectures: [
                  {
                    id: "single-vid",
                    video_id: videoId,
                    title: vItem.snippet.title,
                    position: 0,
                    thumbnail: vItem.snippet.thumbnails?.high?.url,
                    channel_title: vItem.snippet.channelTitle,
                    embed_url: `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&enablejsapi=1`,
                  },
                ],
                completed_videos: [],
              };
            }
          }
        }
      } catch (clientErr) {
        console.error("Client YouTube fetch error:", clientErr);
      }
    }

    if (playlistData) {
      updateRoadmapYouTubePlaylist(roadmapId, topic, playlistData);
      loadRoadmaps();
    }

    return playlistData;
  };

  const handleTopicClickAndRedirect = async (
    roadmapId: string,
    rawTopic: string,
    existingPlaylist?: SavedYouTubePlaylist
  ) => {
    const topic = rawTopic.replace(/^[×⚠✓\s]+/, "").replace(/\s*\([^)]*\)/g, "").trim();
    if (!topic) return;

    setSelectedRoadmapId(roadmapId);
    setSelectedTopic(topic);
    setLoadingTopic(topic);
    setVideoNotice(null);

    let pData = existingPlaylist;
    if (!pData || !pData.embedUrl || !pData.lectures || pData.lectures.length <= 1) {
      pData = (await fetchYouTubeData(roadmapId, topic)) || undefined;
    }

    if (pData) {
      const firstVideoId = pData.lectures?.[0]?.video_id || pData.playlistId;
      setActiveLectureVideoId(firstVideoId);
    } else {
      setVideoNotice(`Unable to load YouTube course for "${topic}".`);
    }

    setLoadingTopic(null);
  };

  const handleToggleLecture = async (
    roadmapId: string,
    topic: string,
    videoId: string
  ) => {
    const result = toggleVideoCompletion(roadmapId, topic, videoId);
    loadRoadmaps();

    try {
      await api.skillTracks.toggleLecture({
        job_id: roadmapId,
        topic,
        video_id: videoId,
        completed: result.completed,
        student_id: studentId || undefined,
      });
    } catch (e) {
      console.warn("Backend progress sync warning:", e);
    }
  };

  const currentRoadmap = roadmaps.find((r) => r.id === selectedRoadmapId) || roadmaps[0];
  const currentTopicName = selectedTopic || currentRoadmap?.whatToLearn?.learningSteps?.[0]?.skill || "";
  const currentPlaylistData: SavedYouTubePlaylist | undefined = currentRoadmap?.yt_playlists?.[currentTopicName];

  const currentLectures = currentPlaylistData?.lectures || [];
  const totalLecturesCount = currentPlaylistData?.total_videos || currentLectures.length || (currentPlaylistData ? 1 : 0);
  const completedLecturesList = currentPlaylistData?.completed_videos || [];
  const completedCount = completedLecturesList.length;
  const progressPercent = totalLecturesCount > 0 ? Math.min(100, Math.round((completedCount / totalLecturesCount) * 100)) : 0;
  const currentPlayingLecture = currentLectures.find((l) => l.video_id === activeLectureVideoId) || currentLectures[0];

  return {
    roadmaps,
    isLoaded,
    selectedRoadmapId,
    setSelectedRoadmapId,
    selectedTopic,
    setSelectedTopic,
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
  };
}
