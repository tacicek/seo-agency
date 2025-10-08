#!/bin/bash
# Quick test script for SEO Analyzer

echo "🧪 Testing SEO Analyzer Installation..."
echo "========================================"
echo ""

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if container exists
if ! docker ps | grep -q "seo-api"; then
    echo "⚠️  API container not found. Starting containers..."
    cd "$(dirname "$0")"
    docker compose up -d
    echo "⏳ Waiting for containers to be ready..."
    sleep 10
fi

echo "✅ API container is running"
echo ""

# Test 1: Check Python version
echo "Test 1: Python version"
docker exec seo-api python --version
echo ""

# Test 2: Check if required packages are installed
echo "Test 2: Checking installed packages..."
docker exec seo-api python -c "
import sys
packages = [
    ('sentence_transformers', 'Sentence Transformers'),
    ('bertopic', 'BERTopic'),
    ('keybert', 'KeyBERT'),
    ('umap', 'UMAP'),
    ('hdbscan', 'HDBSCAN'),
    ('whois', 'Python-WHOIS'),
    ('tldextract', 'tldextract'),
    ('plotly', 'Plotly'),
]

success = 0
failed = 0

for module, name in packages:
    try:
        __import__(module)
        print(f'  ✅ {name}')
        success += 1
    except ImportError:
        print(f'  ❌ {name} - NOT INSTALLED')
        failed += 1

print()
print(f'Result: {success}/{len(packages)} packages installed')
if failed > 0:
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Some packages are missing. Please rebuild Docker container."
    exit 1
fi

echo ""

# Test 3: Check if seo_analyzer.py exists
echo "Test 3: Checking seo_analyzer.py..."
if docker exec seo-api test -f seo_analyzer.py; then
    echo "  ✅ seo_analyzer.py found"
else
    echo "  ❌ seo_analyzer.py not found"
    exit 1
fi

echo ""

# Test 4: Syntax check
echo "Test 4: Python syntax check..."
docker exec seo-api python -m py_compile seo_analyzer.py
if [ $? -eq 0 ]; then
    echo "  ✅ No syntax errors"
else
    echo "  ❌ Syntax errors found"
    exit 1
fi

echo ""

# Test 5: Import test
echo "Test 5: Module import test..."
docker exec seo-api python -c "
from seo_analyzer import SEOAnalyzer
print('  ✅ SEOAnalyzer class imported successfully')
"

if [ $? -ne 0 ]; then
    echo "  ❌ Failed to import SEOAnalyzer"
    exit 1
fi

echo ""

# Test 6: Quick functional test (with a simple site)
echo "Test 6: Quick functional test..."
echo "  Running mini analysis on example.com (5 pages)..."
echo ""

docker exec seo-api python -c "
import os
os.environ['MOZ_ACCESS_ID'] = 'mozscape-8u2uAjdQpV'
os.environ['MOZ_SECRET_KEY'] = 'MCeFg5jtmrLGcpNlNOUfOrX0G7RLttZC'

from seo_analyzer import SEOAnalyzer

try:
    print('  Initializing analyzer...')
    analyzer = SEOAnalyzer()
    
    print('  Crawling 5 pages...')
    pages = analyzer.crawl_website('https://example.com', max_pages=5)
    print(f'  ✅ Crawled {len(pages)} pages')
    
    if len(pages) > 0:
        print('  Extracting topics...')
        topics = analyzer.extract_topics(pages, min_topic_size=1)
        print(f'  ✅ Found {topics.get(\"total_topics\", 0)} topics')
        
        print('  Analyzing domain...')
        metrics = analyzer.analyze_domain('example.com')
        print(f'  ✅ Domain analysis complete')
        
        print('  Calculating score...')
        score = analyzer.calculate_topical_authority_score(topics, metrics)
        print(f'  ✅ Score: {score[\"topical_authority_score\"]} ({score[\"grade\"]})')
        
        print()
        print('  🎉 All tests passed!')
    else:
        print('  ⚠️  No pages crawled, but no errors')
        
except Exception as e:
    print(f'  ❌ Error: {str(e)}')
    import traceback
    traceback.print_exc()
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✅ ALL TESTS PASSED!"
    echo "========================================"
    echo ""
    echo "You can now run:"
    echo "  docker exec -it seo-api python seo_analyzer.py https://yoursite.com"
    echo ""
    echo "Or use the example script:"
    echo "  docker exec -it seo-api python example_usage.py https://yoursite.com"
    echo ""
else
    echo ""
    echo "========================================"
    echo "❌ TESTS FAILED"
    echo "========================================"
    exit 1
fi
