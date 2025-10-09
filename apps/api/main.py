from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from analyzers.onpage import analyze_onpage
from analyzers.keywords import analyze_keywords, analyze_seo_keywords
from analyzers.performance import analyze_performance
from analyzers.moz import get_backlink_summary, analyze_moz_metrics, test_moz_connection
from analyzers.data_analytics import (
    analyze_content_quality,
    predict_seo_potential,
    generate_ai_insights,
    calculate_comprehensive_score,
    generate_content_suggestions
)
from analyzers.serpapi import (
    analyze_serp_results,
    analyze_keyword_difficulty,
    batch_keyword_analysis,
    track_keyword_ranking,
    analyze_competitors
)
from analyzers.ai_insights import (
    get_all_ai_insights,
    get_openai_insights,
    get_gemini_insights,
    get_claude_insights,
    generate_meta_tags,
    generate_content_improvements,
    AIProvider
)
from analyzers.content_generator import generate_seo_content
from analyzers.llm_registry import get_default_model, get_recommended_models, get_registry_snapshot
from services.storage import save_report
from services.ingestion import run_ingestion
from apscheduler.schedulers.background import BackgroundScheduler
import os, json
from services.pdf_report import generate_pdf_bytes
from analyzers.dataforseo import (
    test_dataforseo_connection,
    analyze_keyword_difficulty_dfs,
    analyze_serp_results_dfs,
)

app = FastAPI(title="SEO Analyzer API", version="0.1.0")

# CORS middleware to allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple daily scheduler at 02:00 server time (optional)
scheduler = BackgroundScheduler(timezone="UTC")
def _scheduled_job():
    try:
        # Expect env JSON for a default scheduled job
        job_cfg = os.getenv("SCHEDULED_INGESTION_PAYLOAD")
        if not job_cfg:
            return
        payload = json.loads(job_cfg)
        run_ingestion(payload, save_report)
    except Exception:
        pass
scheduler.add_job(_scheduled_job, "cron", hour=2, minute=0)
try:
    scheduler.start()
except Exception:
    pass

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    include_serp: bool = False  # Optional SERP analysis
    keyword: str | None = None  # Keyword for SERP analysis

class PDFRequest(BaseModel):
    domain: str
    score: int | float = 0
    summary: str = ""

class KeywordDifficultyRequest(BaseModel):
    keyword: str
    location: str = "United States"

class BatchKeywordRequest(BaseModel):
    keywords: list[str]
    location: str = "United States"

class RankTrackingRequest(BaseModel):
    domain: str
    keywords: list[str]
    location: str = "United States"
    language: str = "en"

class DFSKeywordRequest(BaseModel):
    keyword: str
    location_name: str = "United States"
    language_name: str = "English"

class DFSSerpRequest(BaseModel):
    keyword: str
    location_name: str = "United States"
    language_name: str = "English"
    device: str = "desktop"  # mobile|desktop

class CompetitorAnalysisRequest(BaseModel):
    domain: str
    keywords: list[str]
    location: str = "United States"
    language: str = "en"

class AIInsightsRequest(BaseModel):
    url: HttpUrl
    ai_provider: str = "auto"  # auto, openai, gemini, claude
    include_competitors: bool = False

class MetaTagGenerationRequest(BaseModel):
    content: str
    ai_provider: str = "openai"

class ContentImprovementRequest(BaseModel):
    content: str
    keywords: list[str]
    ai_provider: str = "openai"

class ContentGeneratorRequest(BaseModel):
    topic: str
    page_type: str = "BLOG"  # SERVICE / BLOG / LANDING PAGE
    main_keyword: str
    secondary_keywords: list[str] = []
    target_location: str | None = None
    target_audience: str | None = None
    language: str = "Turkish"
    tone: str = "professional but friendly"
    word_count: int = 1200
    competitor_urls: list[str] = []
    local_context: str | None = None
    provider: str = "openai"  # openai / anthropic / gemini
    model: str | None = None  # Optional: specific model name

