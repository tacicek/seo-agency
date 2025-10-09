import re
import os
from collections import Counter
from typing import Optional

# Comprehensive multilingual stop words (English, German, French, Italian, Spanish)
STOPWORDS = set("""
    the a an and or for to of in on with is are was were be by as it this that from at your you we they i our their
    der die das den dem des ein eine einer eines einem einen zur zum bei aus nach vor von mit über durch um nicht
    und oder aber auch wenn dann als wie so noch nur schon mehr sehr viel bereits sein seine seine ihr ihre hat haben
    wird werden kann können muss müssen soll sollen will wollen wurde wurden ist sind war waren sein seine
    ich du er sie es wir ihr ihnen sich mich dich uns euch ihm ihn sie ihnen man einer einem einen
    auf an in zu von bei mit nach über unter durch für um gegen ohne bis seit zwischen hinter neben während
    dieser diese dieses jener jene jenes welcher welche welches solcher solche solches aller alle alles
    mein meine meiner meines meinem meinen dein deine deiner deines deinem deinen
    unser unsere unserer unseres unserem unseren euer eure eurer eures eurem euren
    le la les un une des de du à au aux et ou mais donc car ni ne pas plus moins très tout tous toute toutes
    ce cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs
    je tu il elle nous vous ils elles on me te se lui en y
    être avoir faire dire aller voir venir pouvoir vouloir devoir savoir prendre mettre donner
    il lo la i gli le un uno una dei degli delle di da a in con su per tra fra
    che e o ma anche se non più molto questo quello come quando dove
    io tu lui lei noi voi loro mi ti si ci vi
    essere avere faire dire andare venire potere volere dovere sapere prendere mettere dare
    el la los las un una unos unas de del a al en con por para sobre entre
    que y o pero también si no más muy este esta estos estas ese esa esos esas
    yo tú él ella nosotros vosotros ellos ellas me te se nos os
    ser estar haber tener hacer ir venir poder querer deber saber poner dar
    stock angebot mehr nova bereits transport
""".split())

def analyze_keywords(text: str, top_n: int = 25) -> dict:
    """
    Analyze text and extract top keywords with frequency and density.
    
    Features:
    - Multilingual stop word filtering (EN, DE, FR, IT, ES)
    - Minimum word length: 3 characters
    - Case-insensitive analysis
    - Percentage density calculation
    
    Args:
        text: Input text to analyze
        top_n: Number of top keywords to return (default: 25)
        
    Returns:
        dict: {
            "total_words": int,
            "top": [{"word": str, "count": int, "percent": float}]
        }
    """
    # Extract words (alphanumeric + umlauts/accents)
    words = re.findall(r"\b[\w\u00C0-\u017F]+\b", text.lower())
    
    # Filter stop words and short words
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    
    total = len(words) or 1
    freq = Counter(words)
    top = freq.most_common(top_n)
    
    density = [
        {
            "word": w, 
            "count": c, 
            "percent": round(c * 100.0 / total, 2)
        } 
        for w, c in top
    ]
    
    return {
        "total_words": total, 
        "top": density
    }


