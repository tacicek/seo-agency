"""
AI-powered SEO Content Generator
Generates topical, holistic, E-E-A-T optimized content using OpenAI/Anthropic/Google Gemini models.
Supports latest models: GPT-4o, Claude 3.7 Sonnet, Gemini 2.0 Flash, etc.
"""
import os
from typing import Dict, Any, Optional, List
from .llm_registry import get_default_model
import anthropic
from openai import OpenAI

# Try to import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Try to import Mistral (support both new and old SDKs)
MISTRAL_AVAILABLE = False
MISTRAL_SDK_MODE = None  # "new" or "old"
try:
    from mistralai.client import MistralClient  # type: ignore
    from mistralai.models.chat_completion import ChatMessage  # type: ignore
    MISTRAL_AVAILABLE = True
    MISTRAL_SDK_MODE = "new"
except Exception:
    try:
        from mistralai import Mistral as MistralClient  # type: ignore
        ChatMessage = None  # not used in old SDK
        MISTRAL_AVAILABLE = True
        MISTRAL_SDK_MODE = "old"
    except Exception:
        MISTRAL_AVAILABLE = False


def build_content_prompt(
    topic: str,
    page_type: str,
    main_keyword: str,
    secondary_keywords: List[str],
    target_location: Optional[str] = None,
    target_audience: Optional[str] = None,
    language: str = "Turkish",
    tone: str = "professional but friendly",
    word_count: int = 1200,
    competitor_urls: Optional[List[str]] = None,
    local_context: Optional[str] = None,
) -> str:
    """
    Build the full prompt for topical/holistic SEO content generation.
    """
    secondary_kw_str = ", ".join(secondary_keywords) if secondary_keywords else "None provided"
    competitor_str = (
        f"\n- Model the structure after websites like: {', '.join(competitor_urls)}"
        if competitor_urls
        else ""
    )
    local_str = (
        f"\n- Add local references and context about {local_context}, using nearby landmarks or regional details."
        if local_context
        else ""
    )

    prompt = f"""You are an expert in holistic and topical SEO content writing.
Your task is to create a complete, search-optimized web page text that follows modern SEO principles (Topical Authority, E-E-A-T, and Semantic SEO).

INSTRUCTIONS:

1. **Page Context**
- Page type: {page_type}
- Target location: {target_location or "Global"}
- Target audience: {target_audience or "General audience"}
- Main keyword: {main_keyword}
- Secondary keywords: {secondary_kw_str}
- Language and tone: {language}, {tone}

2. **SEO Goals**
- Follow Topical SEO: cover all semantically related subtopics.
- Follow Holistic SEO: ensure the content fully satisfies the user intent (transactional / informational / navigational).
- Apply E-E-A-T: demonstrate experience, expertise, authority, and trust throughout the text.
- Optimize headings (H1–H3) for readability and SEO relevance.
- Suggest 2–3 internal links to related pages (use placeholder links like [link: related-topic]).
- Include a short FAQ section (3-5 questions) that answers user intent-based questions.
- Provide meta title (max 60 chars) and meta description (max 155 chars) at the end.

3. **Content Structure**
- H1: include the main keyword naturally.
- Introduction: 3–4 sentences that summarize the topic and value.
- H2–H3 sections: cover benefits, process, reasons to choose, pricing factors, and relevant subtopics.
- CTA: a short, persuasive paragraph encouraging the user to take action.
- Word count: minimum {word_count} words.

4. **Output Format**
Return the content in clean Markdown format, using proper H2/H3 hierarchy, bullet points, and short paragraphs.

**Additional Professional Tips:**
- Use semantic terms that commonly appear in Google's top 10 results for this keyword.
- Write as if authored by an experienced professional with 15+ years of experience in this field.
- Include emotional and persuasive triggers that lead users to take action.{competitor_str}{local_str}

Please ensure the content is:
- Unique and natural (no keyword stuffing),
- Semantically rich,
- SEO-optimized,
- Human-readable and conversion-oriented.

Now generate the content for:
**Topic:** {topic}
"""
    return prompt


