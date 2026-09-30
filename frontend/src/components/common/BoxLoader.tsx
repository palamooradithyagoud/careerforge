"use client";

import React from "react";

interface BoxLoaderProps {
  size?: number;
  color?: string;
  className?: string;
}

export default function BoxLoader({
  size = 112,
  color,
  className = "",
}: BoxLoaderProps) {
  const scale = size / 112;

  return (
    <div
      className={`inline-flex items-center justify-center ${className}`.trim()}
      style={{
        width: `${size}px`,
        height: `${size}px`,
      }}
    >
      <div
        className="box-loader shrink-0"
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "center center",
          ...(color ? ({ "--loader-color": color } as React.CSSProperties) : {}),
        }}
      >
        <div className="box1" />
        <div className="box2" />
        <div className="box3" />
      </div>
    </div>
  );
}

export function PageLoader({
  title = "Loading...",
  subtitle,
  size = 80,
  color,
}: {
  title?: string;
  subtitle?: string;
  size?: number;
  color?: string;
}) {
  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center text-center px-4 py-16 gap-6 select-none">
      <BoxLoader size={size} color={color} />
      {(title || subtitle) && (
        <div className="space-y-1">
          {title && <h3 className="text-sm font-bold text-white tracking-wide">{title}</h3>}
          {subtitle && <p className="text-xs text-[#8E8E9C] max-w-sm">{subtitle}</p>}
        </div>
      )}
    </div>
  );
}
