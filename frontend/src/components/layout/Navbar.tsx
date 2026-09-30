"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Compass, Sparkles, User, LogOut, ArrowUpRight } from "lucide-react";

import AscendLogo from "@/components/common/AscendLogo";
import StrokeText from "@/components/common/StrokeText";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("skillcatalyst_session");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setUserName(parsed.name || "Student");
      } catch {
        // ignore
      }
    }
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("skillcatalyst_session");
    localStorage.removeItem("skillcatalyst_profile");
    setUserName(null);
    window.dispatchEvent(new Event("storage"));
    router.push("/login");
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-[#0C0C10]/85 backdrop-blur-md border-b border-[#20202C]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand with ASCEND Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <AscendLogo size="sm" showText={true} />
        </Link>

        {/* Center Pill Navigation */}
        <nav className="hidden md:flex items-center gap-1.5 p-1 rounded-full bg-[#161620] border border-[#262634]">
          <Link
            href="/scholarships"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
              pathname.startsWith("/scholarships")
                ? "bg-white text-black font-semibold shadow-xs"
                : "text-[#8E8E9C] hover:text-white"
            }`}
          >
            Scholarships
          </Link>
          <Link
            href="/onboarding"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
              pathname.startsWith("/onboarding")
                ? "bg-white text-black font-semibold shadow-xs"
                : "text-[#8E8E9C] hover:text-white"
            }`}
          >
            Build Profile
          </Link>
          <Link
            href="/profile"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
              pathname.startsWith("/profile")
                ? "bg-white text-black font-semibold shadow-xs"
                : "text-[#8E8E9C] hover:text-white"
            }`}
          >
            Profile Section
          </Link>
          <Link
            href="/jobs"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
              pathname.startsWith("/jobs")
                ? "bg-white text-black font-semibold shadow-xs"
                : "text-[#8E8E9C] hover:text-white"
            }`}
          >
            Job Pathways
          </Link>
          <Link
            href="/dashboard"
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
              pathname.startsWith("/dashboard")
                ? "bg-white text-black font-semibold shadow-xs"
                : "text-[#8E8E9C] hover:text-white"
            }`}
          >
            Dashboard
          </Link>
        </nav>

        {/* Right User Action */}
        <div className="flex items-center gap-3">
          {userName ? (
            <div className="flex items-center gap-2.5">
              <Link
                href="/profile"
                className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#181824] hover:bg-[#222232] border border-[#282838] hover:border-[#38384C] text-xs text-white transition-all cursor-pointer"
                title="View Profile Section"
              >
                <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-amber-400 to-pink-500 flex items-center justify-center text-black font-bold text-[11px] shrink-0">
                  {userName.charAt(0).toUpperCase()}
                </div>
                <StrokeText
                  text={userName}
                  strokeColor="#A78BFA"
                  fillColor="#F8FAFC"
                  strokeWidth={0.9}
                  drawDuration={1.3}
                  fillDelay={0.1}
                  stagger={0.03}
                  ease="power2.out"
                  trigger="mount"
                  fillMode="wipe"
                  fontSize={13}
                  fontWeight={600}
                  letterSpacing={0}
                  reverse={false}
                />
              </Link>
              <button
                onClick={handleLogout}
                title="Log out"
                className="p-1.5 text-[#8E8E9C] hover:text-white hover:bg-[#1A1A26] rounded-full transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                href="/login"
                className="px-3.5 py-1.5 text-xs font-medium text-[#8E8E9C] hover:text-white transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/login"
                className="px-4 py-1.5 text-xs font-semibold bg-white text-black rounded-full hover:bg-neutral-200 transition-colors shadow-xs flex items-center gap-1"
              >
                <span>Demo Entry</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