def generate_content_openai(prompt: str, model: str = None) -> Dict[str, Any]:
    """
    Generate content using OpenAI models.
    
    Supported models (2025):
    - gpt-4o (recommended - latest flagship model)
    - gpt-4o-mini (faster, cost-effective)
    - gpt-4-turbo (legacy)
    - o1-preview (advanced reasoning)
    - o1-mini (reasoning, cost-effective)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = model or os.getenv("OPENAI_MODEL", get_default_model("openai") or "gpt-4o")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY not configured",
            "provider": "openai",
        }

    try:
        # Azure OpenAI support via env vars
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", model)

        if azure_endpoint and azure_api_key:
            # Use Azure OpenAI Completions API compatibility
            client = OpenAI(
                api_key=azure_api_key,
                base_url=f"{azure_endpoint.rstrip('/')}/openai/deployments/{azure_deployment}",
            )
            # For azure, set model to 'gpt-4o' like; deployment name resolves routing
            resolved_model = azure_deployment
        else:
            client = OpenAI(api_key=api_key)
            resolved_model = model
        
        # o1 models don't support system messages or temperature
        if resolved_model.startswith("o1"):
            response = client.chat.completions.create(
                model=resolved_model,
                messages=[
                    {"role": "user", "content": f"You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies.\n\n{prompt}"},
                ],
                max_completion_tokens=4000,
            )
        else:
            response = client.chat.completions.create(
                model=resolved_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=4000,
            )

        content = response.choices[0].message.content
        return {
            "success": True,
            "content": content,
            "provider": "openai",
            "model": resolved_model,
            "tokens_used": response.usage.total_tokens if response.usage else None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "openai",
        }


def generate_content_claude(prompt: str, model: str = None) -> Dict[str, Any]:
    """
    Generate content using Anthropic Claude.
    
    Supported models (2025):
    - claude-3-7-sonnet-20250219 (recommended - latest, most capable)
    - claude-3-5-sonnet-20241022 (previous flagship)
    - claude-3-5-haiku-20241022 (fast, cost-effective)
    - claude-3-opus-20240229 (legacy, powerful)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = model or os.getenv("ANTHROPIC_MODEL", get_default_model("anthropic") or "claude-3-7-sonnet-20250219")
    if not api_key:
        return {
            "success": False,
            "error": "ANTHROPIC_API_KEY not configured",
            "provider": "anthropic",
        }

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=4000,
            temperature=0.7,
            system="You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies.",
            messages=[{"role": "user", "content": prompt}],
        )

        content = message.content[0].text if message.content else ""
        return {
            "success": True,
            "content": content,
            "provider": "anthropic",
            "model": model,
            "tokens_used": message.usage.input_tokens + message.usage.output_tokens if message.usage else None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "anthropic",
        }


def generate_content_gemini(prompt: str, model: str = None) -> Dict[str, Any]:
    """
    Generate content using Google Gemini.
    
    Supported models (2025):
    - gemini-2.0-flash-exp (recommended - latest, fastest)
    - gemini-1.5-pro (powerful, large context)
    - gemini-1.5-flash (fast, cost-effective)
    """
    if not GEMINI_AVAILABLE:
        return {
            "success": False,
            "error": "Google Generative AI library not installed. Install: pip install google-generativeai",
            "provider": "gemini",
        }
    
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMINI_MODEL", get_default_model("gemini") or "gemini-2.0-flash-exp")
    if not api_key:
        return {
            "success": False,
            "error": "GOOGLE_API_KEY or GEMINI_API_KEY not configured",
            "provider": "gemini",
        }

    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction="You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies.",
        )
        
        response = model_instance.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4000,
            }
        )

        content = response.text if response.text else ""
        
        # Calculate tokens (approximate)
        tokens_used = None
        if hasattr(response, 'usage_metadata'):
            tokens_used = response.usage_metadata.total_token_count
        
        return {
            "success": True,
            "content": content,
            "provider": "gemini",
            "model": model,
            "tokens_used": tokens_used,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "gemini",
        }


