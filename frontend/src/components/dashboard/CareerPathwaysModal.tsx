"use client";

import React, { useState, useEffect, useTransition } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Search,
  ExternalLink,
  Clock,
  Sparkles,
  RefreshCw,
  Newspaper,
  Flame,
  Globe,
  Radio,
  Cpu,
  ArrowUpRight,
  AlertCircle
} from "lucide-react";

interface NewsArticle {
  source: { id: string | null; name: string };
  author: string | null;
  title: string;
  description: string | null;
  url: string;
  urlToImage: string | null;
  publishedAt: string;
  content: string | null;
}

interface TechbitsModalProps {
  isOpen: boolean;
  onClose: () => void;
  educationStage?: "class_10" | "intermediate" | "b_tech" | string | null;
  onSelectStreamForScholarships?: (streamName: string) => void;
}

const COMPANY_FILTERS = [
  { id: "All", label: "All", brandColor: "from-pink-500 to-rose-500", activeBg: "bg-pink-500/20 text-pink-300 border-pink-500/40" },
  { id: "Google", label: "Google", brandColor: "from-blue-500 to-cyan-500", activeBg: "bg-blue-500/20 text-blue-300 border-blue-500/40" },
  { id: "NVIDIA", label: "NVIDIA", brandColor: "from-emerald-500 to-green-500", activeBg: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40" },
  { id: "Microsoft", label: "Microsoft", brandColor: "from-sky-500 to-blue-500", activeBg: "bg-sky-500/20 text-sky-300 border-sky-500/40" },
  { id: "Apple", label: "Apple", brandColor: "from-neutral-400 to-zinc-400", activeBg: "bg-neutral-500/20 text-neutral-200 border-neutral-400/40" },
  { id: "OpenAI", label: "OpenAI", brandColor: "from-teal-500 to-emerald-500", activeBg: "bg-teal-500/20 text-teal-300 border-teal-500/40" }
];

function formatTimeAgo(isoString: string): string {
  try {
    const date = new Date(isoString);
    const now = new Date();
    const diffSec = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffSec < 60) return "Just now";
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHr = Math.floor(diffMin / 60);
    if (diffHr < 24) return `${diffHr}h ago`;
    const diffDay = Math.floor(diffHr / 24);
    if (diffDay < 7) return `${diffDay}d ago`;

    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric"
    });
  } catch {
    return "Recently";
  }
}

