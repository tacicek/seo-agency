"""
Advanced SEO Data Analytics Module
Uses pandas, numpy, and scikit-learn for advanced analysis
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from collections import Counter
import re


def analyze_content_quality(text: str, keywords: List[str] = None) -> Dict[str, Any]:
    """
    Analyze content quality using data science techniques
    
    Args:
        text: The text content to analyze
        keywords: Optional list of target keywords
        
    Returns:
        Dict with quality metrics
    """
    if not text:
        return {"error": "No text provided"}
    
    # Basic metrics
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Calculate readability scores
    avg_word_length = np.mean([len(word) for word in words]) if words else 0
    avg_sentence_length = np.mean([len(s.split()) for s in sentences]) if sentences else 0
    
    # Flesch Reading Ease approximation
    syllables = sum([max(1, len(re.findall(r'[aeiouy]+', word.lower()))) for word in words])
    avg_syllables_per_word = syllables / len(words) if words else 0
    
    reading_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    reading_ease = max(0, min(100, reading_ease))  # Clamp between 0-100
    
    # Content diversity (unique word ratio)
    unique_words = len(set([w.lower() for w in words]))
    diversity_score = (unique_words / len(words) * 100) if words else 0
    
    # Keyword density analysis
    keyword_analysis = {}
    if keywords:
        text_lower = text.lower()
        for kw in keywords:
            count = text_lower.count(kw.lower())
            density = (count / len(words) * 100) if words else 0
            keyword_analysis[kw] = {
                "count": count,
                "density": round(density, 2)
            }
    
    return {
        "total_words": len(words),
        "total_sentences": len(sentences),
        "unique_words": unique_words,
        "avg_word_length": round(avg_word_length, 2),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "readability_score": round(reading_ease, 2),
        "readability_level": get_readability_level(reading_ease),
        "diversity_score": round(diversity_score, 2),
        "keyword_analysis": keyword_analysis
    }


def get_readability_level(score: float) -> str:
    """Convert Flesch score to readability level"""
    if score >= 90:
        return "Very Easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly Easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly Difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College)"
    else:
        return "Very Difficult (College graduate)"


def compare_competitors(urls_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare multiple URLs using pandas
    
    Args:
        urls_data: List of analysis results from different URLs
        
    Returns:
        Comparative analysis
    """
    if not urls_data:
        return {"error": "No data provided"}
    
    # Create DataFrame
    df = pd.DataFrame(urls_data)
    
    # Calculate statistics
    stats = {
        "total_sites": len(df),
        "avg_domain_authority": df.get("domain_authority", pd.Series([0])).mean(),
        "avg_page_authority": df.get("page_authority", pd.Series([0])).mean(),
        "avg_spam_score": df.get("spam_score", pd.Series([0])).mean(),
        "best_performing": {
            "domain_authority": df.loc[df.get("domain_authority", pd.Series([0])).idxmax()].to_dict() if "domain_authority" in df else None,
            "page_authority": df.loc[df.get("page_authority", pd.Series([0])).idxmax()].to_dict() if "page_authority" in df else None,
        }
    }
    
    return stats


