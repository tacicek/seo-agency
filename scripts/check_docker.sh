#!/bin/bash

# Docker kurulum kontrolü ve yardımcı script

echo "🐳 Docker Kurulum Asistanı"
echo "================================"
echo ""

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo "✅ Docker zaten kurulu!"
    echo ""
    docker --version
    echo ""
    
    # Check if Docker is running
    if docker ps &> /dev/null; then
        echo "✅ Docker çalışıyor!"
        echo ""
        echo "🎉 Sistem başlatmaya hazır!"
        echo ""
        echo "Başlatmak için:"
        echo "  docker compose up --build"
        echo ""
        exit 0
    else
        echo "⚠️  Docker kurulu ama çalışmıyor"
        echo ""
        echo "Lütfen Docker Desktop'ı başlatın:"
        echo "  1. Applications klasörünü açın"
        echo "  2. Docker'a çift tıklayın"
        echo "  3. Yeşil 🟢 olana kadar bekleyin"
        echo "  4. Bu scripti tekrar çalıştırın"
        echo ""
        exit 1
    fi
else
    echo "❌ Docker kurulu değil"
    echo ""
    echo "📥 Docker Desktop İndirme:"
    echo ""
    echo "Apple Silicon Mac (M1/M2/M3) için:"
    echo "  https://desktop.docker.com/mac/main/arm64/Docker.dmg"
    echo ""
    echo "📋 Kurulum Adımları:"
    echo ""
    echo "1. Yukarıdaki linke gidin (veya çalıştırın: open 'https://desktop.docker.com/mac/main/arm64/Docker.dmg')"
    echo "2. Docker.dmg dosyasını indirin (~600 MB)"
    echo "3. İndirilen dosyaya çift tıklayın"
    echo "4. Docker ikonunu Applications klasörüne sürükleyin"
    echo "5. Applications'dan Docker'ı başlatın"
    echo "6. Yeşil 🟢 olana kadar bekleyin"
    echo "7. Bu scripti tekrar çalıştırın"
    echo ""
    echo "Detaylı rehber: DOCKER_KURULUM.md"
    echo ""
fi