class IngestionRequest(BaseModel):
    project_id: str
    gcp_credentials: str  # service account JSON as string; DO NOT LOG
    gsc: dict
    psi: dict
    sampling: dict | None = None
    policy: dict | None = None
    rate_limits: dict | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/moz/test")
def moz_test():
    """Test MOZ API connection"""
    result = test_moz_connection()
    return result

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        # Basic analysis
        onpage = analyze_onpage(str(req.url))
        keywords = analyze_keywords(onpage.get("text_content", ""))
        
        # SEO-focused keyword analysis (SERP-enhanced)
        seo_keywords = analyze_seo_keywords(
            text=onpage.get("text_content", ""),
            url=str(req.url),
            title=onpage.get("title"),
            top_n=10
        )
        
        performance = analyze_performance(str(req.url))
        
        # MOZ metrics
        moz_metrics = get_backlink_summary(str(req.url))
        
        # Advanced Data Analytics (use SEO keywords for better relevance)
        top_seo_kw = [kw["keyword"] for kw in seo_keywords.get("seo_keywords", [])[:5]]
        if not top_seo_kw:
            top_seo_kw = [kw["word"] for kw in keywords.get("top", [])[:5]]
        
        content_quality = analyze_content_quality(
            onpage.get("text_content", ""),
            keywords=top_seo_kw
        )
        
        # SEO Potential Prediction
        seo_prediction = predict_seo_potential({
            "domain_authority": moz_metrics.get("backlink_metrics", {}).get("domain_authority", 0),
            "page_authority": moz_metrics.get("backlink_metrics", {}).get("page_authority", 0),
            "spam_score": moz_metrics.get("backlink_metrics", {}).get("spam_score", 0),
            "root_domains_linking": moz_metrics.get("backlink_metrics", {}).get("root_domains_linking", 0),
        })
        
        # Combine all data for comprehensive analysis
        complete_analysis = {
            "onpage": onpage,
            "keywords": keywords,
            "seo_keywords": seo_keywords,
            "performance": performance,
            "moz": moz_metrics,
            "content_quality": content_quality
        }
        
        # Generate AI insights
        ai_insights = generate_ai_insights(complete_analysis)
        
        # Calculate comprehensive score
        comprehensive_score = calculate_comprehensive_score(complete_analysis)
        
        # Optional SERP analysis
        serp_analysis = None
        if req.include_serp and req.keyword:
            serp_analysis = analyze_serp_results(req.keyword)
        
        report = {
            "url": str(req.url),
            "onpage": onpage,
            "keywords": keywords,
            "seo_keywords": seo_keywords,
            "performance": performance,
            "moz": moz_metrics,
            "content_quality": content_quality,
            "seo_prediction": seo_prediction,
            "ai_insights": ai_insights,
            "comprehensive_score": comprehensive_score,
            "serp_analysis": serp_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        report_id = save_report(report)
        return {"reportId": report_id, "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export/pdf")
def export_pdf(req: PDFRequest):
    pdf = generate_pdf_bytes(req.domain, req.score, req.summary)
    # Return as base64 to keep it simple
    import base64
    return {"filename": f"seo-report-{req.domain}.pdf", "base64": base64.b64encode(pdf).decode("utf-8")}

@app.post("/webhooks/scan")
def webhook_scan(payload: dict):
    # expected: { "websiteId": "...", "url": "https://..." }
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="url required")
    onpage = analyze_onpage(url)
    keywords = analyze_keywords(onpage.get("text_content", ""))
    performance = analyze_performance(url)
    moz_metrics = get_backlink_summary(url)
    report = {
        "url": url,
        "onpage": onpage,
        "keywords": keywords,
        "performance": performance,
        "moz": moz_metrics
    }
    report_id = save_report(report)
    return {"ok": True, "reportId": report_id}

# ===== SerpAPI Endpoints =====

