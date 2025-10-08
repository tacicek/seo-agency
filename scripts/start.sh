#!/bin/bash

# Quick Start Script für SEO Analyzer
# Dieses Script hilft beim Starten des Systems

echo "🚀 SEO Analyzer - Quick Start"
echo "============================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker ist nicht installiert!"
    echo ""
    echo "Bitte installieren Sie Docker Desktop:"
    echo "  https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

echo "✅ Docker ist installiert"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env Datei nicht gefunden!"
    echo ""
    echo "Bitte erstellen Sie die .env Datei:"
    echo "  cp .env.sample .env"
    echo ""
    exit 1
fi

echo "✅ .env Datei gefunden"
echo ""

# Check Supabase configuration
if grep -q "SUPABASE_SERVICE_KEY=$" .env || grep -q "SUPABASE_SERVICE_KEY=\"\"" .env; then
    echo "⚠️  SUPABASE_SERVICE_KEY ist nicht gesetzt"
    echo ""
    echo "Für vollständige Supabase-Integration:"
    echo "  1. Führen Sie aus: ./scripts/setup_supabase.sh"
    echo "  2. Folgen Sie den Anweisungen"
    echo ""
    echo "Das System funktioniert auch ohne - Reports werden lokal gespeichert."
    echo ""
    read -p "Möchten Sie trotzdem fortfahren? (j/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[JjYy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Starte Docker Container..."
echo ""

# Start Docker Compose
if command -v docker-compose &> /dev/null; then
    docker-compose up --build
else
    docker compose up --build
fi
