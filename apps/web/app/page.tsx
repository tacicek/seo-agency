"use client";

import { useEffect, useMemo, useState } from "react";

interface MozBacklink {
  source_url: string;
  source_title?: string;
  target_url?: string;
  anchor_text?: string;
  domain_authority?: number;
  page_authority?: number;
  spam_score?: number;
  first_seen?: string;
  last_seen?: string;
  link_flags?: string[];
}

interface AnalysisResult {
  reportId: string;
  report: {
    url: string;
    onpage: any;
    keywords: any;
    performance: any;
    moz: {
      backlink_metrics?: any;
      link_quality?: any;
      backlinks?: MozBacklink[];
      backlinks_overview?: {
        total_results?: number;
        limit?: number;
      } | null;
      backlinks_error?: { error?: string; message?: string } | null;
      full_metrics?: any;
    };
    content_quality?: any;
    seo_prediction?: any;
    ai_insights?: any;
    comprehensive_score?: any;
  };
}

const toRecord = (value: unknown): Record<string, any> | null =>
  value !== null && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, any>) : null;

const trustSignals = [
  { label: "Screaming Frog", value: "Enterprise Crawl Automation" },
  { label: "SerpAPI", value: "Realtime SERP Intelligence" },
  { label: "Supabase", value: "Analytics Warehouse" },
];

const aiProviders = [
  "OpenAI GPT-4o",
  "Google Gemini 2.0 Flash",
  "Anthropic Claude 3.7 Sonnet",
  "Mistral Large (latest)",
];

const navItems = [
  { id: "overview", label: "Genel Bakış" },
  { id: "analysis", label: "Analiz Motoru" },
  { id: "metrics", label: "Moz Metrikleri" },
  { id: "backlinks", label: "Backlink Profili" },
  { id: "onpage", label: "On-Page SEO" },
  { id: "keywords", label: "Anahtar Kelimeler" },
  { id: "comprehensive-score", label: "Kompozit Skor" },
  { id: "content-quality", label: "İçerik Kalitesi" },
  { id: "ai-insights", label: "AI Insights" },
  { id: "content-generator", label: "Content Generator" },
  { id: "seo-prediction", label: "SEO Tahmini" },
  { id: "report-meta", label: "Rapor Özeti" },
];