@app.post("/serp/analyze")
def serp_analyze(req: KeywordDifficultyRequest):
    """
    Analyze Google SERP for a specific keyword
    Returns: organic results, featured snippets, PAA, knowledge graph, etc.
    """
    try:
        result = analyze_serp_results(req.keyword, req.location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serp/difficulty")
def serp_difficulty(req: KeywordDifficultyRequest):
    """
    Calculate keyword difficulty score
    Returns: difficulty score (0-100), level (Easy/Medium/Hard), recommendations
    """
    try:
        result = analyze_keyword_difficulty(req.keyword, req.location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serp/batch")
def serp_batch(req: BatchKeywordRequest):
    """
    Batch keyword difficulty analysis
    Returns: Analysis for multiple keywords with summary statistics
    """
    try:
        result = batch_keyword_analysis(req.keywords, req.location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/serp/test")
def serp_test():
    """Test SerpAPI connection"""
    import os
    api_key = os.getenv('SERPAPI_API_KEY')
    
    if not api_key:
        return {
            "status": "error",
            "message": "SERPAPI_API_KEY not configured",
            "instructions": "Set SERPAPI_API_KEY environment variable"
        }
    
    # Try a simple search
    try:
        result = analyze_keyword_difficulty("test query", "United States")
        if 'error' in result:
            return {
                "status": "error",
                "message": result['error']
            }
        return {
            "status": "success",
            "message": "SerpAPI connection successful",
            "test_result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# ===== DataForSEO Endpoints =====

@app.get("/dfs/test")
def dfs_test():
    """Test DataForSEO connection"""
    return test_dataforseo_connection()

@app.post("/dfs/difficulty")
def dfs_difficulty(req: DFSKeywordRequest):
    try:
        result = analyze_keyword_difficulty_dfs(req.keyword, req.location_name, req.language_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dfs/serp")
def dfs_serp(req: DFSSerpRequest):
    try:
        result = analyze_serp_results_dfs(req.keyword, req.location_name, req.language_name, req.device)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serp/rank-tracking")
def serp_rank_tracking(req: RankTrackingRequest):
    """
    Track domain's ranking positions for multiple keywords
    
    Example:
    {
        "domain": "bs-company.ch",
        "keywords": ["umzug zürich", "umzugsfirma zürich", "zürich umzug"],
        "location": "Switzerland",
        "language": "de"
    }
    
    Returns:
    - Summary with visibility score, average position, rankings by position
    - Detailed rankings for each keyword with position, URL, competitors
    - Recommendations for improvement
    """
    try:
        result = track_keyword_ranking(
            req.domain, 
            req.keywords, 
            req.location,
            req.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/serp/competitor-analysis")
def serp_competitor_analysis(req: CompetitorAnalysisRequest):
    """
    Analyze top competitors for given keywords
    
    Example:
    {
        "domain": "bs-company.ch",
        "keywords": ["umzug zürich", "umzugsfirma", "transport zürich"],
        "location": "Switzerland",
        "language": "de"
    }
    
    Returns:
    - Top 10 competitors with visibility scores
    - Competitive landscape analysis
    - Market concentration metrics
    - Strategic recommendations
    """
    try:
        result = analyze_competitors(
            req.domain,
            req.keywords,
            req.location,
            req.language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== AI-Powered Insights Endpoints =====

@app.post("/ai/insights")
def ai_insights(req: AIInsightsRequest):
    """
    Generate AI-powered SEO insights for a URL
    
    Example:
    {
        "url": "https://bs-company.ch",
        "ai_provider": "auto",
        "include_competitors": false
    }
    
    AI Providers:
    - "auto": Try all available providers, use first successful
    - "openai": Use OpenAI GPT-4
    - "gemini": Use Google Gemini
    - "claude": Use Anthropic Claude
    
    Returns:
    - Comprehensive SEO analysis
    - Content quality assessment
    - Technical SEO issues (prioritized)
    - Keyword strategy recommendations
    - Backlink profile analysis
    - Priority action items
    - Quick wins
    - Long-term strategy
    - Overall SEO score
    """
    try:
        # Get basic SEO analysis
        onpage = analyze_onpage(str(req.url))
        keywords = analyze_keywords(onpage.get("text_content", ""))
        performance = analyze_performance(str(req.url))
        moz_metrics = get_backlink_summary(str(req.url))
        
        content_quality = analyze_content_quality(
            onpage.get("text_content", ""),
            keywords=[kw["word"] for kw in keywords.get("top", [])[:5]]
        )
        
        # Prepare analysis data
        analysis_data = {
            "url": str(req.url),
            "onpage": onpage,
            "keywords": keywords,
            "performance": performance,
            "moz": moz_metrics,
            "content_quality": content_quality
        }
        
        # Add competitor data if requested
        if req.include_competitors:
            try:
                # Get top keywords for competitor analysis
                top_keywords = [kw["word"] for kw in keywords.get("top", [])[:5]]
                competitors = analyze_competitors(
                    str(req.url),
                    top_keywords,
                    "United States",
                    "en"
                )
                analysis_data["competitors"] = competitors
            except:
                pass  # Continue without competitor data
        
        # Generate AI insights based on provider
        if req.ai_provider.lower() == "auto":
            ai_result = get_all_ai_insights(analysis_data)
        elif req.ai_provider.lower() == "openai":
            ai_result = get_openai_insights(analysis_data)
        elif req.ai_provider.lower() == "gemini":
            ai_result = get_gemini_insights(analysis_data)
        elif req.ai_provider.lower() == "claude":
            ai_result = get_claude_insights(analysis_data)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid AI provider: {req.ai_provider}. Use: auto, openai, gemini, or claude"
            )
        
        return {
            "url": str(req.url),
            "analysis_data": analysis_data,
            "ai_insights": ai_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/meta-tags")
def ai_meta_tags(req: MetaTagGenerationRequest):
    """
    Generate optimized meta tags using AI
    
    Example:
    {
        "content": "Your webpage content here...",
        "ai_provider": "openai"
    }
    
    Returns:
    - 3 variations of meta titles (50-60 chars)
    - 3 variations of meta descriptions (150-160 chars)
    - Primary keywords identified
    - SEO recommendations
    """
    try:
        provider = AIProvider(req.ai_provider.lower())
        result = generate_meta_tags(req.content, provider)
        return result
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid AI provider: {req.ai_provider}. Use: openai, gemini, or claude"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/content-improvements")
def ai_content_improvements(req: ContentImprovementRequest):
    """
    Get AI-powered content improvement suggestions
    
    Example:
    {
        "content": "Your current page content...",
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "ai_provider": "openai"
    }
    
    Returns:
    - Content structure issues
    - Keyword optimization tips
    - Readability improvements
    - Content gaps to fill
    - Engagement tips
    - Specific rewrite examples
    - Priority score and estimated impact
    """
    try:
        provider = AIProvider(req.ai_provider.lower())
        result = generate_content_improvements(req.content, req.keywords, provider)
        return result
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid AI provider: {req.ai_provider}. Use: openai, gemini, or claude"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/test")
def ai_test():
    """Test AI provider connections"""
    import os
    
    results = {
        "openai": {
            "configured": bool(os.getenv('OPENAI_API_KEY')),
            "default_model": os.getenv('OPENAI_MODEL', get_default_model('openai')),
            "recommended_models": get_recommended_models('openai'),
        },
        "azure-openai": {
            "configured": bool(os.getenv('AZURE_OPENAI_ENDPOINT') and os.getenv('AZURE_OPENAI_API_KEY')),
            "default_model": os.getenv('AZURE_OPENAI_DEPLOYMENT', get_default_model('openai')),
            "recommended_models": [m for m in get_recommended_models('openai') if m.startswith('gpt')],
        },
        "gemini": {
            "configured": bool(os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')),
            "default_model": os.getenv('GEMINI_MODEL', get_default_model('gemini')),
            "recommended_models": get_recommended_models('gemini'),
        },
        "anthropic": {
            "configured": bool(os.getenv('ANTHROPIC_API_KEY')),
            "default_model": os.getenv('ANTHROPIC_MODEL', get_default_model('anthropic')),
            "recommended_models": get_recommended_models('anthropic'),
        },
        "mistral": {
            "configured": bool(os.getenv('MISTRAL_API_KEY')),
            "default_model": os.getenv('MISTRAL_MODEL', get_default_model('mistral')),
            "recommended_models": get_recommended_models('mistral'),
        }
    }
    
    available = [k for k, v in results.items() if v['configured']]
    
    return {
        "status": "ok" if available else "error",
        "message": f"{len(available)} AI provider(s) configured" if available else "No AI providers configured",
        "available_providers": available,
        "providers": results,
        "registry": get_registry_snapshot(),
        "instructions": {
            "openai": "Set OPENAI_API_KEY and optionally OPENAI_MODEL (e.g., gpt-5)",
            "azure-openai": "Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and optionally AZURE_OPENAI_DEPLOYMENT",
            "gemini": "Set GOOGLE_API_KEY or GEMINI_API_KEY and optionally GEMINI_MODEL (e.g., gemini-2.0-pro)",
            "anthropic": "Set ANTHROPIC_API_KEY and optionally ANTHROPIC_MODEL (e.g., claude-4.5-sonnet)",
            "mistral": "Set MISTRAL_API_KEY and optionally MISTRAL_MODEL (e.g., mistral-large-latest)"
        }
    }

# ===== AI Content Generator Endpoint =====

@app.post("/ai/generate-content")
def generate_content(req: ContentGeneratorRequest):
    """
    Generate topical, holistic, E-E-A-T optimized SEO content with latest AI models
    
    Supported Providers & Models (2025):
        OpenAI:
            - gpt-4o (default, recommended)
            - gpt-4o-mini (faster, cost-effective)
            - o1-preview (advanced reasoning)
            - o1-mini (reasoning, cost-effective)
        
        Anthropic:
            - claude-3-7-sonnet-20250219 (default, recommended)
            - claude-3-5-sonnet-20241022
            - claude-3-5-haiku-20241022
        
        Google Gemini:
            - gemini-2.0-flash-exp (default, recommended)
            - gemini-1.5-pro
            - gemini-1.5-flash
    
    Example:
    {
        "topic": "İstanbul Evden Eve Nakliyat - Profesyonel Taşıma Hizmeti",
        "page_type": "SERVICE",
        "main_keyword": "istanbul nakliyat",
        "secondary_keywords": ["evden eve nakliyat", "taşımacılık", "eşya taşıma"],
        "target_location": "İstanbul, Türkiye",
        "target_audience": "İstanbul'da taşınmak isteyen aileler ve profesyoneller",
        "language": "Turkish",
        "tone": "professional but friendly",
        "word_count": 1500,
        "competitor_urls": ["https://competitor1.com", "https://competitor2.com"],
        "local_context": "Kadıköy, Beşiktaş, Şişli merkezi bölgeler",
        "provider": "openai",
        "model": "gpt-4o"
    }
    
    Returns:
    - Full SEO-optimized content in Markdown format
    - Meta title and description
    - FAQ section
    - Internal linking suggestions
    - H1-H3 structured headings
    - CTA section
    - Metadata about generation (tokens, model, etc.)
    """
    try:
        result = generate_seo_content(
            topic=req.topic,
            page_type=req.page_type,
            main_keyword=req.main_keyword,
            secondary_keywords=req.secondary_keywords,
            target_location=req.target_location,
            target_audience=req.target_audience,
            language=req.language,
            tone=req.tone,
            word_count=req.word_count,
            competitor_urls=req.competitor_urls if req.competitor_urls else None,
            local_context=req.local_context,
            provider=req.provider,
            model=req.model,
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== Ingestion Endpoint =====

@app.post("/integrations/google/ingest")
def ingest_google(req: IngestionRequest):
    """
    Ingest GSC and PSI data, normalize and persist.
    Returns the normalized JSON payload or error schema.
    """
    try:
        # Mask secrets in logs – so do not log req.gcp_credentials
        payload = {
            "project_id": req.project_id,
            "gcp_credentials": req.gcp_credentials,
            "gsc": req.gsc,
            "psi": req.psi,
            "sampling": req.sampling or {},
            "policy": req.policy or {},
            "rate_limits": req.rate_limits or {},
        }
        result = run_ingestion(payload, save_report)
        if "error" in result:
            return result
        return result
    except Exception as e:
        return {"error": {"message": str(e), "hint": "Invalid request", "stage": "fetch"}}
