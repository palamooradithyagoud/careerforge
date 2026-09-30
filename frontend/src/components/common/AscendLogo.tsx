"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import StrokeText from "@/components/common/StrokeText";

interface AscendLogoProps {
  size?: "xs" | "sm" | "md" | "lg" | "xl" | "2xl";
  variant?: "horizontal" | "stacked" | "icon" | "badge";
  showText?: boolean;
  className?: string;
  withLink?: boolean;
  href?: string;
}

export default function AscendLogo({
  size = "md",
  variant = "horizontal",
  showText = true,
  className = "",
  withLink = false,
  href = "/",
}: AscendLogoProps) {
  // Dimensions mapping
  const dimensions = {
    xs: { icon: 20, fontSize: 13, strokeWidth: 0.9, letterSpacing: 2 },
    sm: { icon: 26, fontSize: 16, strokeWidth: 1.0, letterSpacing: 2.5 },
    md: { icon: 34, fontSize: 20, strokeWidth: 1.2, letterSpacing: 3 },
    lg: { icon: 44, fontSize: 26, strokeWidth: 1.3, letterSpacing: 4 },
    xl: { icon: 60, fontSize: 34, strokeWidth: 1.4, letterSpacing: 5 },
    "2xl": { icon: 84, fontSize: 48, strokeWidth: 1.6, letterSpacing: 6 },
  }[size];

  const iconElement = (
    <div
      className="relative flex items-center justify-center shrink-0 group select-none"
      style={{ width: dimensions.icon, height: dimensions.icon }}
    >
      {/* Subtle ambient glow behind the logo */}
      <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-amber-500/20 via-violet-500/20 to-transparent blur-md group-hover:scale-125 transition-transform duration-500 opacity-80" />

      {/* High-res optimized Ascend Icon */}
      <Image
        src="/ascend-icon.png"
        alt="ASCEND Logo"
        width={dimensions.icon * 2}
        height={dimensions.icon * 2}
        className="w-full h-full object-contain relative z-10 drop-shadow-[0_2px_10px_rgba(251,191,36,0.2)]"
        priority
      />
    </div>
  );

  const textElement = showText && (
    <div className="flex flex-col select-none justify-center">
      <StrokeText
        text="ASCEND"
        strokeColor="#F59E0B"
        fillColor="#F8FAFC"
        strokeWidth={dimensions.strokeWidth}
        drawDuration={1.4}
        fillDelay={0.15}
        stagger={0.06}
        ease="power2.out"
        trigger="mount"
        fillMode="wipe"
        fontSize={dimensions.fontSize}
        fontWeight={900}
        letterSpacing={dimensions.letterSpacing}
        reverse={false}
      />
      {size === "xl" || size === "2xl" ? (
        <span className="text-[10px] tracking-[0.25em] text-[#8E8E9C] font-semibold uppercase mt-0.5">
          Student Career Intelligence
        </span>
      ) : null}
    </div>
  );

  const content = (() => {
    if (variant === "icon") {
      return iconElement;
    }

    if (variant === "badge") {
      return (
        <div
          className={`inline-flex items-center gap-2.5 px-3 py-1.5 rounded-2xl bg-[#14141E]/90 border border-[#2B2B3C] shadow-lg backdrop-blur-md ${className}`}
        >
          {iconElement}
          {textElement}
        </div>
      );
    }

    if (variant === "stacked") {
      return (
        <div className={`flex flex-col items-center text-center gap-3 ${className}`}>
          {iconElement}
          {textElement}
        </div>
      );
    }

    // Default horizontal
    return (
      <div className={`flex items-center gap-3 ${className}`}>
        {iconElement}
        {textElement}
      </div>
    );
  })();

  if (withLink) {
    return (
      <Link href={href} className="group inline-flex items-center">
        {content}
      </Link>
    );
  }

  return content;
}