def generate_content_mistral(prompt: str, model: str = None) -> Dict[str, Any]:
    """
    Generate content using Mistral AI.
    
    Supported models (2025):
    - mistral-large-latest (recommended)
    - mistral-small-latest (fast, cost-effective)
    - open-mixtral-8x22b (open)
    """
    if not MISTRAL_AVAILABLE:
        return {
            "success": False,
            "error": "mistralai library not installed. Install: pip install mistralai",
            "provider": "mistral",
        }

    api_key = os.getenv("MISTRAL_API_KEY")
    model = model or os.getenv("MISTRAL_MODEL", get_default_model("mistral") or "mistral-large-latest")
    if not api_key:
        return {
            "success": False,
            "error": "MISTRAL_API_KEY not configured",
            "provider": "mistral",
        }

    try:
        if MISTRAL_SDK_MODE == "new":
            client = MistralClient(api_key=api_key)
            response = client.chat(
                model=model,
                messages=[
                    ChatMessage(role="system", content="You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies."),
                    ChatMessage(role="user", content=prompt),
                ],
                temperature=0.7,
                max_tokens=4000,
            )
            content = response.choices[0].message.content if getattr(response, "choices", None) else ""
        else:
            # old SDK fallback
            client = MistralClient(api_key=api_key)
            response = client.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO content writer specializing in topical authority, E-E-A-T, and holistic content strategies."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=4000,
            )
            content = response.choices[0].message.content if response and getattr(response, "choices", None) else ""
        return {
            "success": True,
            "content": content,
            "provider": "mistral",
            "model": model,
            "tokens_used": None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "mistral",
        }

def generate_seo_content(
    topic: str,
    page_type: str = "BLOG",
    main_keyword: str = "",
    secondary_keywords: Optional[List[str]] = None,
    target_location: Optional[str] = None,
    target_audience: Optional[str] = None,
    language: str = "Turkish",
    tone: str = "professional but friendly",
    word_count: int = 1200,
    competitor_urls: Optional[List[str]] = None,
    local_context: Optional[str] = None,
    provider: str = "openai",
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main function to generate SEO-optimized content.
    
    Args:
        topic: Main topic/title for the content
        page_type: SERVICE / BLOG / LANDING PAGE
        main_keyword: Primary SEO keyword
        secondary_keywords: List of secondary keywords
        target_location: City/Country for local SEO
        target_audience: Description of target audience
        language: Content language (default: Turkish)
        tone: Writing tone (default: professional but friendly)
        word_count: Minimum word count (default: 1200)
        competitor_urls: URLs to model structure after
        local_context: Local landmarks/context for regional SEO
        provider: "openai" / "anthropic" / "gemini" (default: openai)
        model: Specific model name (optional, uses provider default if not specified)
    
    Supported Providers & Models (2025):
        OpenAI:
            - gpt-4o (default, recommended)
            - gpt-4o-mini
            - o1-preview
            - o1-mini
        
        Anthropic:
            - claude-3-7-sonnet-20250219 (default, recommended)
            - claude-3-5-sonnet-20241022
            - claude-3-5-haiku-20241022
        
        Google Gemini:
            - gemini-2.0-flash-exp (default, recommended)
            - gemini-1.5-pro
            - gemini-1.5-flash
    
    Returns:
        Dictionary with generated content or error
    """
    if not topic or not main_keyword:
        return {
            "success": False,
            "error": "Topic and main_keyword are required",
        }

    # Build the prompt
    prompt = build_content_prompt(
        topic=topic,
        page_type=page_type,
        main_keyword=main_keyword,
        secondary_keywords=secondary_keywords or [],
        target_location=target_location,
        target_audience=target_audience,
        language=language,
        tone=tone,
        word_count=word_count,
        competitor_urls=competitor_urls,
        local_context=local_context,
    )

    # Generate content with selected provider
    provider_lower = provider.lower()
    
    if provider_lower == "anthropic":
        result = generate_content_claude(prompt, model=model) if model else generate_content_claude(prompt)
    elif provider_lower == "gemini":
        result = generate_content_gemini(prompt, model=model) if model else generate_content_gemini(prompt)
    elif provider_lower == "mistral":
        result = generate_content_mistral(prompt, model=model) if model else generate_content_mistral(prompt)
    else:  # default to openai
        result = generate_content_openai(prompt, model=model) if model else generate_content_openai(prompt)

    # Add metadata
    if result.get("success"):
        result["metadata"] = {
            "topic": topic,
            "page_type": page_type,
            "main_keyword": main_keyword,
            "secondary_keywords": secondary_keywords,
            "language": language,
            "target_word_count": word_count,
        }

    return result
