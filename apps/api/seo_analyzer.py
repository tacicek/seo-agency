#!/usr/bin/env python3
"""
Advanced SEO Analyzer with Topical Analysis and Domain Authority Estimation

This script performs comprehensive SEO analysis including:
- Website crawling and content extraction
- Topical clustering using BERTopic
- Semantic keyword extraction using KeyBERT
- Domain authority analysis via Moz API
- Custom Topical Authority Score calculation
- Visual report generation

Author: SEO Analysis Team
Date: October 2025
"""

import os
import sys
import json
import time
import hashlib
import hmac
import base64
import whois
import tldextract
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from urllib.parse import urljoin, urlparse
from collections import Counter

# Web scraping
import requests
from bs4 import BeautifulSoup

# NLP and Topic Modeling
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from keybert import KeyBERT
import umap
import hdbscan

# Data processing and ML
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Visualization
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuration
MAX_PAGES = 20  # Maximum number of pages to crawl
REQUEST_TIMEOUT = 10  # Seconds
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


class SEOAnalyzer:
    """Main SEO Analysis class with topical analysis and DA estimation"""
    
    def __init__(self, moz_access_id: str = None, moz_secret_key: str = None):
        """
        Initialize the SEO Analyzer
        
        Args:
            moz_access_id: Moz API Access ID
            moz_secret_key: Moz API Secret Key
        """
        self.moz_access_id = moz_access_id or os.getenv('MOZ_ACCESS_ID')
        self.moz_secret_key = moz_secret_key or os.getenv('MOZ_SECRET_KEY')
        
        # Initialize NLP models
        print("🔄 Loading NLP models...")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.keybert_model = KeyBERT(model=self.sentence_model)
        
        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
        print("✅ SEO Analyzer initialized successfully!")
    
    
    def crawl_website(self, url: str, max_pages: int = MAX_PAGES) -> List[Dict[str, Any]]:
        """
        Crawl website and extract content from multiple pages
        
        Args:
            url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl
            
        Returns:
            List of dictionaries containing page data
        """
        print(f"\n🕷️  Crawling website: {url}")
        
        visited = set()
        to_visit = [url]
        pages_data = []
        
        # Parse base domain
        parsed_base = urlparse(url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
        
        while to_visit and len(pages_data) < max_pages:
            current_url = to_visit.pop(0)
            
            if current_url in visited:
                continue
            
            try:
                print(f"  📄 Crawling: {current_url}")
                response = self.session.get(current_url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                visited.add(current_url)
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract content
                title = soup.find('title')
                title = title.get_text().strip() if title else ""
                
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                meta_desc = meta_desc.get('content', '').strip() if meta_desc else ""
                
                # Extract body text (remove scripts, styles)
                for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                    script.decompose()
                
                body_text = soup.get_text(separator=' ', strip=True)
                body_text = ' '.join(body_text.split())[:5000]  # Limit to 5000 chars
                
                # Combine all text
                full_text = f"{title}. {meta_desc}. {body_text}"
                
                if len(full_text.strip()) > 50:  # Only save pages with substantial content
                    pages_data.append({
                        'url': current_url,
                        'title': title,
                        'meta_description': meta_desc,
                        'body_text': body_text,
                        'full_text': full_text,
                        'word_count': len(full_text.split())
                    })
                
                # Find internal links
                if len(pages_data) < max_pages:
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)
                        
                        # Only follow internal links
                        if full_url.startswith(base_domain) and full_url not in visited:
                            to_visit.append(full_url)
                
                time.sleep(0.5)  # Be polite
                
            except Exception as e:
                print(f"  ⚠️  Error crawling {current_url}: {str(e)}")
                continue
        
        print(f"✅ Crawled {len(pages_data)} pages successfully!")
        return pages_data
    
    
    def extract_topics(self, pages_data: List[Dict[str, Any]], 
                      min_topic_size: int = 2) -> Dict[str, Any]:
        """
        Extract topics from page content using BERTopic
        
        Args:
            pages_data: List of page data dictionaries
            min_topic_size: Minimum number of documents per topic
            
        Returns:
            Dictionary containing topics, keywords, and metadata
        """
        print("\n🧠 Performing topical analysis...")
        
        if not pages_data:
            return {'error': 'No pages to analyze'}
        
        # Extract texts
        texts = [page['full_text'] for page in pages_data]
        urls = [page['url'] for page in pages_data]
        
        # Generate embeddings
        print("  🔢 Generating sentence embeddings...")
        embeddings = self.sentence_model.encode(texts, show_progress_bar=True)
        
        # Configure UMAP and HDBSCAN for BERTopic
        umap_model = umap.UMAP(
            n_neighbors=min(15, len(texts) - 1),
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            random_state=42
        )
        
        hdbscan_model = hdbscan.HDBSCAN(
            min_cluster_size=min_topic_size,
            metric='euclidean',
            cluster_selection_method='eom',
            prediction_data=True
        )
        
        # Create BERTopic model
        topic_model = BERTopic(
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            language='english',
            calculate_probabilities=True,
            verbose=True
        )
        
        # Fit the model
        print("  🔍 Clustering topics with BERTopic...")
        topics, probs = topic_model.fit_transform(texts, embeddings)
        
        # Get topic info
        topic_info = topic_model.get_topic_info()
        
        # Extract keywords for each topic using KeyBERT
        print("  🔑 Extracting semantic keywords with KeyBERT...")
        topic_results = []
        
        for topic_id in topic_info['Topic'].values:
            if topic_id == -1:  # Skip outlier topic
                continue
            
            # Get documents in this topic
            topic_docs = [texts[i] for i, t in enumerate(topics) if t == topic_id]
            topic_urls = [urls[i] for i, t in enumerate(topics) if t == topic_id]
            
            if not topic_docs:
                continue
            
            # Combine documents for keyword extraction
            combined_text = ' '.join(topic_docs)[:10000]  # Limit text size
            
            # Extract keywords using KeyBERT
            keywords = self.keybert_model.extract_keywords(
                combined_text,
                keyphrase_ngram_range=(1, 3),
                stop_words='english',
                top_n=10,
                use_maxsum=True,
                nr_candidates=20,
                diversity=0.5
            )
            
            # Get topic representation from BERTopic
            topic_words = topic_model.get_topic(topic_id)
            bertopic_keywords = [word for word, score in topic_words[:10]] if topic_words else []
            
            topic_results.append({
                'topic_id': int(topic_id),
                'document_count': len(topic_docs),
                'keybert_keywords': [{'keyword': kw, 'score': float(score)} for kw, score in keywords],
                'bertopic_keywords': bertopic_keywords,
                'sample_urls': topic_urls[:3],
                'representative_text': topic_docs[0][:200] + '...' if topic_docs else ''
            })
        
        # Calculate topical consistency
        topic_distribution = Counter(topics)
        total_docs = len([t for t in topics if t != -1])
        
        if total_docs > 0:
            # Shannon entropy for topic diversity
            topic_probs = [count / total_docs for count in topic_distribution.values() if count > 0]
            entropy = -sum(p * np.log(p) for p in topic_probs if p > 0)
            max_entropy = np.log(len(topic_probs)) if len(topic_probs) > 1 else 1
            topical_consistency = 1 - (entropy / max_entropy if max_entropy > 0 else 0)
        else:
            topical_consistency = 0
        
        # Calculate semantic relevance (average cosine similarity within topics)
        semantic_relevance = self._calculate_semantic_relevance(embeddings, topics)
        
        print(f"✅ Found {len(topic_results)} distinct topics!")
        
        return {
            'topics': topic_results,
            'total_documents': len(texts),
            'total_topics': len(topic_results),
            'outliers': topic_distribution.get(-1, 0),
            'topical_consistency': float(topical_consistency),
            'semantic_relevance': float(semantic_relevance),
            'embeddings': embeddings.tolist(),
            'topic_assignments': [int(t) for t in topics]
        }
    
    
    def _calculate_semantic_relevance(self, embeddings: np.ndarray, 
                                     topics: List[int]) -> float:
        """
        Calculate average semantic relevance within topics
        
        Args:
            embeddings: Document embeddings
            topics: Topic assignments
            
        Returns:
            Average cosine similarity within topics
        """
        similarities = []
        
        for topic_id in set(topics):
            if topic_id == -1:  # Skip outliers
                continue
            
            topic_embeddings = embeddings[[i for i, t in enumerate(topics) if t == topic_id]]
            
            if len(topic_embeddings) > 1:
                # Calculate pairwise cosine similarities
                sim_matrix = cosine_similarity(topic_embeddings)
                # Get upper triangle (excluding diagonal)
                upper_tri = sim_matrix[np.triu_indices_from(sim_matrix, k=1)]
                if len(upper_tri) > 0:
                    similarities.extend(upper_tri)
        
        return float(np.mean(similarities)) if similarities else 0.0
    
    
    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """
        Analyze domain authority and metrics
        
        Args:
            domain: Domain to analyze (e.g., 'example.com')
            
        Returns:
            Dictionary containing domain metrics
        """
        print(f"\n🔍 Analyzing domain: {domain}")
        
        metrics = {
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract clean domain
        extracted = tldextract.extract(domain)
        clean_domain = f"{extracted.domain}.{extracted.suffix}"
        
        # 1. Get MOZ metrics
        if self.moz_access_id and self.moz_secret_key:
            print("  📊 Fetching Moz metrics...")
            moz_data = self._get_moz_metrics(clean_domain)
            metrics['moz'] = moz_data
        else:
            print("  ⚠️  Moz API credentials not found, skipping...")
            metrics['moz'] = {}
        
        # 2. Get WHOIS data
        try:
            print("  🔎 Fetching WHOIS data...")
            w = whois.whois(clean_domain)
            
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                domain_age_days = (datetime.now() - creation_date).days
                domain_age_years = domain_age_days / 365.25
            else:
                domain_age_days = None
                domain_age_years = None
            
            metrics['whois'] = {
                'registrar': w.registrar,
                'creation_date': creation_date.isoformat() if creation_date else None,
                'expiration_date': w.expiration_date[0].isoformat() if isinstance(w.expiration_date, list) and w.expiration_date else None,
                'domain_age_days': domain_age_days,
                'domain_age_years': round(domain_age_years, 2) if domain_age_years else None,
                'name_servers': w.name_servers if w.name_servers else []
            }
        except Exception as e:
            print(f"  ⚠️  WHOIS lookup failed: {str(e)}")
            metrics['whois'] = {'error': str(e)}
        
        # 3. Domain structure analysis
        metrics['domain_structure'] = {
            'subdomain': extracted.subdomain,
            'domain': extracted.domain,
            'suffix': extracted.suffix,
            'is_subdomain': bool(extracted.subdomain),
            'tld_category': self._categorize_tld(extracted.suffix)
        }
        
        print("✅ Domain analysis complete!")
        return metrics
    
    
    def _get_moz_metrics(self, domain: str) -> Dict[str, Any]:
        """
        Fetch metrics from Moz API
        
        Args:
            domain: Domain to analyze
            
        Returns:
            Dictionary with Moz metrics
        """
        try:
            # Moz API endpoint
            url = "https://lsapi.seomoz.com/v2/url_metrics"
            
            # Create expires timestamp (5 minutes from now)
            expires = int(time.time() + 300)
            
            # Create signature
            string_to_sign = f"{self.moz_access_id}\n{expires}"
            binary_signature = hmac.new(
                self.moz_secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
            signature = base64.b64encode(binary_signature).decode('utf-8')
            
            # Headers
            headers = {
                'Content-Type': 'application/json'
            }
            
            # Request body
            payload = {
                "targets": [domain],
            }
            
            # Make request
            auth = (self.moz_access_id, signature)
            response = requests.post(
                f"{url}?Expires={expires}",
                json=payload,
                headers=headers,
                auth=auth,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    result = data['results'][0]
                    
                    return {
                        'domain_authority': result.get('domain_authority', 0),
                        'page_authority': result.get('page_authority', 0),
                        'spam_score': result.get('spam_score', 0),
                        'root_domains_linking': result.get('root_domains_to_root_domain', 0),
                        'external_links': result.get('external_links_to_root_domain', 0),
                        'pages_to_root': result.get('pages_to_root_domain', 0),
                        'status': 'success'
                    }
            
            return {
                'status': 'error',
                'message': f"API returned status {response.status_code}",
                'response': response.text[:200]
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    
    def _categorize_tld(self, tld: str) -> str:
        """Categorize TLD type"""
        generic = ['com', 'net', 'org', 'info', 'biz']
        country = ['uk', 'de', 'fr', 'jp', 'cn', 'in', 'br', 'au']
        
        if tld in generic:
            return 'generic'
        elif tld in country:
            return 'country_code'
        else:
            return 'other'
    
    
    def calculate_topical_authority_score(self, topic_data: Dict[str, Any], 
                                         domain_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate custom Topical Authority Score
        
        Formula: (semantic_relevance + topical_consistency + backlink_quality) / 3
        
        Args:
            topic_data: Results from extract_topics()
            domain_metrics: Results from analyze_domain()
            
        Returns:
            Dictionary with score breakdown
        """
        print("\n🎯 Calculating Topical Authority Score...")
        
        # 1. Semantic Relevance (0-100)
        semantic_relevance = topic_data.get('semantic_relevance', 0) * 100
        
        # 2. Topical Consistency (0-100)
        topical_consistency = topic_data.get('topical_consistency', 0) * 100
        
        # 3. Backlink Quality Score (0-100)
        moz = domain_metrics.get('moz', {})
        
        if moz.get('status') == 'success':
            da = moz.get('domain_authority', 0)
            spam = moz.get('spam_score', 0)
            root_domains = moz.get('root_domains_linking', 0)
            
            # Normalize and weight backlink factors
            da_normalized = min(da, 100)
            spam_penalty = max(0, 100 - (spam * 2))  # Spam score penalizes
            backlink_score = min(np.log1p(root_domains) * 10, 100)  # Log scale
            
            backlink_quality = (da_normalized * 0.5 + spam_penalty * 0.2 + backlink_score * 0.3)
        else:
            backlink_quality = 50  # Default if Moz data unavailable
        
        # 4. Domain Age Bonus (0-10 bonus points)
        whois = domain_metrics.get('whois', {})
        domain_age_years = whois.get('domain_age_years', 0)
        age_bonus = min(domain_age_years * 2, 10) if domain_age_years else 0
        
        # Calculate final score
        base_score = (semantic_relevance + topical_consistency + backlink_quality) / 3
        final_score = min(base_score + age_bonus, 100)
        
        # Determine grade
        if final_score >= 90:
            grade = 'A+'
        elif final_score >= 80:
            grade = 'A'
        elif final_score >= 70:
            grade = 'B'
        elif final_score >= 60:
            grade = 'C'
        elif final_score >= 50:
            grade = 'D'
        else:
            grade = 'F'
        
        result = {
            'topical_authority_score': round(final_score, 2),
            'grade': grade,
            'components': {
                'semantic_relevance': round(semantic_relevance, 2),
                'topical_consistency': round(topical_consistency, 2),
                'backlink_quality': round(backlink_quality, 2),
                'domain_age_bonus': round(age_bonus, 2)
            },
            'interpretation': self._interpret_score(final_score)
        }
        
        print(f"✅ Topical Authority Score: {final_score:.2f} ({grade})")
        return result
    
    
    def _interpret_score(self, score: float) -> str:
        """Provide interpretation for the score"""
        if score >= 90:
            return "Exceptional topical authority with strong content focus and authoritative backlinks"
        elif score >= 80:
            return "Strong topical authority with good content coherence and solid domain metrics"
        elif score >= 70:
            return "Good topical authority with room for improvement in content focus or backlinks"
        elif score >= 60:
            return "Moderate topical authority; consider improving content consistency and link building"
        elif score >= 50:
            return "Fair topical authority; significant improvements needed in multiple areas"
        else:
            return "Weak topical authority; requires comprehensive SEO strategy overhaul"
    
    
    def generate_report(self, url: str, pages_data: List[Dict[str, Any]], 
                       topic_data: Dict[str, Any], domain_metrics: Dict[str, Any],
                       authority_score: Dict[str, Any]) -> None:
        """
        Generate comprehensive HTML and JSON reports with visualizations
        
        Args:
            url: Original URL analyzed
            pages_data: Crawled pages data
            topic_data: Topic analysis results
            domain_metrics: Domain metrics
            authority_score: Topical authority score
        """
        print("\n📊 Generating reports...")
        
        # 1. Save topics.json
        topics_output = {
            'url': url,
            'analysis_date': datetime.now().isoformat(),
            'total_pages_analyzed': len(pages_data),
            'topics': topic_data.get('topics', []),
            'metrics': {
                'total_topics': topic_data.get('total_topics', 0),
                'outliers': topic_data.get('outliers', 0),
                'topical_consistency': topic_data.get('topical_consistency', 0),
                'semantic_relevance': topic_data.get('semantic_relevance', 0)
            }
        }
        
        with open('topics.json', 'w', encoding='utf-8') as f:
            json.dump(topics_output, f, indent=2, ensure_ascii=False)
        print("  ✅ Saved topics.json")
        
        # 2. Save domain_metrics.json
        with open('domain_metrics.json', 'w', encoding='utf-8') as f:
            json.dump(domain_metrics, f, indent=2, ensure_ascii=False)
        print("  ✅ Saved domain_metrics.json")
        
        # 3. Create visualizations
        self._create_visualizations(topic_data, domain_metrics, authority_score)
        
        # 4. Generate HTML report
        self._generate_html_report(url, pages_data, topic_data, domain_metrics, authority_score)
        
        print("✅ All reports generated successfully!")
        print("\n📁 Output files:")
        print("  - topics.json")
        print("  - domain_metrics.json")
        print("  - report.html")
        print("  - topic_distribution.png")
        print("  - authority_breakdown.png")
    
    
    def _create_visualizations(self, topic_data: Dict[str, Any], 
                              domain_metrics: Dict[str, Any],
                              authority_score: Dict[str, Any]) -> None:
        """Create visualization charts"""
        
        # 1. Topic Distribution Pie Chart
        topics = topic_data.get('topics', [])
        if topics:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Pie chart
            labels = [f"Topic {t['topic_id']}" for t in topics]
            sizes = [t['document_count'] for t in topics]
            colors = plt.cm.Set3(range(len(topics)))
            
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Topic Distribution', fontsize=14, fontweight='bold')
            
            # Bar chart for top keywords
            ax2.axis('off')
            y_pos = 0.9
            ax2.text(0.5, 0.95, 'Top Topics & Keywords', ha='center', 
                    fontsize=12, fontweight='bold', transform=ax2.transAxes)
            
            for i, topic in enumerate(topics[:5]):
                keywords = [kw['keyword'] for kw in topic['keybert_keywords'][:3]]
                text = f"Topic {topic['topic_id']}: {', '.join(keywords)}"
                ax2.text(0.1, y_pos, text, fontsize=9, transform=ax2.transAxes)
                y_pos -= 0.15
            
            plt.tight_layout()
            plt.savefig('topic_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  ✅ Saved topic_distribution.png")
        
        # 2. Authority Score Breakdown
        components = authority_score.get('components', {})
        if components:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            categories = list(components.keys())
            values = list(components.values())
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
            
            bars = ax.barh(categories, values, color=colors)
            ax.set_xlabel('Score', fontsize=12, fontweight='bold')
            ax.set_title(f'Topical Authority Score Breakdown\nOverall Score: {authority_score["topical_authority_score"]} ({authority_score["grade"]})', 
                        fontsize=14, fontweight='bold')
            ax.set_xlim(0, 100)
            
            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax.text(val + 2, i, f'{val:.1f}', va='center', fontsize=10)
            
            plt.tight_layout()
            plt.savefig('authority_breakdown.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  ✅ Saved authority_breakdown.png")
    
    
    def _generate_html_report(self, url: str, pages_data: List[Dict[str, Any]],
                             topic_data: Dict[str, Any], domain_metrics: Dict[str, Any],
                             authority_score: Dict[str, Any]) -> None:
        """Generate comprehensive HTML report"""
        
        moz = domain_metrics.get('moz', {})
        whois = domain_metrics.get('whois', {})
        topics = topic_data.get('topics', [])
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report - {url}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2563eb;
            margin-bottom: 10px;
            font-size: 32px;
        }}
        h2 {{
            color: #1e40af;
            margin: 30px 0 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3b82f6;
        }}
        h3 {{
            color: #3730a3;
            margin: 20px 0 10px;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        .score-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
        .score-card .score {{
            font-size: 72px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .score-card .grade {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }}
        .metric-card .label {{
            color: #64748b;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .metric-card .value {{
            font-size: 28px;
            font-weight: bold;
            color: #1e293b;
        }}
        .topic-card {{
            background: #f1f5f9;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #8b5cf6;
        }}
        .keyword-tag {{
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 5px 12px;
            border-radius: 20px;
            margin: 5px;
            font-size: 13px;
        }}
        .status-success {{
            color: #16a34a;
            font-weight: bold;
        }}
        .status-warning {{
            color: #ea580c;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
        }}
        .component-bar {{
            background: #e2e8f0;
            height: 30px;
            border-radius: 5px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .component-fill {{
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            height: 100%;
            display: flex;
            align-items: center;
            padding: 0 10px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }}
        .interpretation {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SEO Analysis Report</h1>
        <p class="meta">
            <strong>URL:</strong> {url}<br>
            <strong>Analysis Date:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br>
            <strong>Pages Analyzed:</strong> {len(pages_data)}
        </p>

        <div class="score-card">
            <div class="grade">{authority_score['grade']}</div>
            <div class="score">{authority_score['topical_authority_score']}</div>
            <h3 style="margin: 0; font-size: 24px;">Topical Authority Score</h3>
            <p style="margin-top: 15px; font-size: 16px;">{authority_score['interpretation']}</p>
        </div>

        <h2>📊 Score Components</h2>
        <div class="metrics-grid">
"""
        
        # Add component metrics
        for component, value in authority_score['components'].items():
            html += f"""
            <div class="metric-card">
                <div class="label">{component.replace('_', ' ').title()}</div>
                <div class="value">{value:.1f}</div>
                <div class="component-bar">
                    <div class="component-fill" style="width: {value}%">{value:.1f}%</div>
                </div>
            </div>
"""
        
        html += """
        </div>

        <h2>🌐 Domain Metrics</h2>
        <div class="metrics-grid">
"""
        
        # Add Moz metrics
        if moz.get('status') == 'success':
            metrics_to_show = [
                ('Domain Authority', moz.get('domain_authority', 0)),
                ('Page Authority', moz.get('page_authority', 0)),
                ('Spam Score', f"{moz.get('spam_score', 0)}%"),
                ('Root Domains Linking', f"{moz.get('root_domains_linking', 0):,}")
            ]
        else:
            metrics_to_show = [('Moz Data', 'Unavailable')]
        
        # Add WHOIS metrics
        if whois.get('domain_age_years'):
            metrics_to_show.append(('Domain Age', f"{whois['domain_age_years']:.1f} years"))
        
        for label, value in metrics_to_show:
            html += f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
            </div>
"""
        
        html += f"""
        </div>

        <h2>🧠 Topical Analysis</h2>
        <p><strong>Total Topics Identified:</strong> {len(topics)}</p>
        <p><strong>Topical Consistency:</strong> {topic_data.get('topical_consistency', 0) * 100:.1f}%</p>
        <p><strong>Semantic Relevance:</strong> {topic_data.get('semantic_relevance', 0) * 100:.1f}%</p>

        <img src="topic_distribution.png" alt="Topic Distribution">
        <img src="authority_breakdown.png" alt="Authority Score Breakdown">

        <h3>📑 Topic Details</h3>
"""
        
        # Add topic details
        for topic in topics:
            html += f"""
        <div class="topic-card">
            <h4>Topic {topic['topic_id']} ({topic['document_count']} documents)</h4>
            <p><strong>Top KeyBERT Keywords:</strong></p>
            <div>
"""
            for kw in topic['keybert_keywords'][:10]:
                html += f'                <span class="keyword-tag">{kw["keyword"]} ({kw["score"]:.3f})</span>\n'
            
            html += f"""
            </div>
            <p style="margin-top: 10px;"><strong>Sample URL:</strong> <a href="{topic['sample_urls'][0]}" target="_blank">{topic['sample_urls'][0]}</a></p>
            <p style="margin-top: 10px; font-size: 13px; color: #64748b;">{topic['representative_text']}</p>
        </div>
"""
        
        html += f"""
        <h2>📄 Crawled Pages Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Page Title</th>
                    <th>Word Count</th>
                    <th>URL</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for page in pages_data[:20]:  # Show first 20 pages
            html += f"""
                <tr>
                    <td>{page['title'][:80]}</td>
                    <td>{page['word_count']}</td>
                    <td><a href="{page['url']}" target="_blank" style="font-size: 12px;">{page['url'][:50]}...</a></td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>

        <h2>💡 Recommendations</h2>
        <div class="interpretation">
"""
        
        # Generate recommendations
        score = authority_score['topical_authority_score']
        components = authority_score['components']
        
        recommendations = []
        
        if components['semantic_relevance'] < 70:
            recommendations.append("📝 <strong>Improve Content Relevance:</strong> Focus on creating more semantically related content within your main topics.")
        
        if components['topical_consistency'] < 70:
            recommendations.append("🎯 <strong>Increase Topical Consistency:</strong> Narrow your content focus to fewer, more coherent topics.")
        
        if components['backlink_quality'] < 70:
            recommendations.append("🔗 <strong>Build Quality Backlinks:</strong> Focus on acquiring backlinks from authoritative domains in your niche.")
        
        if moz.get('spam_score', 0) > 30:
            recommendations.append("⚠️ <strong>Address Spam Score:</strong> Audit and disavow toxic backlinks immediately.")
        
        if len(topics) < 3:
            recommendations.append("📚 <strong>Expand Content Coverage:</strong> Create more diverse content to establish authority across multiple related topics.")
        
        if not recommendations:
            recommendations.append("✅ <strong>Excellent Work!</strong> Your site demonstrates strong topical authority. Continue monitoring and maintaining your SEO performance.")
        
        for rec in recommendations:
            html += f"            <p style='margin: 10px 0;'>{rec}</p>\n"
        
        html += """
        </div>

        <hr style="margin: 40px 0; border: none; border-top: 2px solid #e2e8f0;">
        <p style="text-align: center; color: #94a3b8; font-size: 13px;">
            Generated by Advanced SEO Analyzer | Powered by BERTopic, KeyBERT & Moz API
        </p>
    </div>
</body>
</html>
"""
        
        with open('report.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("  ✅ Saved report.html")


def main():
    """Main execution function"""
    
    print("="*70)
    print("   🚀 ADVANCED SEO ANALYZER")
    print("   Topical Analysis & Domain Authority Estimation")
    print("="*70)
    
    # Get input URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("\n🌐 Enter website URL to analyze: ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Initialize analyzer
    try:
        analyzer = SEOAnalyzer()
    except Exception as e:
        print(f"❌ Failed to initialize analyzer: {e}")
        return
    
    try:
        # Step 1: Crawl website
        pages_data = analyzer.crawl_website(url, max_pages=MAX_PAGES)
        
        if not pages_data:
            print("❌ No pages could be crawled. Exiting.")
            return
        
        # Step 2: Extract topics
        topic_data = analyzer.extract_topics(pages_data)
        
        # Step 3: Analyze domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        domain_metrics = analyzer.analyze_domain(domain)
        
        # Step 4: Calculate topical authority score
        authority_score = analyzer.calculate_topical_authority_score(topic_data, domain_metrics)
        
        # Step 5: Generate reports
        analyzer.generate_report(url, pages_data, topic_data, domain_metrics, authority_score)
        
        # Print summary to console
        print("\n" + "="*70)
        print("   ✅ ANALYSIS COMPLETE!")
        print("="*70)
        print(f"\n📊 TOPICAL AUTHORITY SCORE: {authority_score['topical_authority_score']} ({authority_score['grade']})")
        print(f"\n📝 Total Pages Analyzed: {len(pages_data)}")
        print(f"🧠 Topics Identified: {topic_data.get('total_topics', 0)}")
        print(f"🔗 Domain Authority: {domain_metrics.get('moz', {}).get('domain_authority', 'N/A')}")
        print(f"📅 Domain Age: {domain_metrics.get('whois', {}).get('domain_age_years', 'N/A')} years")
        
        print("\n💡 Interpretation:")
        print(f"   {authority_score['interpretation']}")
        
        print("\n" + "="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