export default function Page() {
  const [url, setUrl] = useState("https://example.com");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<string>(navItems[0].id);

  // Content Generator States
  const [contentLoading, setContentLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<string>("");
  const [contentError, setContentError] = useState<string | null>(null);
  const [contentForm, setContentForm] = useState({
    topic: "",
    pageType: "SERVICE",
    mainKeyword: "",
    secondaryKeywords: "",
    targetLocation: "",
    targetAudience: "",
    language: "Turkish",
    tone: "professional but friendly",
    wordCount: 1200,
    competitorUrls: "",
    localContext: "",
    provider: "openai",
    model: "", // Specific model selection
  });

  const availableNavItems = useMemo(() => (result ? navItems : navItems.slice(0, 2)), [result]);

  useEffect(() => {
    const items = availableNavItems.length > 0 ? availableNavItems : [navItems[0]];

    const handleScroll = () => {
      let currentId = items[0]?.id ?? navItems[0].id;
      const offset = 160;

      for (const item of items) {
        const element = document.getElementById(item.id);
        if (!element) continue;
        const rect = element.getBoundingClientRect();
        if (rect.top - offset <= 0) {
          currentId = item.id;
        }
      }

      setActiveSection((prev) => (prev !== currentId ? currentId : prev));
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [availableNavItems]);

  const analyze = async () => {
    setLoading(true);
    setResult(null);
    setError(null);

    if (!url || url.trim() === "") {
      setError("Please enter a URL");
      setLoading(false);
      return;
    }

    try {
      new URL(url);
    } catch {
      setError("Please enter a valid URL (e.g., https://example.com)");
      setLoading(false);
      return;
    }

    try {
  // Use relative /api to go through Next.js rewrite to FastAPI service
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";
  const res = await fetch(`${base}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: "Analysis failed" }));

        if (Array.isArray(errorData.detail)) {
          const validationErrors = errorData.detail.map((err: any) => err.msg).join(", ");
          throw new Error(`Validation error: ${validationErrors}`);
        }

        throw new Error(errorData.detail || `HTTP ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Analysis error:", err);
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const generateContent = async () => {
    setContentLoading(true);
    setGeneratedContent("");
    setContentError(null);

    if (!contentForm.topic || !contentForm.mainKeyword) {
      setContentError("Topic and Main Keyword are required");
      setContentLoading(false);
      return;
    }

    try {
  // Use relative /api to go through Next.js rewrite to FastAPI service
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";
  const res = await fetch(`${base}/ai/generate-content`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: contentForm.topic,
          page_type: contentForm.pageType,
          main_keyword: contentForm.mainKeyword,
          secondary_keywords: contentForm.secondaryKeywords
            .split(",")
            .map((k) => k.trim())
            .filter((k) => k.length > 0),
          target_location: contentForm.targetLocation || undefined,
          target_audience: contentForm.targetAudience || undefined,
          language: contentForm.language,
          tone: contentForm.tone,
          word_count: contentForm.wordCount,
          competitor_urls: contentForm.competitorUrls
            .split(",")
            .map((u) => u.trim())
            .filter((u) => u.length > 0),
          local_context: contentForm.localContext || undefined,
          provider: contentForm.provider,
          model: contentForm.model || undefined,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: "Content generation failed" }));
        throw new Error(errorData.detail || `HTTP ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      setGeneratedContent(data.content || "");
    } catch (err) {
      console.error("Content generation error:", err);
      setContentError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setContentLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 60) return "text-amber-300";
    return "text-rose-400";
  };

  const report = toRecord(result?.report);
  const reportId = result?.reportId ?? "";
  const mozSection = toRecord(report?.moz);
  const mozMetrics = toRecord(mozSection?.backlink_metrics) ?? {};
  const linkQuality = toRecord(mozSection?.link_quality) ?? {};
  const mozTimestamp = toRecord(mozSection?.full_metrics)?.timestamp;
  const backlinks = Array.isArray(mozSection?.backlinks) ? (mozSection?.backlinks as MozBacklink[]) : [];
  const backlinksOverview = mozSection?.backlinks_overview ?? null;
  const backlinksError = mozSection?.backlinks_error ?? null;
  const spamScore = mozMetrics?.spam_score ?? 0;
  const mozRank = linkQuality?.mozrank ?? 0;
  const keywordTop = Array.isArray(report?.keywords?.top) ? report?.keywords?.top.slice(0, 10) : [];
  const seoKeywordsData = toRecord(report?.seo_keywords);
  const seoKeywords = Array.isArray(seoKeywordsData?.seo_keywords) ? seoKeywordsData.seo_keywords : [];
  const detectedTopic = seoKeywordsData?.detected_topic ?? null;
  const relatedSearches = Array.isArray(seoKeywordsData?.related_searches) ? seoKeywordsData.related_searches : [];
  const onpage = toRecord(report?.onpage) ?? {};
  const keywords = toRecord(report?.keywords) ?? {};
  const contentQuality = toRecord(report?.content_quality);
  const comprehensiveScore = toRecord(report?.comprehensive_score);
  const seoPrediction = toRecord(report?.seo_prediction);
  const aiData = toRecord(report?.ai_insights);
  const aiInsights = toRecord(aiData?.insights) ?? {};
  const strengths: string[] = Array.isArray(aiInsights.strengths) ? aiInsights.strengths : [];
  const weaknesses: string[] = Array.isArray(aiInsights.weaknesses) ? aiInsights.weaknesses : [];
  const opportunities: string[] = Array.isArray(aiInsights.opportunities) ? aiInsights.opportunities : [];
  const threats: string[] = Array.isArray(aiInsights.threats) ? aiInsights.threats : [];
  const actionItems: string[] = Array.isArray(aiInsights.action_items) ? aiInsights.action_items : [];
  const totalActionItems = aiData?.total_action_items ?? actionItems.length;
  const priorityScore = aiData?.priority_score ?? 0;
  const aiSummary = aiData?.summary ?? "";
  const seoRecommendations = Array.isArray(seoPrediction?.recommendations) ? seoPrediction.recommendations : [];
  const comprehensiveScoreBreakdown =
    comprehensiveScore && typeof comprehensiveScore.score_breakdown === "object" && comprehensiveScore.score_breakdown !== null
      ? comprehensiveScore.score_breakdown
      : {};

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="relative isolate overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,_#3b82f630,_transparent_45%),radial-gradient(circle_at_bottom,_#9333ea30,_transparent_40%)]" />

        <section id="overview" className="px-6 pt-16 pb-24 sm:pt-24 lg:pt-32">
          <div className="mx-auto max-w-6xl">
            <div className="mx-auto max-w-3xl space-y-6 text-center">
              <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1 text-sm text-slate-200 backdrop-blur">
                <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
                AI destekli SEO command center
              </span>
              <h1 className="text-4xl font-black tracking-tight sm:text-5xl lg:text-6xl">
                Tek ekranda crawler verileri, SERP skoru ve GPT-5 içgörüleriyle
                <span className="bg-gradient-to-r from-sky-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent"> SEO yönetimi</span>.
              </h1>
              <p className="text-lg text-slate-300 opacity-90">
                Screaming Frog otomasyonu, SerpAPI rank tracking, Supabase raporlama ve üçlü yapay zeka orkestrasyonu (GPT-5, Gemini, Claude 4.5 Sonnet) tek platformda birleşiyor.
              </p>

              <div className="mt-10 grid gap-4 sm:grid-cols-3">
                {[
                  { label: "4.2B", hint: "Sayfa tarama kapasitesi" },
                  { label: "3× AI", hint: "OpenAI · Gemini · Claude" },
                  { label: "< 60 sn", hint: "Canlı SERP + backlink denetimi" },
                ].map(({ label, hint }) => (
                  <div key={hint} className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                    <div className="text-3xl font-semibold text-slate-50">{label}</div>
                    <div className="mt-1 text-sm text-slate-300/90">{hint}</div>
                  </div>
                ))}
              </div>

              <div className="mt-10 flex flex-wrap items-center justify-center gap-3 text-sm text-slate-300/90">
                {trustSignals.map((item) => (
                  <div key={item.label} className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 backdrop-blur">
                    <span className="h-2 w-2 rounded-full bg-emerald-400" />
                    <span className="font-semibold text-slate-100/90">{item.label}</span>
                    <span className="text-slate-300/70">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <div className="px-6 pb-24">
          <div className="mx-auto flex max-w-6xl flex-col gap-10 lg:flex-row">
            <aside className="lg:w-64 lg:flex-shrink-0">
              <div className="sticky top-28 space-y-6">
                <div className="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                  <div className="text-xs uppercase tracking-[0.3em] text-slate-300/70">Kontrol Paneli</div>
                  <div className="mt-2 text-lg font-semibold text-slate-100">SEO Analyzer</div>
                  <p className="mt-2 text-sm text-slate-300/70">
                    Screaming Frog • SerpAPI • Supabase • GPT-5 orkestrasyonu ile Ahrefs tarzı görünüm.
                  </p>

                  {result && (
                    <div className="mt-4 grid grid-cols-2 gap-3 text-xs text-slate-300/80">
                      <div>
                        <div className="text-slate-400">DA</div>
                        <div className="text-base font-semibold text-slate-100">
                          {result.report.moz?.backlink_metrics?.domain_authority ?? "—"}
                        </div>
                      </div>
                      <div>
                        <div className="text-slate-400">PA</div>
                        <div className="text-base font-semibold text-slate-100">
                          {result.report.moz?.backlink_metrics?.page_authority ?? "—"}
                        </div>
                      </div>
                      <div>
                        <div className="text-slate-400">Spam</div>
                        <div className={`text-base font-semibold ${getScoreColor(result.report.moz?.backlink_metrics?.spam_score ?? 0)}`}>
                          {result.report.moz?.backlink_metrics?.spam_score ?? "—"}%
                        </div>
                      </div>
                      <div>
                        <div className="text-slate-400">SEO</div>
                        <div className={`text-base font-semibold ${getScoreColor(result.report.moz?.backlink_metrics?.seo_score ?? 0)}`}>
                          {result.report.moz?.backlink_metrics?.seo_score ?? "—"}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <nav className="rounded-3xl border border-white/10 bg-white/5 p-3 backdrop-blur">
                  <ul className="space-y-1">
                    {availableNavItems.map((item) => (
                      <li key={item.id}>
                        <a
                          href={`#${item.id}`}
                          className={`flex items-center justify-between rounded-2xl px-3 py-2 text-sm transition ${
                            activeSection === item.id
                              ? "bg-emerald-400 text-slate-950 shadow-lg"
                              : "text-slate-300 hover:bg-white/5 hover:text-slate-100"
                          }`}
                        >
                          <span className="font-medium">{item.label}</span>
                          <span
                            className={`h-2 w-2 rounded-full ${
                              activeSection === item.id ? "bg-slate-900" : "bg-slate-600"
                            }`}
                          />
                        </a>
                      </li>
                    ))}
                  </ul>
                </nav>
              </div>
            </aside>

            <div className="flex-1 space-y-16">
              <section id="analysis">
                <div className="flex flex-col gap-6 lg:flex-row">
                  <div className="flex-1 space-y-6 rounded-3xl border border-white/10 bg-slate-900/70 p-8 shadow-2xl backdrop-blur">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <div className="text-sm uppercase tracking-[0.3em] text-slate-400">Analiz başlat</div>
                        <h2 className="mt-2 text-3xl font-semibold">URL taraması ve raporlama</h2>
                      </div>
                      <div className="hidden items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300 sm:flex">
                        <span className="h-2 w-2 animate-ping rounded-full bg-emerald-300" />
                        Canlı bağlantı
                      </div>
                    </div>

                    <p className="text-sm text-slate-300/80">
                      URL girin, platform Screaming Frog crawl verilerini, SerpAPI rank ölçümlerini ve MOZ backlink metriklerini anında çekip GPT-5 destekli aksiyon planına dönüştürsün.
                    </p>

                    <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 shadow-inner">
                      <div className="flex flex-col gap-4 md:flex-row">
                        <input
                          className="flex-1 rounded-xl border border-white/10 bg-slate-900/60 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-400/40"
                          placeholder="https://domain.com"
                          value={url}
                          onChange={(e) => setUrl(e.target.value)}
                        />
                        <button
                          className="flex items-center justify-center gap-2 rounded-xl bg-emerald-400 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:bg-slate-600 disabled:text-slate-300"
                          onClick={analyze}
                          disabled={loading}
                        >
                          {loading ? (
                            <>
                              <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                              </svg>
                              Analiz ediliyor…
                            </>
                          ) : (
                            <>
                              <span>Analizi başlat</span>
                              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                <path d="M5 12h14" />
                                <path d="M12 5l7 7-7 7" />
                              </svg>
                            </>
                          )}
                        </button>
                      </div>
                    </div>

                    <div className="grid gap-4 sm:grid-cols-3">
                      {[
                        { title: "Saniyeler içinde sonuç", desc: "Supabase rapor kaydı ve PDF aktarımına hazır çıktı", icon: "⚡️" },
                        { title: "Rakip analizi", desc: "SerpAPI + GPT önerileriyle pazar payı analizi", icon: "🧭" },
                        { title: "Tam entegrasyon", desc: "n8n workflow & CLI otomasyonu", icon: "🔗" },
                      ].map(({ title, desc, icon }) => (
                        <div key={title} className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                          <div className="mb-2 text-xl">{icon}</div>
                          <div className="text-sm font-semibold text-slate-100/90">{title}</div>
                          <div className="text-xs text-slate-300/80">{desc}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex w-full max-w-md flex-col justify-between gap-6 rounded-3xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur">
                    <div className="space-y-3">
                      <h3 className="text-lg font-semibold text-slate-100/90">Desteklenen yapay zeka motorları</h3>
                      <p className="text-sm text-slate-300/80">
                        Analiz motoru, provider çakışmalarında otomatik fallback uygular. Her öneri GPT-5 ana modeli ile başlar; Claude 4.5 Sonnet ve Gemini replik destek sağlar.
                      </p>
                    </div>

                    <ul className="space-y-3 text-sm text-slate-200">
                      {aiProviders.map((provider) => (
                        <li key={provider} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-400/20 text-emerald-300">✓</span>
                          <div className="flex-1">
                            <div className="font-semibold">{provider}</div>
                            <div className="text-xs text-slate-300/70">Realtime prompt orkestrasyonu</div>
                          </div>
                        </li>
                      ))}
                    </ul>

                    <div className="rounded-2xl border border-emerald-400/30 bg-emerald-500/10 p-4 text-xs text-emerald-200">
                      <div className="font-semibold text-emerald-100">Başlama ipucu</div>
                      <p className="mt-1">
                        İlk analizi demo URL ile tetikleyin, ardından `.env` dosyasında tanımlı API anahtarlarınızla rakip domain’leri kıyaslayın.
                      </p>
                    </div>
                  </div>
                </div>
              </section>

              {error && (
                <section aria-live="polite">
                  <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-5 text-sm text-rose-200 shadow-xl">
                    <strong className="font-semibold">Hata:</strong> {error}
                  </div>
                </section>
              )}

              {result ? (
                <>
                  <section id="metrics" className="space-y-6">
                    <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-xl">
                      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                          <div className="text-xs uppercase tracking-[0.3em] text-slate-400">Moz Snapshot</div>
                          <h2 className="text-xl font-semibold text-slate-100">Backlink & Authority Skorları</h2>
                        </div>
                        <div className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">
                          Son Güncelleme:{" "}
                          <span className="font-semibold text-slate-100">
                            {mozTimestamp ? new Date(mozTimestamp * 1000).toLocaleString() : "Canlı"}
                          </span>
                        </div>
                      </div>

                      <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
                        {[
                          {
                            label: "Domain Authority",
                            value: mozMetrics.domain_authority,
                            hint: "Moz Metric",
                            border: "border-sky-400/60",
                          },
                          {
                            label: "Page Authority",
                            value: mozMetrics.page_authority,
                            hint: "Moz Metric",
                            border: "border-emerald-400/60",
                          },
                          {
                            label: "Spam Score",
                            value: spamScore,
                            hint: "Lower is better",
                            border: "border-amber-400/60",
                            isSpam: true,
                          },
                          {
                            label: "SEO Score",
                            value: mozMetrics.seo_score,
                            hint: "Overall Rating",
                            border: "border-fuchsia-400/60",
                          },
                        ].map(({ label, value, hint, border, isSpam }) => {
                          const numericValue = typeof value === "number" ? value : undefined;
                          const colorClass = isSpam
                            ? spamScore <= 10
                              ? "text-emerald-400"
                              : "text-rose-400"
                            : getScoreColor(numericValue ?? 0);
                          const displayValue = isSpam ? `${spamScore}%` : numericValue ?? "N/A";

                          return (
                            <div key={label} className={`rounded-2xl border ${border} bg-slate-900/70 p-6 shadow-lg`}>
                              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</div>
                              <div className={`mt-3 text-4xl font-semibold ${colorClass}`}>{displayValue}</div>
                              <div className="mt-2 text-xs text-slate-400">{hint}</div>
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    <div className="grid gap-6 lg:grid-cols-3">
                      <div className="rounded-3xl border border-sky-400/30 bg-sky-500/10 p-6 shadow-xl">
                        <h3 className="text-lg font-semibold text-slate-100">Root Domains Linking</h3>
                        <p className="mt-1 text-sm text-slate-300/80">Moz backlink metrics</p>
                        <div className="mt-4 text-4xl font-semibold text-sky-100">{mozMetrics.root_domains_linking?.toLocaleString() ?? 0}</div>
                      </div>
                      <div className="rounded-3xl border border-emerald-400/30 bg-emerald-500/10 p-6 shadow-xl">
                        <h3 className="text-lg font-semibold text-slate-100">External Links</h3>
                        <p className="mt-1 text-sm text-slate-300/80">Giden bağlantı hacmi</p>
                        <div className="mt-4 text-4xl font-semibold text-emerald-100">{mozMetrics.external_links?.toLocaleString() ?? 0}</div>
                      </div>
                      <div className="rounded-3xl border border-fuchsia-400/30 bg-fuchsia-500/10 p-6 shadow-xl">
                        <h3 className="text-lg font-semibold text-slate-100">Link Quality</h3>
                        <p className="mt-1 text-sm text-slate-300/80">MozRank tabanlı kalite</p>
                        <div className="mt-4 text-4xl font-semibold text-fuchsia-100">{(mozRank * 10).toFixed(0)}/100</div>
                      </div>
                    </div>
                  </section>

                  <section id="backlinks" className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-xl">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <div>
                        <h2 className="text-xl font-semibold text-slate-100">Backlink Profili</h2>
                        <p className="text-sm text-slate-300/80">Moz Link Explorer sonuçlarından ilk {backlinks.length || 0} bağlantı</p>
                      </div>
                      {backlinksOverview?.total_results !== undefined && (
                        <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200">
                          <span className="font-semibold text-slate-100/90">Toplam:</span>
                          <span>{backlinksOverview.total_results?.toLocaleString() ?? "-"}</span>
                        </div>
                      )}
                    </div>

                    {backlinksError ? (
                      <div className="mt-4 rounded-2xl border border-amber-400/40 bg-amber-500/10 p-4 text-sm text-amber-200">
                        <div className="font-semibold text-amber-100">Backlink verisi alınamadı</div>
                        <div className="text-xs text-amber-100/80">{backlinksError.message || backlinksError.error || "MOZ API yanıtı alınamadı."}</div>
                      </div>
                    ) : backlinks.length > 0 ? (
                      <div className="mt-6 overflow-hidden rounded-2xl border border-white/10">
                        <table className="min-w-full divide-y divide-white/5 text-sm">
                          <thead className="bg-white/5 text-xs uppercase tracking-wider text-slate-200">
                            <tr>
                              <th className="px-4 py-3 text-left font-semibold">Kaynak Sayfa</th>
                              <th className="px-4 py-3 text-left font-semibold">Anchor</th>
                              <th className="px-4 py-3 text-right font-semibold">DA</th>
                              <th className="px-4 py-3 text-right font-semibold">PA</th>
                              <th className="px-4 py-3 text-right font-semibold">Spam</th>
                              <th className="px-4 py-3 text-right font-semibold">İlk Görülme</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-white/5 text-sm">
                            {backlinks.map((link, idx) => (
                              <tr key={`${link.source_url}-${idx}`} className="hover:bg-white/5">
                                <td className="px-4 py-3 align-top">
                                  <div className="max-w-xs truncate text-slate-100">
                                    <a href={link.source_url} target="_blank" rel="noopener noreferrer" className="underline decoration-dotted underline-offset-4">
                                      {link.source_title || link.source_url}
                                    </a>
                                  </div>
                                </td>
                                <td className="px-4 py-3 align-top text-slate-300/90">
                                  {link.anchor_text ? (
                                    <span className="line-clamp-2 text-xs text-slate-200/80">{link.anchor_text}</span>
                                  ) : (
                                    <span className="text-xs text-slate-500">(No anchor)</span>
                                  )}
                                </td>
                                <td className="px-4 py-3 text-right font-semibold text-slate-200">
                                  {link.domain_authority ?? "-"}
                                </td>
                                <td className="px-4 py-3 text-right text-slate-200">
                                  {link.page_authority ?? "-"}
                                </td>
                                <td className={`px-4 py-3 text-right ${link.spam_score !== undefined && link.spam_score >= 30 ? "text-rose-300" : "text-slate-200"}`}>
                                  {link.spam_score !== undefined ? `${link.spam_score}%` : "-"}
                                </td>
                                <td className="px-4 py-3 text-right text-slate-400">
                                  {link.first_seen ? new Date(link.first_seen).toLocaleDateString() : "-"}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <div className="mt-5 rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300/80">
                        Bu URL için paylaşılabilir backlink bulunamadı.
                      </div>
                    )}
                  </section>

                  <section id="onpage" className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-xl">
                    <div className="flex items-center justify-between">
                      <h2 className="text-xl font-semibold text-slate-100">On-Page SEO</h2>
                      <div className="text-xs text-slate-400">Tarama özeti</div>
                    </div>

                    <div className="mt-5 grid gap-5 lg:grid-cols-3">
                      <div className="space-y-4 lg:col-span-2">
                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <div className="flex items-center justify-between text-sm">
                            <span className="font-semibold text-slate-100/90">Title Tag</span>
                            <span className={`rounded-full px-3 py-1 text-xs font-semibold ${onpage?.title ? "bg-emerald-500/10 text-emerald-300" : "bg-rose-500/10 text-rose-300"}`}>
                              {onpage?.title ? "✓ Found" : "✗ Missing"}
                            </span>
                          </div>
                          <p className="mt-2 text-sm text-slate-200/80">{onpage?.title || "No title tag found"}</p>
                          <p className="mt-1 text-xs text-slate-400">Length: {onpage?.title?.length ?? 0} characters</p>
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <div className="flex items-center justify-between text-sm">
                            <span className="font-semibold text-slate-100/90">Meta Description</span>
                            <span className={`rounded-full px-3 py-1 text-xs font-semibold ${onpage?.meta_description ? "bg-emerald-500/10 text-emerald-300" : "bg-rose-500/10 text-rose-300"}`}>
                              {onpage?.meta_description ? "✓ Found" : "✗ Missing"}
                            </span>
                          </div>
                          <p className="mt-2 text-sm text-slate-200/80">{onpage?.meta_description || "No meta description found"}</p>
                          <p className="mt-1 text-xs text-slate-400">Length: {onpage?.meta_description?.length ?? 0} characters</p>
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <div className="font-semibold text-slate-100/90">Heading Structure</div>
                          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
                            {["h1", "h2", "h3", "h4", "h5", "h6"].map((tag) => {
                              const count = (onpage?.headings?.[tag] ?? []).length;
                              return (
                                <div key={tag} className="rounded-xl border border-white/10 bg-slate-950/40 p-3 text-center">
                                  <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{tag}</div>
                                  <div className="mt-1 text-xl font-semibold text-slate-100">{count}</div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div className="rounded-2xl border border-sky-400/30 bg-sky-500/10 p-4">
                          <div className="text-sm text-slate-100/90">Total Images</div>
                          <div className="text-3xl font-semibold text-sky-200">{onpage?.images?.length ?? 0}</div>
                        </div>
                        <div className="rounded-2xl border border-emerald-400/30 bg-emerald-500/10 p-4">
                          <div className="text-sm text-slate-100/90">Total Links</div>
                          <div className="text-3xl font-semibold text-emerald-200">{onpage?.links?.length ?? 0}</div>
                        </div>
                      </div>
                    </div>
                  </section>

                  <section id="keywords" className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-xl">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                      <div>
                        <h2 className="text-xl font-semibold text-slate-100">SEO Keywords (SERP-Enhanced)</h2>
                        <p className="mt-1 text-sm text-slate-300/80">
                          Relevante Keywords basierend auf Thema, SERP-Daten und Seiteninhalt
                        </p>
                        {detectedTopic && (
                          <div className="mt-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
                            <span className="h-2 w-2 rounded-full bg-emerald-400" />
                            Thema erkannt: {detectedTopic}
                          </div>
                        )}
                      </div>
                      <div className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">
                        Total Words: <span className="font-semibold text-slate-100">{keywords?.total_words ?? 0}</span>
                      </div>
                    </div>

                    {seoKeywords.length > 0 ? (
                      <>
                        <div className="mt-5 overflow-hidden rounded-2xl border border-white/10">
                          <table className="min-w-full divide-y divide-white/5 text-sm">
                            <thead className="bg-white/5">
                              <tr>
                                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-200">Rank</th>
                                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-200">Keyword</th>
                                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-200">Relevanz</th>
                                <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-200">Vorkommen</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                              {seoKeywords.slice(0, 10).map((kw: any, idx: number) => (
                                <tr key={`${kw.keyword}-${idx}`} className="hover:bg-white/5">
                                  <td className="px-4 py-3 font-semibold text-slate-400">#{idx + 1}</td>
                                  <td className="px-4 py-3 font-medium text-slate-100">
                                    {kw.keyword}
                                    {kw.keyword === detectedTopic && (
                                      <span className="ml-2 rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] font-semibold text-emerald-300">
                                        HAUPT
                                      </span>
                                    )}
                                  </td>
                                  <td className="px-4 py-3 text-right">
                                    <span className={`rounded-full px-2 py-1 text-xs font-semibold ${
                                      kw.relevance_score >= 10 
                                        ? "bg-emerald-500/10 text-emerald-200" 
                                        : kw.relevance_score >= 5 
                                        ? "bg-sky-500/10 text-sky-200" 
                                        : "bg-slate-500/10 text-slate-300"
                                    }`}>
                                      {kw.relevance_score}
                                    </span>
                                  </td>
                                  <td className="px-4 py-3 text-right text-slate-300">{kw.count_on_page}×</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>

                        {relatedSearches.length > 0 && (
                          <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 p-4">
                            <div className="text-sm font-semibold text-slate-100">Verwandte Suchanfragen (Google SERP)</div>
                            <div className="mt-3 flex flex-wrap gap-2">
                              {relatedSearches.slice(0, 8).map((search: string, idx: number) => (
                                <span
                                  key={`${search}-${idx}`}
                                  className="rounded-full border border-white/10 bg-slate-900/60 px-3 py-1 text-xs text-slate-200"
                                >
                                  {search}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300/80">
                        SEO-Keywords konnten nicht analysiert werden. Möglicherweise fehlt SerpAPI-Zugriff oder der Inhalt ist zu kurz.
                      </div>
                    )}
                  </section>

                  <section id="comprehensive-score" className="rounded-3xl border border-indigo-400/30 bg-indigo-500/10 p-6 shadow-xl">
                    {comprehensiveScore ? (
                      <>
                        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                          <div className="space-y-2">
                            <h2 className="text-xl font-semibold text-slate-100">Comprehensive SEO Score</h2>
                            <p className="text-sm text-slate-300/80">Skorlar GPT-5, ML tahminleri ve MOZ metrikleriyle ağırlıklandırılır.</p>
                          </div>
                          <div className="rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-center">
                            <div className="text-xs uppercase tracking-[0.3em] text-slate-300/70">Overall Score</div>
                            <div className={`mt-2 text-5xl font-semibold ${getScoreColor(comprehensiveScore.overall_score)}`}>
                              {comprehensiveScore.overall_score}
                            </div>
                            <div className="mt-1 text-sm text-slate-300">Grade: {comprehensiveScore.grade}</div>
                            <div className="text-xs text-slate-400">{comprehensiveScore.percentile}</div>
                          </div>
                        </div>

                        <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                          {Object.entries(comprehensiveScoreBreakdown as Record<string, number>).map(([key, value]) => {
                            const numericValue = typeof value === "number" ? value : Number(value ?? 0);
                            return (
                              <div key={key} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <div className="text-xs uppercase tracking-[0.2em] text-slate-300/70">{key.replace(/_/g, " ")}</div>
                                <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-white/10">
                                  <div
                                    className={`h-2 rounded-full ${
                                      numericValue >= 80 ? "bg-emerald-400" : numericValue >= 60 ? "bg-amber-300" : "bg-rose-400"
                                    }`}
                                    style={{ width: `${numericValue}%` }}
                                  />
                                </div>
                                <div className={`mt-3 text-2xl font-semibold ${getScoreColor(numericValue)}`}>{numericValue}</div>
                              </div>
                            );
                          })}
                        </div>
                      </>
                    ) : (
                      <p className="text-sm text-slate-300/80">Bu analizde kompozit skor verisi bulunamadı.</p>
                    )}
                  </section>

                  <section id="content-quality" className="rounded-3xl border border-emerald-400/30 bg-emerald-500/10 p-6 shadow-xl">
                    <h2 className="text-xl font-semibold text-slate-100">Content Quality Analysis</h2>
                    {contentQuality ? (
                      <>
                        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                          {[
                            { label: "Total Words", value: contentQuality.total_words },
                            { label: "Unique Words", value: contentQuality.unique_words },
                            { label: "Avg Word Length", value: contentQuality.avg_word_length },
                            { label: "Diversity", value: `${contentQuality.diversity_score}%` },
                          ].map((item) => (
                            <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                              <div className="text-xs uppercase tracking-[0.2em] text-slate-300/70">{item.label}</div>
                              <div className="mt-2 text-2xl font-semibold text-slate-100">{item.value}</div>
                            </div>
                          ))}
                        </div>

                        <div className="mt-5 rounded-2xl border border-white/10 bg-white/5 p-4">
                          <div className="flex items-center justify-between">
                            <div>
                              <div className="text-sm font-semibold text-slate-100">Readability Assessment</div>
                              <div className="text-xs text-slate-300/70">Flesch Reading Ease</div>
                            </div>
                            <div className="text-right">
                              <div className="text-3xl font-semibold text-sky-200">{contentQuality.readability_score}</div>
                              <div className="text-xs text-slate-300">{contentQuality.readability_level}</div>
                            </div>
                          </div>
                        </div>
                      </>
                    ) : (
                      <p className="mt-4 text-sm text-slate-300/80">İçerik kalitesi metrikleri hesaplanamadı.</p>
                    )}
                  </section>

                  <section id="ai-insights" className="rounded-3xl border border-violet-400/30 bg-violet-500/10 p-6 shadow-xl">
                    {aiData ? (
                      <>
                        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                          <div>
                            <h2 className="text-xl font-semibold text-slate-100">AI-Powered Insights</h2>
                            <p className="text-sm text-slate-300/80">GPT-5 ana plan + Claude & Gemini destekli risk raporu</p>
                          </div>
                          <div className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">
                            <span>Priority Score</span>
                            <div className="flex items-center gap-2">
                              <div className="h-2 w-28 overflow-hidden rounded-full bg-white/10">
                                <div
                                  className={`h-2 rounded-full ${
                                    priorityScore >= 80 ? "bg-emerald-400" : priorityScore >= 60 ? "bg-amber-300" : "bg-rose-400"
                                  }`}
                                  style={{ width: `${priorityScore}%` }}
                                />
                              </div>
                              <span className="text-lg font-semibold text-slate-100">{priorityScore}</span>
                            </div>
                          </div>
                        </div>

                        <div className="mt-5 grid gap-4 lg:grid-cols-2">
                          <div className="space-y-4">
                            {aiSummary && (
                              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200">
                                <div className="font-semibold text-slate-100">Summary</div>
                                <p className="mt-2 text-slate-300/80">{aiSummary}</p>
                              </div>
                            )}

                            <div className="grid gap-3 sm:grid-cols-2">
                              {strengths.length > 0 && (
                                <div className="rounded-2xl border border-emerald-400/30 bg-emerald-500/10 p-4">
                                  <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-emerald-200">✅ Strengths</div>
                                  <ul className="space-y-1 text-xs text-slate-200">
                                    {strengths.map((item, idx) => (
                                      <li key={`${item}-${idx}`}>• {item}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {weaknesses.length > 0 && (
                                <div className="rounded-2xl border border-rose-400/30 bg-rose-500/10 p-4">
                                  <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-rose-200">⚠️ Weaknesses</div>
                                  <ul className="space-y-1 text-xs text-slate-200">
                                    {weaknesses.map((item, idx) => (
                                      <li key={`${item}-${idx}`}>• {item}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          </div>

                          <div className="space-y-4">
                            <div className="grid gap-3 sm:grid-cols-2">
                              {opportunities.length > 0 && (
                                <div className="rounded-2xl border border-amber-400/30 bg-amber-500/10 p-4 text-xs text-slate-200">
                                  <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-amber-200">💡 Opportunities</div>
                                  <ul className="space-y-1">
                                    {opportunities.map((item, idx) => (
                                      <li key={`${item}-${idx}`}>• {item}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {threats.length > 0 && (
                                <div className="rounded-2xl border border-orange-400/30 bg-orange-500/10 p-4 text-xs text-slate-200">
                                  <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-orange-200">🚨 Threats</div>
                                  <ul className="space-y-1">
                                    {threats.map((item, idx) => (
                                      <li key={`${item}-${idx}`}>• {item}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>

                            {actionItems.length > 0 && (
                              <div className="rounded-2xl border border-violet-400/40 bg-violet-500/20 p-4 text-xs text-slate-200">
                                <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-violet-200">
                                  🎯 Recommended Actions ({totalActionItems})
                                </div>
                                <ul className="space-y-2">
                                  {actionItems.map((item, idx) => (
                                    <li key={`${item}-${idx}`} className="flex items-start gap-3">
                                      <span className="mt-0.5 text-sm font-semibold text-violet-200">{idx + 1}.</span>
                                      <span className="flex-1 text-slate-100/80">{item}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        </div>
                      </>
                    ) : (
                      <p className="text-sm text-slate-300/80">Yapay zeka içgörüleri bu analiz için oluşturulmadı.</p>
                    )}
                  </section>

                  <section id="content-generator" className="rounded-3xl border border-cyan-400/30 bg-cyan-500/10 p-6 shadow-xl">
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                      <div>
                        <h2 className="text-xl font-semibold text-slate-100">AI Content Generator</h2>
                        <p className="text-sm text-slate-300/80">E-E-A-T optimized, topical & holistic SEO content - 100% human-like (2025 Models)</p>
                      </div>
                      <div className="flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-300">
                        <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-300" />
                        GPT-4o • Claude 3.7 • Gemini 2.0 • Mistral
                      </div>
                    </div>

                    <div className="mt-6 grid gap-6 lg:grid-cols-2">
                      {/* Form Column */}
                      <div className="space-y-4">
                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Topic *</label>
                          <input
                            type="text"
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="z.B. Umzug nach Zürich - Professionelle Umzugsfirma"
                            value={contentForm.topic}
                            onChange={(e) => setContentForm({ ...contentForm, topic: e.target.value })}
                          />
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">
                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <label className="block text-sm font-semibold text-slate-100">Page Type</label>
                            <select
                              className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                              value={contentForm.pageType}
                              onChange={(e) => setContentForm({ ...contentForm, pageType: e.target.value })}
                            >
                              <option value="SERVICE">Service Page</option>
                              <option value="BLOG">Blog Post</option>
                              <option value="LANDING PAGE">Landing Page</option>
                            </select>
                          </div>

                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <label className="block text-sm font-semibold text-slate-100">AI Provider</label>
                            <select
                              className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                              value={contentForm.provider}
                              onChange={(e) => setContentForm({ ...contentForm, provider: e.target.value, model: "" })}
                            >
                              <option value="openai">OpenAI</option>
                              <option value="anthropic">Anthropic</option>
                              <option value="gemini">Google Gemini</option>
                              <option value="mistral">Mistral</option>
                            </select>
                          </div>
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">
                            Model {contentForm.provider === "openai" && "(2025)"}
                            {contentForm.provider === "anthropic" && "(2025)"}
                            {contentForm.provider === "gemini" && "(2025)"}
                            {contentForm.provider === "mistral" && "(2025)"}
                          </label>
                          <select
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            value={contentForm.model}
                            onChange={(e) => setContentForm({ ...contentForm, model: e.target.value })}
                          >
                            {contentForm.provider === "openai" && (
                              <>
                                <option value="">gpt-5 (Default - Recommended)</option>
                                <option value="gpt-5">gpt-5 (Topical + E-E-A-T)</option>
                                <option value="gpt-4o">gpt-4o (Stable)</option>
                                <option value="gpt-4o-mini">gpt-4o-mini (Fast & Cost-Effective)</option>
                              </>
                            )}
                            {contentForm.provider === "anthropic" && (
                              <>
                                <option value="">claude-4.5-sonnet (Default - Recommended)</option>
                                <option value="claude-4.5-sonnet">claude-4.5-sonnet (Holistic + Structured)</option>
                                <option value="claude-3-7-sonnet-20250219">claude-3-7-sonnet-20250219 (Stable)</option>
                              </>
                            )}
                            {contentForm.provider === "gemini" && (
                              <>
                                <option value="">gemini-2.0-pro (Default - Recommended)</option>
                                <option value="gemini-2.0-pro">gemini-2.0-pro (Evidence-Grounded)</option>
                                <option value="gemini-2.0-flash-exp">gemini-2.0-flash-exp (Fast)</option>
                                <option value="gemini-1.5-pro">gemini-1.5-pro (Stable)</option>
                              </>
                            )}
                            {contentForm.provider === "mistral" && (
                              <>
                                <option value="">mistral-large-latest (Default - Recommended)</option>
                                <option value="mistral-large-latest">mistral-large-latest (Latest Flagship)</option>
                                <option value="mistral-small-latest">mistral-small-latest (Fast & Cost-Effective)</option>
                                <option value="open-mixtral-8x22b">open-mixtral-8x22b (Open)</option>
                              </>
                            )}
                          </select>
                          <p className="mt-1 text-xs text-slate-400">
                            {contentForm.provider === "openai" && "OpenAI'nin en güncel modelleri"}
                            {contentForm.provider === "anthropic" && "Anthropic'in en güncel Claude modelleri"}
                            {contentForm.provider === "gemini" && "Google'ın en güncel Gemini modelleri"}
                            {contentForm.provider === "mistral" && "Mistral'ın en güncel modelleri"}
                          </p>
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Main Keyword *</label>
                          <input
                            type="text"
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="umzug zürich"
                            value={contentForm.mainKeyword}
                            onChange={(e) => setContentForm({ ...contentForm, mainKeyword: e.target.value })}
                          />
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Secondary Keywords</label>
                          <input
                            type="text"
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="umzugsfirma zürich, möbeltransport (comma separated)"
                            value={contentForm.secondaryKeywords}
                            onChange={(e) => setContentForm({ ...contentForm, secondaryKeywords: e.target.value })}
                          />
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">
                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <label className="block text-sm font-semibold text-slate-100">Target Location</label>
                            <input
                              type="text"
                              className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                              placeholder="Zürich, Switzerland"
                              value={contentForm.targetLocation}
                              onChange={(e) => setContentForm({ ...contentForm, targetLocation: e.target.value })}
                            />
                          </div>

                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                            <label className="block text-sm font-semibold text-slate-100">Word Count</label>
                            <input
                              type="number"
                              className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                              placeholder="1200"
                              value={contentForm.wordCount}
                              onChange={(e) => setContentForm({ ...contentForm, wordCount: parseInt(e.target.value) || 1200 })}
                            />
                          </div>
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Target Audience</label>
                          <input
                            type="text"
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="Families and professionals moving to Zürich"
                            value={contentForm.targetAudience}
                            onChange={(e) => setContentForm({ ...contentForm, targetAudience: e.target.value })}
                          />
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Competitor URLs</label>
                          <input
                            type="text"
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="https://competitor1.ch, https://competitor2.ch"
                            value={contentForm.competitorUrls}
                            onChange={(e) => setContentForm({ ...contentForm, competitorUrls: e.target.value })}
                          />
                        </div>

                        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                          <label className="block text-sm font-semibold text-slate-100">Local Context</label>
                          <textarea
                            className="mt-2 w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-400 focus:border-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                            placeholder="Zürich city center, Limmat river, ETH Zürich area..."
                            rows={3}
                            value={contentForm.localContext}
                            onChange={(e) => setContentForm({ ...contentForm, localContext: e.target.value })}
                          />
                        </div>

                        <button
                          className="w-full rounded-xl bg-cyan-400 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-slate-600 disabled:text-slate-300"
                          onClick={generateContent}
                          disabled={contentLoading}
                        >
                          {contentLoading ? (
                            <span className="flex items-center justify-center gap-2">
                              <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                              </svg>
                              Generating Content...
                            </span>
                          ) : (
                            "Generate SEO Content"
                          )}
                        </button>
                      </div>

                      {/* Output Column */}
                      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                        <div className="mb-4 flex items-center justify-between">
                          <h3 className="text-sm font-semibold text-slate-100">Generated Content</h3>
                          {generatedContent && (
                            <button
                              className="rounded-lg border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200 hover:bg-white/10"
                              onClick={() => {
                                navigator.clipboard.writeText(generatedContent);
                                alert("Content copied to clipboard!");
                              }}
                            >
                              📋 Copy
                            </button>
                          )}
                        </div>

                        {contentError && (
                          <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-200">
                            <strong className="font-semibold">Error:</strong> {contentError}
                          </div>
                        )}

                        {generatedContent ? (
                          <div className="max-h-[600px] overflow-y-auto rounded-xl border border-white/10 bg-slate-900/60 p-4">
                            <pre className="whitespace-pre-wrap text-xs text-slate-200">{generatedContent}</pre>
                          </div>
                        ) : (
                          <div className="flex h-[300px] items-center justify-center rounded-xl border border-dashed border-white/10 bg-slate-900/30 text-sm text-slate-400">
                            {contentLoading ? "Generating content..." : "Generated content will appear here"}
                          </div>
                        )}

                        {generatedContent && (
                          <div className="mt-4 rounded-xl border border-cyan-400/30 bg-cyan-500/10 p-3 text-xs text-cyan-200">
                            <div className="font-semibold text-cyan-100">✨ Content Generated Successfully</div>
                            <p className="mt-1">Word count: ~{generatedContent.split(/\s+/).length} words</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </section>

                  <section id="seo-prediction" className="rounded-3xl border border-fuchsia-400/30 bg-fuchsia-500/10 p-6 shadow-xl">
                    {seoPrediction ? (
                      <>
                        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                          <div>
                            <h2 className="text-xl font-semibold text-slate-100">SEO Potential Prediction</h2>
                            <p className="text-sm text-slate-300/80">Makine öğrenimi modeli büyüme potansiyelini ve önceliklendirilecek alanları öngörür.</p>
                          </div>
                          <div className="rounded-2xl border border-white/10 bg-white/5 px-5 py-3 text-center">
                            <div className="text-xs uppercase tracking-[0.3em] text-slate-300/70">Potential Score</div>
                            <div className={`mt-2 text-4xl font-semibold ${getScoreColor(seoPrediction.seo_potential_score)}`}>
                              {seoPrediction.seo_potential_score}
                            </div>
                            <div className="text-xs text-slate-300">Confidence: {seoPrediction.confidence ?? "N/A"}</div>
                          </div>
                        </div>

                        <div className="mt-6 grid gap-4 lg:grid-cols-3">
                          <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-200">
                            <div className="font-semibold text-slate-100">Potential Level</div>
                            <p className="mt-2 text-slate-300/80">{seoPrediction.potential_level}</p>
                          </div>
                          <div className="lg:col-span-2">
                            {seoRecommendations.length > 0 ? (
                              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <div className="text-sm font-semibold text-slate-100">Priority Recommendations</div>
                                <ul className="mt-3 space-y-2 text-xs text-slate-200">
                                  {seoRecommendations.map((rec: any, idx: number) => (
                                    <li
                                      key={`${rec.area}-${idx}`}
                                      className={`flex items-start gap-3 rounded-2xl border px-3 py-3 ${
                                        rec.priority === "critical"
                                          ? "border-rose-400/30 bg-rose-500/10"
                                          : rec.priority === "high"
                                          ? "border-amber-400/30 bg-amber-500/10"
                                          : "border-sky-400/30 bg-sky-500/10"
                                      }`}
                                    >
                                      <span className="mt-0.5 rounded-full bg-white/10 px-2 py-1 text-[10px] font-semibold uppercase tracking-widest text-slate-100">
                                        {rec.priority}
                                      </span>
                                      <div>
                                        <div className="text-sm font-semibold text-slate-100/90">{rec.area}</div>
                                        <div className="text-xs text-slate-200/80">{rec.suggestion}</div>
                                      </div>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            ) : (
                              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300/80">
                                Bu analiz için önceliklendirilmiş öneri bulunmuyor.
                              </div>
                            )}
                          </div>
                        </div>
                      </>
                    ) : (
                      <p className="text-sm text-slate-300/80">SEO potansiyel tahmini oluşturulmadı.</p>
                    )}
                  </section>

                  <section id="report-meta" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-xs text-slate-300">
                    <strong className="text-slate-100/90">Report ID:</strong> {reportId}
                  </section>
                </>
              ) : null}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