def predict_seo_potential(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict SEO potential using weighted scoring
    
    Args:
        metrics: Dictionary with SEO metrics
        
    Returns:
        Prediction with score and recommendations
    """
    # Weights for different factors
    weights = {
        "domain_authority": 0.25,
        "page_authority": 0.20,
        "content_quality": 0.20,
        "backlinks": 0.15,
        "technical": 0.10,
        "spam_penalty": -0.10
    }
    
    # Extract and normalize metrics (0-100 scale)
    da = metrics.get("domain_authority", 0)
    pa = metrics.get("page_authority", 0)
    spam = metrics.get("spam_score", 0)
    backlinks = min(100, (metrics.get("root_domains_linking", 0) / 100) * 100)
    
    # Calculate weighted score
    score = (
        da * weights["domain_authority"] +
        pa * weights["page_authority"] +
        backlinks * weights["backlinks"] -
        spam * weights["spam_penalty"]
    )
    
    # Generate recommendations
    recommendations = []
    
    if da < 40:
        recommendations.append({
            "priority": "high",
            "area": "Domain Authority",
            "suggestion": "Focus on acquiring high-quality backlinks from authoritative domains"
        })
    
    if pa < 40:
        recommendations.append({
            "priority": "high",
            "area": "Page Authority",
            "suggestion": "Improve on-page SEO and content quality"
        })
    
    if spam > 30:
        recommendations.append({
            "priority": "critical",
            "area": "Spam Score",
            "suggestion": "Audit and remove toxic backlinks immediately"
        })
    
    if backlinks < 20:
        recommendations.append({
            "priority": "medium",
            "area": "Backlinks",
            "suggestion": "Implement link building strategy to increase referring domains"
        })
    
    return {
        "seo_potential_score": round(score, 2),
        "potential_level": get_potential_level(score),
        "recommendations": recommendations,
        "confidence": "high" if len(recommendations) <= 2 else "medium"
    }


def get_potential_level(score: float) -> str:
    """Convert score to potential level"""
    if score >= 80:
        return "Excellent - High ranking potential"
    elif score >= 60:
        return "Good - Moderate ranking potential"
    elif score >= 40:
        return "Fair - Needs improvement"
    else:
        return "Poor - Significant work required"


def analyze_keyword_trends(keywords_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze keyword trends over time using numpy
    
    Args:
        keywords_data: Historical keyword data
        
    Returns:
        Trend analysis
    """
    if not keywords_data:
        return {"error": "No data provided"}
    
    df = pd.DataFrame(keywords_data)
    
    # Calculate trends
    trends = {}
    for keyword in df["keyword"].unique():
        kw_data = df[df["keyword"] == keyword]
        counts = kw_data["count"].values
        
        if len(counts) > 1:
            # Simple linear trend
            x = np.arange(len(counts))
            z = np.polyfit(x, counts, 1)
            trend = "increasing" if z[0] > 0 else "decreasing"
            
            trends[keyword] = {
                "trend": trend,
                "slope": float(z[0]),
                "avg_count": float(np.mean(counts)),
                "volatility": float(np.std(counts))
            }
    
    return {
        "analyzed_keywords": len(trends),
        "trends": trends
    }


def generate_content_suggestions(current_keywords: List[str], target_keywords: List[str]) -> Dict[str, Any]:
    """
    Generate content optimization suggestions
    
    Args:
        current_keywords: Keywords currently in content
        target_keywords: Desired keywords to rank for
        
    Returns:
        Optimization suggestions
    """
    current_set = set([k.lower() for k in current_keywords])
    target_set = set([k.lower() for k in target_keywords])
    
    missing = target_set - current_set
    present = target_set & current_set
    
    return {
        "coverage": len(present) / len(target_set) * 100 if target_set else 0,
        "missing_keywords": list(missing),
        "present_keywords": list(present),
        "suggestions": [
            f"Add '{kw}' to your content naturally" for kw in list(missing)[:5]
        ]
    }


def generate_ai_insights(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate AI-powered insights from complete analysis
    
    Args:
        analysis_data: Complete analysis results
        
    Returns:
        Comprehensive insights
    """
    insights = {
        "strengths": [],
        "weaknesses": [],
        "opportunities": [],
        "threats": [],
        "action_items": []
    }
    
    # Analyze MOZ metrics
    moz = analysis_data.get("moz", {}).get("backlink_metrics", {})
    da = moz.get("domain_authority", 0)
    pa = moz.get("page_authority", 0)
    spam = moz.get("spam_score", 0)
    
    if da >= 60:
        insights["strengths"].append(f"Strong Domain Authority ({da}) indicates established credibility")
    elif da < 30:
        insights["weaknesses"].append(f"Low Domain Authority ({da}) limits ranking potential")
        insights["action_items"].append("Priority: Build high-quality backlinks to improve Domain Authority")
    
    if spam > 30:
        insights["threats"].append(f"High Spam Score ({spam}) could trigger penalties")
        insights["action_items"].append("Critical: Conduct backlink audit and disavow toxic links")
    
    # Analyze content quality
    content = analysis_data.get("content_quality", {})
    readability = content.get("readability_score", 0)
    
    if readability >= 60:
        insights["strengths"].append(f"Good readability score ({readability}) enhances user experience")
    elif readability < 40:
        insights["weaknesses"].append("Content is too complex for average readers")
        insights["action_items"].append("Simplify content structure and use shorter sentences")
    
    word_count = content.get("total_words", 0)
    if word_count < 300:
        insights["weaknesses"].append("Content is too thin for good rankings")
        insights["action_items"].append("Expand content to at least 1000-1500 words")
    elif word_count >= 1500:
        insights["strengths"].append("Comprehensive content length supports SEO")
    
    # Analyze on-page SEO
    onpage = analysis_data.get("onpage", {})
    title = onpage.get("title", "")
    meta_desc = onpage.get("meta_description", "")
    
    if not title:
        insights["weaknesses"].append("Missing title tag - critical for SEO")
        insights["action_items"].append("Add optimized title tag (50-60 characters)")
    
    if not meta_desc:
        insights["opportunities"].append("Add meta description to improve CTR")
        insights["action_items"].append("Write compelling meta description (150-160 characters)")
    
    # Calculate priority score
    critical_issues = len([item for item in insights["action_items"] if "Critical" in item])
    priority_score = 100 - (len(insights["weaknesses"]) * 10) - (critical_issues * 20)
    priority_score = max(0, min(100, priority_score))
    
    return {
        "insights": insights,
        "priority_score": priority_score,
        "total_action_items": len(insights["action_items"]),
        "summary": generate_summary(insights)
    }


def generate_summary(insights: Dict[str, List[str]]) -> str:
    """Generate human-readable summary"""
    strength_count = len(insights["strengths"])
    weakness_count = len(insights["weaknesses"])
    
    if weakness_count == 0 and strength_count > 3:
        return "Excellent SEO health with strong fundamentals across all areas"
    elif weakness_count <= 2:
        return "Good SEO foundation with minor improvements needed"
    elif weakness_count <= 5:
        return "Moderate SEO health requiring focused optimization"
    else:
        return "Significant SEO challenges requiring comprehensive strategy"


def calculate_comprehensive_score(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate comprehensive SEO score using all available data
    
    Args:
        analysis_data: Complete analysis results
        
    Returns:
        Overall SEO score with breakdown
    """
    scores = {
        "domain_authority": 0,
        "page_authority": 0,
        "content_quality": 0,
        "technical_seo": 0,
        "user_experience": 0
    }
    
    weights = {
        "domain_authority": 0.25,
        "page_authority": 0.20,
        "content_quality": 0.25,
        "technical_seo": 0.15,
        "user_experience": 0.15
    }
    
    # Domain Authority Score
    moz = analysis_data.get("moz", {}).get("backlink_metrics", {})
    scores["domain_authority"] = moz.get("domain_authority", 0) or 0
    scores["page_authority"] = moz.get("page_authority", 0) or 0
    
    # Content Quality Score
    content = analysis_data.get("content_quality", {})
    word_count = content.get("total_words", 0) or 0
    readability = content.get("readability_score", 50) or 50
    
    # Normalize content score
    word_score = min(100, (word_count / 1500) * 100) if word_count < 1500 else 100
    content_score = (word_score * 0.4) + (readability * 0.6)
    scores["content_quality"] = content_score
    
    # Technical SEO Score
    onpage = analysis_data.get("onpage", {})
    technical_score = 100
    
    if not onpage.get("title"):
        technical_score -= 30
    if not onpage.get("meta_description"):
        technical_score -= 20
    if not onpage.get("h1"):
        technical_score -= 15
    if len(onpage.get("images_without_alt", [])) > 0:
        technical_score -= min(20, len(onpage.get("images_without_alt", [])) * 5)
    
    scores["technical_seo"] = max(0, technical_score)
    
    # User Experience Score (based on readability and performance)
    perf = analysis_data.get("performance", {})
    perf_score = perf.get("score", 50) or 50
    ux_score = (readability * 0.4) + (perf_score * 0.6)
    scores["user_experience"] = ux_score
    
    # Calculate weighted total - ensure all values are not None
    total_score = 0
    for key in scores.keys():
        score_val = scores[key] or 0
        weight_val = weights[key]
        total_score += score_val * weight_val
    
    return {
        "overall_score": round(total_score, 2),
        "score_breakdown": {k: round(v or 0, 2) for k, v in scores.items()},
        "grade": get_grade(total_score),
        "percentile": get_percentile(total_score)
    }


def get_grade(score: float) -> str:
    """Convert score to letter grade"""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def get_percentile(score: float) -> str:
    """Estimate percentile ranking"""
    if score >= 90:
        return "Top 5% of websites"
    elif score >= 80:
        return "Top 15% of websites"
    elif score >= 70:
        return "Top 30% of websites"
    elif score >= 60:
        return "Top 50% of websites"
    else:
        return "Bottom 50% of websites"


if __name__ == "__main__":
    # Test the analytics
    sample_text = """
    This is a sample text for testing content quality analysis.
    It contains multiple sentences with various words.
    The analysis will check readability and other metrics.
    """
    
    result = analyze_content_quality(sample_text, keywords=["analysis", "content"])
    print("Content Quality Analysis:")
    print(result)
    
    sample_metrics = {
        "domain_authority": 45,
        "page_authority": 50,
        "spam_score": 5,
        "root_domains_linking": 150
    }
    
    prediction = predict_seo_potential(sample_metrics)
    print("\nSEO Potential Prediction:")
    print(prediction)