def analyze_seo_keywords(text: str, url: str, title: Optional[str] = None, top_n: int = 10) -> dict:
    """
    SEO-focused keyword analysis using SERP data and search volume.
    
    Instead of just word frequency, this function:
    1. Extracts main topic from URL/title (e.g., "umzug", "transport")
    2. Gets related searches from SerpAPI for that topic
    3. Matches page content keywords with SERP-based keywords
    4. Enriches with search volume data (DataForSEO if available)
    5. Returns top keywords ranked by relevance × search volume
    
    Args:
        text: Page content
        url: Page URL (used for topic extraction)
        title: Page title (optional, helps topic detection)
        top_n: Number of top SEO keywords to return
        
    Returns:
        dict: {
            "detected_topic": str,
            "seo_keywords": [{"keyword": str, "search_volume": int, "relevance_score": float, "count_on_page": int}],
            "related_searches": [str],
            "method": str
        }
    """
    from .serpapi import analyze_serp_results
    
    # Extract topic from URL and title
    topic = _extract_topic(url, title or "")
    
    if not topic:
        # Fallback: analyze basic keywords and return top as topic
        basic = analyze_keywords(text, top_n=5)
        if basic["top"]:
            topic = basic["top"][0]["word"]
        else:
            return {
                "detected_topic": None,
                "seo_keywords": [],
                "related_searches": [],
                "method": "fallback_failed"
            }
    
    # Get related searches from SERP
    related_keywords = []
    try:
        serp_data = analyze_serp_results(topic, location="Switzerland")
        if serp_data and not serp_data.get("error"):
            # Extract related searches
            related = serp_data.get("related_searches", [])
            related_keywords = [r.get("query", "") for r in related if r.get("query")]
            
            # Extract People Also Ask keywords
            paa = serp_data.get("people_also_ask", [])
            for q in paa:
                question = q.get("question", "")
                if question:
                    related_keywords.append(question.lower())
    except Exception:
        pass  # SerpAPI not available or quota exceeded
    
    # Extract all candidate keywords from page
    words = re.findall(r"\b[\w\u00C0-\u017F]+\b", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    word_freq = Counter(words)
    
    # Build keyword candidates: combine topic + related + high-frequency words
    candidates = set()
    candidates.add(topic.lower())
    for kw in related_keywords:
        # Extract individual words from related searches
        for w in re.findall(r"\b[\w\u00C0-\u017F]+\b", kw.lower()):
            if w not in STOPWORDS and len(w) > 2:
                candidates.add(w)
    
    # Add top words from page that are NOT stopwords
    for w, _ in word_freq.most_common(30):
        candidates.add(w)
    
    # Score candidates: relevance = count_on_page × serp_match_boost
    scored = []
    for kw in candidates:
        count = word_freq.get(kw, 0)
        serp_boost = 2.0 if any(kw in rk.lower() for rk in related_keywords) else 1.0
        topic_boost = 3.0 if kw == topic.lower() else 1.0
        score = count * serp_boost * topic_boost
        
        if score > 0:
            scored.append({
                "keyword": kw,
                "count_on_page": count,
                "relevance_score": round(score, 2),
                "search_volume": None  # Placeholder for DataForSEO integration
            })
    
    # Sort by relevance score descending
    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "detected_topic": topic,
        "seo_keywords": scored[:top_n],
        "related_searches": related_keywords[:10],
        "method": "serp_enhanced"
    }


def _extract_topic(url: str, title: str) -> Optional[str]:
    """
    Extract main topic/industry from URL and title.
    
    Examples:
        - "nova-stock.ch/umzug" → "umzug"
        - "Umzugsfirma Zürich - Nova Stock" → "umzugsfirma"
    """
    # Common industry keywords (extend as needed)
    industry_keywords = [
        "umzug", "umzugsfirma", "transport", "spedition", "möbeltransport",
        "reinigung", "cleaning", "hausverwaltung", "immobilien", "real estate",
        "restaurant", "catering", "hotel", "bau", "renovation", "handwerk",
        "marketing", "agentur", "consulting", "beratung", "software", "web",
        "fitness", "gym", "yoga", "wellness", "spa", "beauty", "friseur"
    ]
    
    combined = (url + " " + title).lower()
    
    # Check for industry keywords in URL/title
    for kw in industry_keywords:
        if kw in combined:
            return kw
    
    # Fallback: extract domain-specific word from URL path
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    path_parts = [p for p in parsed.path.split("/") if p and len(p) > 3]
    if path_parts:
        candidate = re.sub(r"[^a-zäöüß]", "", path_parts[0].lower())
        if candidate and candidate not in STOPWORDS:
            return candidate
    
    return None
