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

const COMPANY_QUERIES: Record<string, string> = {
  Google: '"Google"',
  NVIDIA: '"NVIDIA"',
  Apple: '"Apple" AND (tech OR iPhone OR Mac OR iOS OR AI)',
  Microsoft: '"Microsoft"',
  OpenAI: '"OpenAI" OR "ChatGPT"'
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

    // 1. Strict Company Queries with mandatory keyword matching
    let query = "";
    if (company && company !== "All") {
      const baseCompanyQuery = COMPANY_QUERIES[company] || `"${company}"`;
      if (searchKeyword) {
        query = `(${baseCompanyQuery}) AND (${searchKeyword})`;
      } else {
        query = baseCompanyQuery;
      }
    } else {
      query = searchKeyword || "technology OR AI OR software OR hardware";
    }

    // 2. Limit domains to quality technology publications & restrict search to title,description
    const domains = "techcrunch.com,theverge.com,wired.com,arstechnica.com";
    const url = `https://newsapi.org/v2/everything?q=${encodeURIComponent(
      query
    )}&searchIn=title,description&domains=${domains}&language=en&sortBy=publishedAt&pageSize=${pageSize}&page=${page}`;

    const res = await fetch(url, {
      headers: {
        "X-Api-Key": apiKey,
        "User-Agent": "CareerForge-Techbits/1.0"
      },
      cache: "no-store" // Strict live real-data fetching
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      console.error("NewsAPI response error:", res.status, errorData);
      return NextResponse.json(
        {
          status: "error",
          message: errorData.message || "Failed to fetch live tech news from NewsAPI",
          articles: []
        },
        { status: res.status }
      );
    }

    const data = await res.json();

    // 3. Filter out [Removed] and invalid spam from NewsAPI
    let validArticles: NewsArticle[] = (data.articles || []).filter(
      (a: NewsArticle) =>
        a &&
        a.title &&
        a.title !== "[Removed]" &&
        !a.title.includes("Yahoo") &&
        a.url
    );

    // 4. Server-Side Strict Headline/Description Match for selected company
    if (company && company !== "All") {
      const compLower = company.toLowerCase();
      validArticles = validArticles.filter((article) => {
        const title = (article.title || "").toLowerCase();
        const desc = (article.description || "").toLowerCase();
        if (compLower === "openai") {
          return (
            title.includes("openai") ||
            desc.includes("openai") ||
            title.includes("chatgpt") ||
            desc.includes("chatgpt")
          );
        }
        return title.includes(compLower) || desc.includes(compLower);
      });
    }

    return NextResponse.json({
      status: "ok",
      totalResults: validArticles.length,
      articles: validArticles
    });
  } catch (error: any) {
    console.error("Techbits Route Exception:", error);
    return NextResponse.json(
      {
        status: "error",
        message: error.message || "Network error contacting NewsAPI",
        articles: []
      },
      { status: 500 }
    );
  }
}
