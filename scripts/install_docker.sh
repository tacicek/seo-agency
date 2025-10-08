#!/bin/bash

# Docker Desktop kurulum yardımcısı

echo "🐳 Docker Desktop Kurulum Rehberi"
echo "=================================="
echo ""
echo "Docker kurulu değil. Docker Desktop'ı yüklemeniz gerekiyor."
echo ""
echo "📥 İndirme Linkleri:"
echo ""
echo "Mac (Intel):     https://desktop.docker.com/mac/main/amd64/Docker.dmg"
echo "Mac (Apple M1+): https://desktop.docker.com/mac/main/arm64/Docker.dmg"
echo ""
echo "veya ana sayfa:  https://www.docker.com/products/docker-desktop"
echo ""
echo "📋 Kurulum Adımları:"
echo ""
echo "1. Yukarıdaki linke tıklayın (Mac tipinize uygun olanı)"
echo "2. Docker.dmg dosyasını indirin"
echo "3. İndirilen dosyayı açın"
echo "4. Docker ikonunu Applications klasörüne sürükleyin"
echo "5. Applications klasöründen Docker'ı başlatın"
echo "6. Docker Desktop açıldıktan sonra şunu çalıştırın:"
echo ""
echo "   ./scripts/start.sh"
echo ""
echo "=================================="
echo ""
echo "💡 Docker Desktop kurulumu birkaç dakika sürebilir."
echo ""

# Detect Mac type
if [ "$(uname -m)" = "arm64" ]; then
    echo "🔍 Sisteminiz: Apple Silicon (M1/M2/M3)"
    echo "👉 Kullanmanız gereken link:"
    echo "   https://desktop.docker.com/mac/main/arm64/Docker.dmg"
else
    echo "🔍 Sisteminiz: Intel Mac"
    echo "👉 Kullanmanız gereken link:"
    echo "   https://desktop.docker.com/mac/main/amd64/Docker.dmg"
fi

echo ""
echo "❓ Yardıma ihtiyacınız varsa, bana söyleyin!"
