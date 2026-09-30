"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

interface CareerPathwaysModalProps {
  isOpen: boolean;
  onClose: () => void;
  educationStage?: "class_10" | "intermediate" | "b_tech" | string | null;
  onSelectStreamForScholarships?: (streamName: string) => void;
}

export default function CareerPathwaysModal({
  isOpen,
  onClose,
}: CareerPathwaysModalProps) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-[#12121A] border border-[#2B2B3C] rounded-2xl w-full max-w-2xl h-[420px] flex flex-col shadow-2xl relative overflow-hidden"
        >
          {/* Header */}
          <div className="p-4 border-b border-[#20202C] flex items-center justify-between">
            <h2 className="text-base font-semibold text-white tracking-tight">
              Career Pathways
            </h2>
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 text-[#8E8E9C] hover:text-white hover:bg-[#1E1E2C] rounded-lg transition-colors cursor-pointer"
              title="Close modal"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Blank Body */}
          <div className="flex-1" />
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
