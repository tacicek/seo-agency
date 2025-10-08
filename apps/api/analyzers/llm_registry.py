"""
Central LLM Model Registry
Keeps latest stable models per provider with metadata (version, capabilities, stability)
"""

from typing import Dict, List, Any


LLM_REGISTRY: Dict[str, Dict[str, Any]] = {
    "openai": {
        "default": "gpt-5",
        "models": [
            {
                "id": "gpt-5",
                "name": "GPT-5",
                "version": "latest",
                "stable": True,
                "capabilities": ["topical-eeat", "reasoning", "long-form"],
                "recommended": True,
            },
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "version": "stable",
                "stable": True,
                "capabilities": ["multimodal", "cost-efficient"],
                "recommended": True,
            },
            {
                "id": "gpt-4o-mini",
                "name": "GPT-4o Mini",
                "version": "stable",
                "stable": True,
                "capabilities": ["fast", "budget"],
                "recommended": False,
            },
        ],
    },
    "anthropic": {
        "default": "claude-4.5-sonnet",
        "models": [
            {
                "id": "claude-4.5-sonnet",
                "name": "Claude 4.5 Sonnet",
                "version": "latest",
                "stable": True,
                "capabilities": ["holistic-structured", "long-form", "tools"],
                "recommended": True,
            },
            {
                "id": "claude-3-7-sonnet-20250219",
                "name": "Claude 3.7 Sonnet",
                "version": "2025-02-19",
                "stable": True,
                "capabilities": ["high-quality", "structured"],
                "recommended": True,
            },
        ],
    },
    "gemini": {
        "default": "gemini-2.0-pro",
        "models": [
            {
                "id": "gemini-2.0-pro",
                "name": "Gemini 2.0 Pro",
                "version": "latest",
                "stable": True,
                "capabilities": ["evidence-grounded", "data-driven", "long-context"],
                "recommended": True,
            },
            {
                "id": "gemini-2.0-flash-exp",
                "name": "Gemini 2.0 Flash (exp)",
                "version": "experimental",
                "stable": False,
                "capabilities": ["fast"],
                "recommended": False,
            },
            {
                "id": "gemini-1.5-pro",
                "name": "Gemini 1.5 Pro",
                "version": "stable",
                "stable": True,
                "capabilities": ["large-context", "quality"],
                "recommended": False,
            },
        ],
    },
    "mistral": {
        "default": "mistral-large-latest",
        "models": [
            {
                "id": "mistral-large-latest",
                "name": "Mistral Large (latest)",
                "version": "latest",
                "stable": True,
                "capabilities": ["general", "fast"],
                "recommended": True,
            }
        ],
    },
}


def get_default_model(provider: str) -> str:
    reg = LLM_REGISTRY.get(provider, {})
    models = reg.get("models", [])
    # Prefer models marked as latest and stable
    for m in models:
        if m.get("version") == "latest" and m.get("stable"):
            return m.get("id", "")
    # Otherwise, prefer stable recommended models
    for m in models:
        if m.get("stable") and m.get("recommended"):
            return m.get("id", "")
    # Fallback to static default if present
    return reg.get("default", "")


def get_recommended_models(provider: str) -> List[str]:
    models = LLM_REGISTRY.get(provider, {}).get("models", [])
    return [m["id"] for m in models if m.get("stable") and (m.get("recommended") or m["id"] == LLM_REGISTRY[provider]["default"])]


def get_registry_snapshot() -> Dict[str, Any]:
    return LLM_REGISTRY
