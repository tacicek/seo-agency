#!/usr/bin/env python3
"""Quick test for SEO keywords analyzer"""

import sys
sys.path.insert(0, '/Users/tuncaycicek/Desktop/seo-analyzer-starter/apps/api')

from analyzers.keywords import analyze_seo_keywords

# Sample content from Nova Stock page
sample_text = """
Nova Stock Transport AG - Umzug Zürich
Umzugsfirma Zürich | Professioneller Umzugsservice

Wir sind Ihre Umzugsfirma in Zürich. Privatumzug, Firmenumzug, Auslandsumzug.
Erfahren Sie mehr über unsere Umzugsdienstleistungen. Kostenlos Angebot einholen.

Unsere Dienstleistungen:
- Privatumzug Zürich
- Firmenumzug und Büroumzug
- Auslandsumzug weltweit
- Möbeltransport und Lagerhaltung
- Einpackservice und Verpackungsmaterial

Kontakt: Nova Stock Transport AG, Zürich
Umzug anfragen | Angebot erhalten | Jetzt buchen
"""

url = "https://www.nova-stock.ch/umzug"
title = "Nova Stock Transport - Umzugsfirma Zürich"

print("Testing SEO Keyword Analysis...")
print("="*60)

result = analyze_seo_keywords(text=sample_text, url=url, title=title, top_n=10)

print(f"\nDetected Topic: {result['detected_topic']}")
print(f"Method: {result['method']}")
print(f"\nRelated Searches ({len(result['related_searches'])}):")
for rs in result['related_searches'][:5]:
    print(f"  - {rs}")

print(f"\nTop SEO Keywords:")
print(f"{'Rank':<6} {'Keyword':<20} {'Score':<10} {'Count':<8}")
print("-"*50)
for i, kw in enumerate(result['seo_keywords'][:10], 1):
    print(f"{i:<6} {kw['keyword']:<20} {kw['relevance_score']:<10} {kw['count_on_page']:<8}")

print("\n" + "="*60)
print("Notice: Generic words like 'stock', 'nova', 'angebot' are")
print("filtered out or ranked lower. Focus is on SEO-relevant terms")
print("like 'umzug', 'zürich', 'firmenumzug', 'privatumzug', etc.")
