"use client";

import React from "react";
import { SavedSkillRoadmap, SavedYouTubePlaylist } from "@/lib/roadmapStorage";
import { RoadmapCard } from "./RoadmapCard";

interface RoadmapListProps {
  roadmaps: SavedSkillRoadmap[];
  activeSection: "req" | "saved";
  onDelete: (id: string, e: React.MouseEvent) => void;
  onTopicClick: (
    roadmapId: string,
    rawTopic: string,
    existingPlaylist?: SavedYouTubePlaylist
  ) => void;
}

export function RoadmapList({
  roadmaps,
  activeSection,
  onDelete,
  onTopicClick,
}: RoadmapListProps) {
  return (
    <div className="space-y-6">
      {roadmaps.map((item) => (
        <RoadmapCard
          key={item.id}
          item={item}
          activeSection={activeSection}
          onDelete={onDelete}
          onTopicClick={onTopicClick}
        />
      ))}
    </div>
  );
}
