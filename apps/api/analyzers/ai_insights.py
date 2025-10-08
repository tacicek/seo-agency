"""
AI-Powered SEO Insights Module

Provides intelligent SEO recommendations using multiple AI providers:
- OpenAI (GPT-4, GPT-3.5)
- Google Gemini
- Anthropic Claude

Features:
- Content optimization suggestions
- Keyword strategy recommendations
- Competitor analysis insights
- Technical SEO recommendations
- Meta tag generation
- Content gap analysis
"""

import os
import json
from typing import Dict, Any, List, Optional
from enum import Enum


class AIProvider(str, Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"


class AIInsightsGenerator:
    """Main class for generating AI-powered SEO insights"""
    
    def __init__(self, provider: AIProvider = AIProvider.OPENAI):
        self.provider = provider
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == AIProvider.OPENAI:
            self._init_openai()
        elif self.provider == AIProvider.GEMINI:
            self._init_gemini()
        elif self.provider == AIProvider.CLAUDE:
            self._init_claude()
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.client = None
                return
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            self.client = None
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                self.client = None
                return
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel('gemini-pro')
        except ImportError:
            self.client = None
    
    def _init_claude(self):
        """Initialize Anthropic Claude client"""
        try:
            from anthropic import Anthropic
            api_key = os.getenv('CLAUDE_API_KEY')
            if not api_key:
                self.client = None
                return
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            self.client = None
    
    def generate_seo_insights(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive SEO insights from analysis data
        
        Args:
            analysis_data: Complete SEO analysis data including:
                - onpage: On-page SEO metrics
                - keywords: Keyword analysis
                - moz: Backlink metrics
                - content_quality: Content analysis
                - competitors: Competitor data (optional)
        
        Returns:
            AI-generated insights and recommendations
        """
        if not self.client:
            return {
                'error': f'{self.provider.value.upper()}_API_KEY not configured',
                'message': 'Please set the appropriate API key environment variable'
            }
        
        prompt = self._build_seo_analysis_prompt(analysis_data)
        
        try:
            if self.provider == AIProvider.OPENAI:
                response = self._query_openai(prompt)
            elif self.provider == AIProvider.GEMINI:
                response = self._query_gemini(prompt)
            elif self.provider == AIProvider.CLAUDE:
                response = self._query_claude(prompt)
            
            return self._parse_ai_response(response, analysis_data)
            
        except Exception as e:
            return {
                'error': str(e),
                'message': f'Failed to generate AI insights using {self.provider.value}'
            }
    
    def _build_seo_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Build comprehensive SEO analysis prompt"""
        
        # Extract key metrics
        onpage = data.get('onpage', {})
        keywords = data.get('keywords', {})
        moz = data.get('moz', {}).get('backlink_metrics', {})
        content = data.get('content_quality', {})
        competitors = data.get('competitors', {})
        
        prompt = f"""As an expert SEO consultant, analyze this website's SEO performance and provide actionable recommendations.

**WEBSITE DATA:**

**On-Page SEO:**
- Title: {onpage.get('title', 'Not found')}
- Meta Description: {onpage.get('meta_description', 'Not found')}
- H1 Count: {len(onpage.get('headings', {}).get('h1', []))}
- Total Images: {len(onpage.get('images', []))}
- Total Links: {len(onpage.get('links', []))}

**Content Metrics:**
- Total Words: {keywords.get('total_words', 0)}
- Unique Words: {content.get('unique_words', 0)}
- Readability Score: {content.get('readability_score', 0)} ({content.get('readability_level', 'Unknown')})
- Diversity Score: {content.get('diversity_score', 0)}%

**Top Keywords:**
{self._format_keywords(keywords.get('top', [])[:5])}

**Authority Metrics (MOZ):**
- Domain Authority: {moz.get('domain_authority', 'N/A')}
- Page Authority: {moz.get('page_authority', 'N/A')}
- Spam Score: {moz.get('spam_score', 'N/A')}%
- Root Domains Linking: {moz.get('root_domains_linking', 'N/A')}

"""

        if competitors.get('top_competitors'):
            prompt += f"""
**Competitor Analysis:**
{self._format_competitors(competitors.get('top_competitors', [])[:3])}
"""

        prompt += """

**REQUIRED ANALYSIS:**

1. **Content Quality Assessment** (1-2 sentences)
   - Overall content quality rating
   - Key strengths and weaknesses

2. **Technical SEO Issues** (3-5 bullet points)
   - Critical issues that need immediate attention
   - Be specific and actionable

3. **Keyword Strategy** (3-5 bullet points)
   - Are current keywords effective?
   - Missing keyword opportunities
   - Keyword optimization suggestions

4. **Backlink Profile** (2-3 sentences)
   - Assessment of current backlink quality
   - Link building recommendations

5. **Competitive Positioning** (if data available, 2-3 sentences)
   - How does this site compare to competitors?
   - Strategic recommendations

6. **Priority Action Items** (5-7 items, ranked by impact)
   - Format: "[Priority Level] Action: Specific task"
   - Priority levels: CRITICAL, HIGH, MEDIUM

7. **Quick Wins** (3-4 items)
   - Easy improvements with immediate impact

8. **Long-term Strategy** (3-4 bullet points)
   - Strategic recommendations for sustained growth

**OUTPUT FORMAT:**
Provide your analysis in a clear, structured JSON format with these sections:
- content_assessment
- technical_issues (array)
- keyword_recommendations (array)
- backlink_strategy
- competitive_insights (if applicable)
- priority_actions (array with priority and action)
- quick_wins (array)
- long_term_strategy (array)
- overall_score (0-100)
- summary (2-3 sentences)

Be specific, actionable, and focus on high-impact recommendations.
"""
        
        return prompt
    
    def _format_keywords(self, keywords: List[Dict]) -> str:
        """Format keywords for prompt"""
        if not keywords:
            return "No keyword data available"
        
        formatted = []
        for kw in keywords:
            formatted.append(f"- {kw.get('word')}: {kw.get('count')} occurrences ({kw.get('percent')}%)")
        return "\n".join(formatted)
    
    def _format_competitors(self, competitors: List[Dict]) -> str:
        """Format competitor data for prompt"""
        if not competitors:
            return "No competitor data available"
        
        formatted = []
        for idx, comp in enumerate(competitors, 1):
            formatted.append(
                f"{idx}. {comp.get('domain')} - "
                f"{comp.get('visibility')}% visibility, "
                f"avg position {comp.get('avg_position')}"
            )
        return "\n".join(formatted)
    
    def _query_openai(self, prompt: str) -> str:
        """Query OpenAI API"""
        response = self.client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert SEO consultant with 15+ years of experience. "
                              "Provide clear, actionable, and data-driven recommendations. "
                              "Always respond in valid JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def _query_gemini(self, prompt: str) -> str:
        """Query Google Gemini API"""
        response = self.client.generate_content(prompt)
        return response.text
    
    def _query_claude(self, prompt: str) -> str:
        """Query Anthropic Claude API"""
        response = self.client.messages.create(
            model=os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229'),
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.content[0].text
    
    def _parse_ai_response(self, response: str, original_data: Dict) -> Dict[str, Any]:
        """Parse and structure AI response"""
        try:
            # Try to extract JSON from response
            import re
            
            # Find JSON in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            
            # Try to parse as JSON
            try:
                parsed = json.loads(response)
            except json.JSONDecodeError:
                # If not valid JSON, create structured response from text
                parsed = {
                    'summary': response[:500],
                    'raw_response': response,
                    'provider': self.provider.value
                }
            
            # Add metadata
            parsed['ai_provider'] = self.provider.value
            parsed['analysis_timestamp'] = original_data.get('timestamp')
            
            return parsed
            
        except Exception as e:
            return {
                'error': f'Failed to parse AI response: {str(e)}',
                'raw_response': response,
                'provider': self.provider.value
            }


def generate_meta_tags(content: str, provider: AIProvider = AIProvider.OPENAI) -> Dict[str, Any]:
    """
    Generate optimized meta title and description using AI
    
    Args:
        content: Page content
        provider: AI provider to use
        
    Returns:
        Generated meta tags with SEO scores
    """
    generator = AIInsightsGenerator(provider)
    
    if not generator.client:
        return {
            'error': f'{provider.value.upper()}_API_KEY not configured'
        }
    
    prompt = f"""Analyze this webpage content and generate optimized SEO meta tags.

**CONTENT SAMPLE:**
{content[:1000]}

**REQUIREMENTS:**
1. Generate 3 variations of meta titles (50-60 characters each)
2. Generate 3 variations of meta descriptions (150-160 characters each)
3. Each should be:
   - Keyword-rich but natural
   - Compelling and click-worthy
   - Accurately describe the content
   - Include a call-to-action when appropriate

**OUTPUT FORMAT (JSON):**
{{
  "titles": [
    {{"text": "Title 1", "length": 55, "keywords": ["keyword1", "keyword2"]}},
    {{"text": "Title 2", "length": 58, "keywords": ["keyword1", "keyword3"]}},
    {{"text": "Title 3", "length": 60, "keywords": ["keyword2", "keyword3"]}}
  ],
  "descriptions": [
    {{"text": "Description 1", "length": 155, "keywords": ["keyword1", "keyword2"]}},
    {{"text": "Description 2", "length": 158, "keywords": ["keyword1", "keyword3"]}},
    {{"text": "Description 3", "length": 160, "keywords": ["keyword2", "keyword3"]}}
  ],
  "primary_keywords": ["keyword1", "keyword2", "keyword3"],
  "recommendations": ["rec1", "rec2"]
}}
"""
    
    try:
        if provider == AIProvider.OPENAI:
            response = generator._query_openai(prompt)
        elif provider == AIProvider.GEMINI:
            response = generator._query_gemini(prompt)
        elif provider == AIProvider.CLAUDE:
            response = generator._query_claude(prompt)
        
        # Parse response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            response = json_match.group(1)
        
        result = json.loads(response)
        result['ai_provider'] = provider.value
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'message': f'Failed to generate meta tags using {provider.value}'
        }


def generate_content_improvements(content: str, keywords: List[str], 
                                  provider: AIProvider = AIProvider.OPENAI) -> Dict[str, Any]:
    """
    Generate content improvement suggestions using AI
    
    Args:
        content: Current page content
        keywords: Target keywords
        provider: AI provider to use
        
    Returns:
        Detailed content improvement suggestions
    """
    generator = AIInsightsGenerator(provider)
    
    if not generator.client:
        return {
            'error': f'{provider.value.upper()}_API_KEY not configured'
        }
    
    prompt = f"""As an expert SEO content strategist, analyze this content and provide improvement suggestions.

**CURRENT CONTENT:**
{content[:2000]}

**TARGET KEYWORDS:**
{', '.join(keywords[:10])}

**ANALYSIS REQUIRED:**

1. **Content Structure** (3-4 bullets)
   - Heading hierarchy issues
   - Paragraph structure
   - Content flow

2. **Keyword Optimization** (4-5 bullets)
   - Current keyword usage
   - Missing keyword opportunities
   - Keyword density issues
   - LSI keywords to add

3. **Readability Improvements** (3-4 bullets)
   - Sentence length issues
   - Complex phrases to simplify
   - Formatting suggestions

4. **Content Gaps** (4-5 bullets)
   - Missing topics to cover
   - Questions readers might have
   - Additional sections to add

5. **Engagement Improvements** (3-4 bullets)
   - How to make content more engaging
   - Call-to-action suggestions
   - Visual content recommendations

6. **Specific Rewrites** (2-3 examples)
   - Show original sentence
   - Provide improved version
   - Explain why it's better

**OUTPUT FORMAT (JSON):**
{{
  "structure_issues": [],
  "keyword_optimization": [],
  "readability_tips": [],
  "content_gaps": [],
  "engagement_tips": [],
  "rewrite_examples": [
    {{"original": "...", "improved": "...", "reason": "..."}}
  ],
  "priority_score": 85,
  "estimated_impact": "High"
}}
"""
    
    try:
        if provider == AIProvider.OPENAI:
            response = generator._query_openai(prompt)
        elif provider == AIProvider.GEMINI:
            response = generator._query_gemini(prompt)
        elif provider == AIProvider.CLAUDE:
            response = generator._query_claude(prompt)
        
        # Parse response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            response = json_match.group(1)
        
        result = json.loads(response)
        result['ai_provider'] = provider.value
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'message': f'Failed to generate content improvements using {provider.value}',
            'raw_response': response if 'response' in locals() else None
        }


def analyze_competitor_content(your_content: str, competitor_url: str, 
                               provider: AIProvider = AIProvider.OPENAI) -> Dict[str, Any]:
    """
    Compare your content with competitor and suggest improvements
    
    Args:
        your_content: Your website content
        competitor_url: Competitor URL to analyze
        provider: AI provider to use
        
    Returns:
        Comparative analysis and recommendations
    """
    # This would integrate with web scraping to get competitor content
    # For now, returns a template response
    
    return {
        'message': 'Competitor content analysis requires web scraping integration',
        'status': 'coming_soon'
    }


# Convenience functions for different AI providers
def get_openai_insights(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get insights using OpenAI"""
    generator = AIInsightsGenerator(AIProvider.OPENAI)
    return generator.generate_seo_insights(analysis_data)


def get_gemini_insights(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get insights using Google Gemini"""
    generator = AIInsightsGenerator(AIProvider.GEMINI)
    return generator.generate_seo_insights(analysis_data)


def get_claude_insights(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get insights using Anthropic Claude"""
    generator = AIInsightsGenerator(AIProvider.CLAUDE)
    return generator.generate_seo_insights(analysis_data)


def get_all_ai_insights(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get insights from all available AI providers and combine them
    
    Returns best insights or fallback to available provider
    """
    results = {}
    
    # Try OpenAI
    if os.getenv('OPENAI_API_KEY'):
        try:
            results['openai'] = get_openai_insights(analysis_data)
        except Exception as e:
            results['openai'] = {'error': str(e)}
    
    # Try Gemini
    if os.getenv('GEMINI_API_KEY'):
        try:
            results['gemini'] = get_gemini_insights(analysis_data)
        except Exception as e:
            results['gemini'] = {'error': str(e)}
    
    # Try Claude
    if os.getenv('CLAUDE_API_KEY'):
        try:
            results['claude'] = get_claude_insights(analysis_data)
        except Exception as e:
            results['claude'] = {'error': str(e)}
    
    # Return best result or combined insights
    if not results:
        return {
            'error': 'No AI provider configured',
            'message': 'Please set at least one of: OPENAI_API_KEY, GEMINI_API_KEY, CLAUDE_API_KEY'
        }
    
    # Find the first successful result
    for provider, result in results.items():
        if 'error' not in result:
            result['primary_provider'] = provider
            result['all_providers_tried'] = list(results.keys())
            return result
    
    # If all failed, return error summary
    return {
        'error': 'All AI providers failed',
        'details': results
    }


if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        'onpage': {
            'title': 'Example Website - Best Services',
            'meta_description': 'We offer the best services',
            'headings': {'h1': ['Welcome'], 'h2': ['Services', 'About']},
            'images': ['img1.jpg', 'img2.jpg'],
            'links': ['link1', 'link2', 'link3']
        },
        'keywords': {
            'total_words': 500,
            'top': [
                {'word': 'services', 'count': 15, 'percent': 3.0},
                {'word': 'quality', 'count': 10, 'percent': 2.0}
            ]
        },
        'moz': {
            'backlink_metrics': {
                'domain_authority': 35,
                'page_authority': 28,
                'spam_score': 5
            }
        },
        'content_quality': {
            'unique_words': 250,
            'readability_score': 60,
            'readability_level': 'Average',
            'diversity_score': 50
        }
    }
    
    print("Testing AI Insights Generator...")
    print("=" * 50)
    
    # Test with available provider
    result = get_all_ai_insights(sample_data)
    print(json.dumps(result, indent=2))