export default function CareerPathwaysModal({
  isOpen,
  onClose
}: TechbitsModalProps) {
  const [selectedCompany, setSelectedCompany] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [activeQuery, setActiveQuery] = useState<string>("");
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  // Fetch articles from /api/techbits
  const fetchArticles = async (company: string, query: string) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (company && company !== "All") params.set("company", company);
      if (query.trim()) params.set("q", query.trim());

      const res = await fetch(`/api/techbits?${params.toString()}`);
      if (!res.ok) {
        throw new Error("Unable to fetch latest tech stories");
      }
      const data = await res.json();
      setArticles(data.articles || []);
    } catch (err: any) {
      console.error("Error loading Techbits:", err);
      setError("Unable to load latest tech articles right now.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchArticles(selectedCompany, activeQuery);
    }
  }, [isOpen, selectedCompany, activeQuery]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setActiveQuery(searchQuery);
  };

  const handleCompanySelect = (companyId: string) => {
    setSelectedCompany(companyId);
  };

  const handleClearFilters = () => {
    setSearchQuery("");
    setActiveQuery("");
    setSelectedCompany("All");
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div
        className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/85 backdrop-blur-md overflow-y-auto"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 15 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 15 }}
          transition={{ duration: 0.22, ease: "easeOut" }}
          onClick={(e) => e.stopPropagation()}
          className="bg-[#0F0F16] border border-[#252538] rounded-3xl w-full max-w-5xl max-h-[92vh] flex flex-col shadow-[0_25px_70px_rgba(0,0,0,0.9)] relative overflow-hidden"
        >
          {/* Top Symmetric Accent Bar */}
          <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500" />

          {/* Modal Header */}
          <div className="p-4 sm:p-5 border-b border-[#1E1E2C] flex items-center justify-between gap-4 bg-[#12121C]">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-pink-500/20 to-purple-500/20 border border-pink-500/30 flex items-center justify-center text-pink-400 shrink-0 shadow-[0_0_15px_rgba(236,72,153,0.15)]">
                <Cpu className="w-5 h-5 text-pink-400" />
              </div>
              <div>
                <div className="flex items-center gap-2.5 flex-wrap">
                  <h2 className="text-lg sm:text-xl font-extrabold text-white tracking-tight">
                    Techbits
                  </h2>
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-pink-500/15 border border-pink-500/30 text-pink-300">
                    <span className="w-1.5 h-1.5 rounded-full bg-pink-400 animate-pulse" />
                    Latest TechNews
                  </span>
                </div>
                <p className="text-xs text-[#8E8E9F] mt-0.5">
                  Curated breaking developer telemetry, engineering breakthroughs & tech releases
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="p-2 text-[#8E8E9F] hover:text-white hover:bg-[#1E1E2C] rounded-full transition-colors cursor-pointer"
              title="Close Techbits"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Controls Bar: Search & Company Filters */}
          <div className="p-4 sm:p-5 border-b border-[#1A1A28] bg-[#0E0E15]/90 space-y-3.5">
            {/* Search Input */}
            <form onSubmit={handleSearchSubmit} className="relative flex items-center">
              <Search className="absolute left-3.5 w-4 h-4 text-[#757589] pointer-events-none" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search any tech keyword (e.g. AI, Quantum, LLMs, Cybersecurity)..."
                className="w-full pl-10 pr-24 py-2.5 rounded-xl bg-[#161622] border border-[#2B2B3E] text-white text-xs sm:text-sm placeholder-[#6E6E84] focus:outline-none focus:border-pink-500/60 focus:ring-1 focus:ring-pink-500/50 transition-all"
              />
              <div className="absolute right-2 flex items-center gap-1">
                {searchQuery && (
                  <button
                    type="button"
                    onClick={() => {
                      setSearchQuery("");
                      setActiveQuery("");
                    }}
                    className="p-1 text-[#8E8E9F] hover:text-white rounded-md transition-colors text-xs"
                    title="Clear search"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
                <button
                  type="submit"
                  className="px-3 py-1.5 rounded-lg bg-pink-500/20 hover:bg-pink-500/30 text-pink-300 border border-pink-500/30 font-semibold text-xs transition-colors cursor-pointer"
                >
                  Search
                </button>
              </div>
            </form>

            {/* Company Quick Filter Tabs ("What's New") */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1 custom-scrollbar">
              <span className="text-[11px] uppercase tracking-wider font-extrabold text-[#7E7E94] whitespace-nowrap mr-1 flex items-center gap-1">
                <Flame className="w-3 h-3 text-pink-400" />
                What&apos;s New:
              </span>
              {COMPANY_FILTERS.map((comp) => {
                const isActive = selectedCompany === comp.id;
                return (
                  <button
                    key={comp.id}
                    type="button"
                    onClick={() => handleCompanySelect(comp.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer border ${
                      isActive
                        ? comp.activeBg + " shadow-[0_0_12px_rgba(236,72,153,0.15)]"
                        : "bg-[#161622] border-[#252538] text-[#9E9EB2] hover:text-white hover:border-[#383852]"
                    }`}
                  >
                    {comp.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Modal Body / Article Feed */}
          <div className="p-4 sm:p-6 overflow-y-auto flex-1 custom-scrollbar space-y-4">
            {/* Header info row */}
            <div className="flex items-center justify-between text-xs text-[#8E8E9F] px-1">
              <div className="flex items-center gap-2">
                <span>
                  Showing{" "}
                  <strong className="text-white">
                    {selectedCompany === "All" ? "Latest Tech" : selectedCompany}
                  </strong>{" "}
                  stories
                  {activeQuery && (
                    <>
                      {" "}matching &ldquo;<span className="text-pink-400">{activeQuery}</span>&rdquo;
                    </>
                  )}
                </span>
              </div>
              <button
                type="button"
                onClick={() => fetchArticles(selectedCompany, activeQuery)}
                className="flex items-center gap-1.5 text-xs text-[#8E8E9F] hover:text-pink-300 transition-colors cursor-pointer"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-pink-400" : ""}`} />
                <span>Refresh</span>
              </button>
            </div>

            {/* Loading State */}
            {loading && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-2xl bg-[#14141E] border border-[#232332] animate-pulse space-y-3"
                  >
                    <div className="h-40 rounded-xl bg-[#1D1D2C]" />
                    <div className="h-4 w-3/4 bg-[#1D1D2C] rounded-md" />
                    <div className="h-3 w-full bg-[#1D1D2C] rounded-md" />
                    <div className="h-3 w-5/6 bg-[#1D1D2C] rounded-md" />
                    <div className="pt-2 flex justify-between items-center">
                      <div className="h-3 w-20 bg-[#1D1D2C] rounded-md" />
                      <div className="h-3 w-16 bg-[#1D1D2C] rounded-md" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Error State */}
            {!loading && error && (
              <div className="p-8 text-center rounded-2xl bg-[#17141D] border border-rose-500/20 space-y-3">
                <AlertCircle className="w-8 h-8 text-rose-400 mx-auto" />
                <h4 className="text-sm font-bold text-white">Notice</h4>
                <p className="text-xs text-[#A6A6BC] max-w-md mx-auto">{error}</p>
                <button
                  type="button"
                  onClick={() => fetchArticles(selectedCompany, activeQuery)}
                  className="px-4 py-2 rounded-xl bg-pink-500/20 hover:bg-pink-500/30 text-pink-300 border border-pink-500/40 text-xs font-bold transition-all cursor-pointer inline-flex items-center gap-1.5"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Retry Fetching</span>
                </button>
              </div>
            )}

            {/* Empty State */}
            {!loading && !error && articles.length === 0 && (
              <div className="p-10 text-center rounded-2xl bg-[#13131D] border border-[#232332] space-y-3 my-6">
                <div className="w-12 h-12 rounded-2xl bg-pink-500/10 border border-pink-500/20 text-pink-400 flex items-center justify-center mx-auto">
                  <Newspaper className="w-6 h-6" />
                </div>
                <h4 className="text-base font-bold text-white">
                  No tech stories found for this search
                </h4>
                <p className="text-xs text-[#8E8E9F] max-w-sm mx-auto">
                  Try searching a different keyword or explore stories from our company filters above.
                </p>
                <button
                  type="button"
                  onClick={handleClearFilters}
                  className="px-4 py-2 rounded-xl bg-pink-500 hover:bg-pink-600 text-white text-xs font-bold transition-all shadow-md cursor-pointer"
                >
                  Reset Filters
                </button>
              </div>
            )}

            {/* Article Cards Grid */}
            {!loading && !error && articles.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {articles.map((item, index) => (
                  <TechbitCard key={`${item.url}-${index}`} article={item} />
                ))}
              </div>
            )}
          </div>

          {/* Modal Footer */}
          <div className="p-4 sm:p-5 border-t border-[#1E1E2C] bg-[#0C0C12] flex items-center justify-between gap-3 flex-wrap">
            <span className="text-[11px] text-[#717186] flex items-center gap-1.5">
              <Sparkles className="w-3 h-3 text-pink-400" />
              Powered by NewsAPI & Quality Technology Publications (The Verge, TechCrunch, Wired, Ars Technica)
            </span>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-1.5 rounded-xl bg-[#1E1E2C] hover:bg-[#2A2A3C] text-white font-bold text-xs transition-colors cursor-pointer ml-auto"
            >
              Close
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}

function TechbitCard({ article }: { article: NewsArticle }) {
  const [imageError, setImageError] = useState(false);

  return (
    <motion.article
      whileHover={{ y: -3 }}
      transition={{ duration: 0.2 }}
      className="rounded-2xl bg-[#13131D] border border-[#232332] hover:border-[#3D3D58] transition-all flex flex-col justify-between overflow-hidden shadow-md group"
    >
      {/* Cover Image / Thumbnail */}
      <div className="relative h-44 sm:h-48 w-full bg-[#181824] overflow-hidden">
        {article.urlToImage && !imageError ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={article.urlToImage}
            alt={article.title}
            onError={() => setImageError(true)}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-[#1C1628] via-[#141420] to-[#101018] flex flex-col items-center justify-center gap-2 p-4 text-center">
            <div className="w-10 h-10 rounded-xl bg-pink-500/15 border border-pink-500/30 flex items-center justify-center text-pink-400">
              <Cpu className="w-5 h-5" />
            </div>
            <span className="text-[11px] font-semibold text-[#8E8E9F]">
              {article.source.name || "Tech Coverage"}
            </span>
          </div>
        )}

        {/* Source Badge */}
        <div className="absolute top-3 left-3 z-10">
          <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-black/75 backdrop-blur-md border border-white/15 text-pink-300 shadow-sm">
            {article.source.name || "Tech News"}
          </span>
        </div>

        {/* Timestamp */}
        <div className="absolute bottom-3 right-3 z-10">
          <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-black/70 backdrop-blur-sm text-neutral-300 flex items-center gap-1 border border-white/10">
            <Clock className="w-3 h-3 text-pink-400" />
            {formatTimeAgo(article.publishedAt)}
          </span>
        </div>
      </div>

      {/* Content Area */}
      <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between space-y-3">
        <div className="space-y-2">
          <h3 className="font-bold text-sm sm:text-base text-white group-hover:text-pink-300 transition-colors line-clamp-2 leading-snug">
            {article.title}
          </h3>

          <p className="text-xs text-[#8E8E9F] line-clamp-2 leading-relaxed">
            {article.description || "Click below to read the complete breakdown and engineering analysis of this story."}
          </p>
        </div>

        {/* Bottom CTA Row */}
        <div className="pt-2 border-t border-[#1C1C28] flex items-center justify-between">
          <span className="text-[11px] text-[#6A6A80] truncate max-w-[150px]">
            {article.author ? `By ${article.author}` : article.source.name}
          </span>

          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-pink-500/15 hover:bg-pink-500/25 border border-pink-500/30 text-pink-300 hover:text-white font-bold text-xs transition-all cursor-pointer group-hover:border-pink-500/60"
          >
            <span>Read Full Bit</span>
            <ArrowUpRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </a>
        </div>
      </div>
    </motion.article>
  );
}
