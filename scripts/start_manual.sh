#!/bin/bash

# Manuel başlatma scripti (Docker olmadan)

echo "🚀 SEO Analyzer - Manuel Başlatma"
echo "====================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 kurulu değil!"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js kurulu değil!"
    echo "   Kurulum: brew install node"
    exit 1
fi

echo "✅ Python3 bulundu: $(python3 --version)"
echo "✅ Node.js bulundu: $(node --version)"
echo ""

echo "📦 Backend başlatılıyor..."
echo ""

# Start backend in background
cd apps/api
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r requirements.txt --quiet
echo "🔧 Backend başlatılıyor (port 8000)..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ../..

sleep 3

echo ""
echo "📦 Frontend başlatılıyor..."
echo ""

# Start frontend
cd apps/web
npm install --silent 2>/dev/null
echo "🔧 Frontend başlatılıyor (port 3000)..."
npm run dev &
FRONTEND_PID=$!
cd ../..

echo ""
echo "✅ Sistem başlatıldı!"
echo ""
echo "📍 Erişim:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "⏹️  Durdurmak için: Ctrl+C"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '⏹️  Sistem durduruluyor...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
