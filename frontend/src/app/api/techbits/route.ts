import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

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

const FALLBACK_ARTICLES: Record<string, NewsArticle[]> = {
  All: [
    {
      source: { id: "the-verge", name: "The Verge" },
      author: "Alex Heath",
      title: "OpenAI announces new multi-agent reasoning models for next-gen software",
      description: "OpenAI has officially launched a suite of next-generation reasoning architectures designed to dramatically enhance autonomous coding and complex problem solving.",
      url: "https://www.theverge.com/tech",
      urlToImage: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
      publishedAt: new Date(Date.now() - 1000 * 60 * 45).toISOString(),
      content: "OpenAI unveiled groundbreaking benchmarks on multi-agent frameworks..."
    },
    {
      source: { id: "techcrunch", name: "TechCrunch" },
      author: "Frederic Lardinois",
      title: "Google debuts enhanced Gemini Cloud toolchains for enterprise developers",
      description: "Google Cloud is expanding developer capabilities with direct integrations for agentic workflows, distributed vector storage, and automated latency optimizations.",
      url: "https://techcrunch.com/category/enterprise/",
      urlToImage: "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=1200&q=80",
      publishedAt: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
      content: "At its latest cloud summit, Google demonstrated enterprise latency reductions..."
    },
    {
      source: { id: "wired", name: "Wired" },
      author: "Will Knight",
      title: "NVIDIA scales Blackwell architecture into hyper-dense datacenter clusters",
      description: "NVIDIA's next wave of ultra-dense AI supercomputing racks is rolling out across premier cloud infrastructure partners worldwide with 4x energy efficiency gains.",
      url: "https://www.wired.com/category/gear/",
      urlToImage: "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=1200&q=80",
      publishedAt: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
      content: "The race for compute efficiency has accelerated as NVIDIA delivers Blackwell nodes..."
    },
    {
      source: { id: "ars-technica", name: "Ars Technica" },
      author: "Benj Edwards",
      title: "Apple introduces on-device neural accelerators for upcoming Silicon hardware",
      description: "Apple silicon teams reveal new low-power neural matrix engines intended to process multi-modal generative queries locally with sub-millisecond responsiveness.",
      url: "https://arstechnica.com/gadgets/",
      urlToImage: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
      publishedAt: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
      content: "Apple's internal whitepaper documents a proprietary neural architecture designed for on-device privacy..."
    },
    {
      source: { id: "the-verge", name: "The Verge" },
      author: "Tom Warren",
      title: "Microsoft Copilot Studio expands custom orchestration capabilities for engineers",
      description: "Microsoft is giving engineering teams native SDK support to wire complex multi-step API actions directly into enterprise workflow pipelines.",
      url: "https://www.theverge.com/microsoft",
      urlToImage: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80",
      publishedAt: new Date(Date.now() - 1000 * 60 * 480).toISOString(),
      content: "Microsoft announced a significant expansion to Copilot developer tooling today..."
    }
  ]
};

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const searchKeyword = searchParams.get("q")?.trim() || "";
    const company = searchParams.get("company")?.trim() || "All";
    const page = searchParams.get("page") || "1";
    const pageSize = searchParams.get("pageSize") || "24";

    const apiKey =
      process.env.NEWS_API_KEY ||
      process.env.NEXT_PUBLIC_NEWS_API_KEY ||
      "b65681a5bb0d42778772d44a29c2b0c4";

    // Build targeted query
    let query = "";
    if (company && company !== "All") {
      if (searchKeyword) {
        query = `${company} AND (${searchKeyword})`;
      } else {
        query = company;
      }
    } else {
      query = searchKeyword || "technology OR AI OR software OR semiconductor";
    }

    const domains = "techcrunch.com,theverge.com,wired.com,arstechnica.com";
    const url = `https://newsapi.org/v2/everything?q=${encodeURIComponent(
      query
    )}&domains=${domains}&language=en&sortBy=publishedAt&pageSize=${pageSize}&page=${page}`;

    const res = await fetch(url, {
      headers: {
        "X-Api-Key": apiKey,
        "User-Agent": "CareerForge-Techbits/1.0"
      },
      next: { revalidate: 300 } // Cache for 5 minutes
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.warn("NewsAPI response error:", res.status, errorData);

      // Return fallback gracefully so UI remains unbroken
      const fallbackList =
        FALLBACK_ARTICLES[company] || FALLBACK_ARTICLES["All"];
      return NextResponse.json({
        status: "ok",
        totalResults: fallbackList.length,
        articles: fallbackList,
        isFallback: true
      });
    }

    const data = await res.json();

    // Filter out [Removed] spam from NewsAPI
    const validArticles: NewsArticle[] = (data.articles || []).filter(
      (a: NewsArticle) =>
        a &&
        a.title &&
        a.title !== "[Removed]" &&
        !a.title.includes("Yahoo") &&
        a.url
    );

    // If zero articles found from specific niche query, but company was selected
    if (validArticles.length === 0 && company !== "All") {
      const fallback = (FALLBACK_ARTICLES["All"] || []).filter(
        (a) =>
          a.title.toLowerCase().includes(company.toLowerCase()) ||
          (a.description &&
            a.description.toLowerCase().includes(company.toLowerCase()))
      );
      if (fallback.length > 0) {
        return NextResponse.json({
          status: "ok",
          totalResults: fallback.length,
          articles: fallback,
          isFallback: true
        });
      }
    }

    return NextResponse.json({
      status: "ok",
      totalResults: data.totalResults ?? validArticles.length,
      articles: validArticles,
      isFallback: false
    });
  } catch (error: any) {
    console.error("Techbits Route Error:", error);
    return NextResponse.json(
      {
        status: "ok",
        totalResults: FALLBACK_ARTICLES["All"].length,
        articles: FALLBACK_ARTICLES["All"],
        isFallback: true
      },
      { status: 200 }
    );
  }
}
