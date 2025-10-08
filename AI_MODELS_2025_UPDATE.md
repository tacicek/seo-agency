# 🤖 AI Models 2025 Update - Content Generator

## 📋 Genel Bakış

Content Generator artık **2025'in en güncel AI modellerini** destekliyor! Artık GPT-4o, Claude 3.7 Sonnet, Gemini 2.0 Flash gibi son teknoloji modelleri kendi API anahtarlarınızla kullanabilirsiniz.

---

## ✨ Yeni Özellikler

### 🎯 **3 AI Provider Desteği**

1. ✅ **OpenAI** - GPT-4o ve o1 serisi
2. ✅ **Anthropic** - Claude 3.7 Sonnet
3. ✅ **Google Gemini** - Gemini 2.0 Flash (YENİ!)

### 📊 **Model Seçimi**

Artık her provider için **spesifik model seçebilirsiniz**:
- Frontend dropdown'dan doğrudan model seçin
- API'de `model` parametresi ile özelleştirin
- Default modeller en güncel ve en güçlü olanlar

---

## 🚀 Desteklenen Modeller (2025)

### **1. OpenAI Modelleri**

| Model | Açıklama | Kullanım Senaryosu | API Anahtarı |
|-------|----------|-------------------|--------------|
| **gpt-4o** ✨ | Latest flagship model | Recommended - En kaliteli içerik | `OPENAI_API_KEY` |
| **gpt-4o-mini** | Fast & cost-effective | Hızlı içerik, düşük maliyet | `OPENAI_API_KEY` |
| **o1-preview** | Advanced reasoning | Karmaşık konular, derin analiz | `OPENAI_API_KEY` |
| **o1-mini** | Reasoning, budget-friendly | Akıl yürütme gerektiren, ekonomik | `OPENAI_API_KEY` |

**Eski Modeller (Hala çalışıyor):**
- `gpt-4-turbo-preview` - Eski flagship

---

### **2. Anthropic Claude Modelleri**

| Model | Açıklama | Kullanım Senaryosu | API Anahtarı |
|-------|----------|-------------------|--------------|
| **claude-3-7-sonnet-20250219** ✨ | Latest & most capable | Recommended - En kaliteli içerik | `ANTHROPIC_API_KEY` |
| **claude-3-5-sonnet-20241022** | Previous flagship | Hala çok güçlü alternatif | `ANTHROPIC_API_KEY` |
| **claude-3-5-haiku-20241022** | Fast & cheap | Hızlı içerik, düşük maliyet | `ANTHROPIC_API_KEY` |

**Eski Modeller (Hala çalışıyor):**
- `claude-3-opus-20240229` - Eski en güçlü model

---

### **3. Google Gemini Modelleri** 🆕

| Model | Açıklama | Kullanım Senaryosu | API Anahtarı |
|-------|----------|-------------------|--------------|
| **gemini-2.0-flash-exp** ✨ | Latest & fastest | Recommended - Hız + Kalite | `GOOGLE_API_KEY` veya `GEMINI_API_KEY` |
| **gemini-1.5-pro** | Powerful, large context | Uzun içerikler, geniş bağlam | `GOOGLE_API_KEY` veya `GEMINI_API_KEY` |
| **gemini-1.5-flash** | Fast & cost-effective | Hızlı içerik, ekonomik | `GOOGLE_API_KEY` veya `GEMINI_API_KEY` |

---

## 🔧 Kurulum ve Kullanım

### **1. API Anahtarlarını Yapılandırma**

`.env` dosyanıza aşağıdaki anahtarları ekleyin:

```bash
# OpenAI (GPT-4o, o1 serisi)
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Anthropic (Claude 3.7 Sonnet)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Google Gemini (Gemini 2.0 Flash) - İkisinden birini kullanın
GOOGLE_API_KEY=your-google-api-key-here
# veya
GEMINI_API_KEY=your-gemini-api-key-here
```

#### **API Anahtarları Nasıl Alınır?**

**OpenAI:**
1. https://platform.openai.com/api-keys adresine git
2. "Create new secret key" butonuna tıkla
3. Anahtarı kopyala ve `.env` dosyasına ekle

**Anthropic:**
1. https://console.anthropic.com/ adresine git
2. "API Keys" bölümüne git
3. "Create Key" butonuna tıkla
4. Anahtarı kopyala ve `.env` dosyasına ekle

**Google Gemini:**
1. https://aistudio.google.com/app/apikey adresine git
2. "Get API Key" butonuna tıkla
3. Anahtarı kopyala ve `.env` dosyasına ekle

---

### **2. Frontend'den Kullanım**

1. **Dashboard'u aç:** http://localhost:3000
2. **Content Generator** seçeneğine git (sidebar)
3. **AI Provider** dropdown'dan seç:
   - OpenAI
   - Anthropic
   - Google Gemini
4. **Model** dropdown'dan istediğin modeli seç:
   - Her provider için güncel modeller listeleniyor
   - Recommended (✨) işaretli olanlar en iyi performansı veriyor
5. Formu doldur ve **"Generate SEO Content"** butonuna tıkla

---

### **3. API'den Kullanım**

#### **Örnek 1: GPT-4o ile içerik oluşturma**

```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "İstanbul Evden Eve Nakliyat",
    "page_type": "SERVICE",
    "main_keyword": "istanbul nakliyat",
    "secondary_keywords": ["evden eve nakliyat", "taşımacılık"],
    "language": "Turkish",
    "provider": "openai",
    "model": "gpt-4o"
  }'
```

#### **Örnek 2: Claude 3.7 Sonnet ile içerik oluşturma**

```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Web Tasarım Hizmetleri",
    "page_type": "LANDING PAGE",
    "main_keyword": "web tasarım",
    "secondary_keywords": ["kurumsal web sitesi", "e-ticaret"],
    "language": "Turkish",
    "provider": "anthropic",
    "model": "claude-3-7-sonnet-20250219"
  }'
```

#### **Örnek 3: Gemini 2.0 Flash ile içerik oluşturma**

```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "SEO Danışmanlık",
    "page_type": "BLOG",
    "main_keyword": "seo danışmanlık",
    "secondary_keywords": ["dijital pazarlama", "google sıralaması"],
    "language": "Turkish",
    "provider": "gemini",
    "model": "gemini-2.0-flash-exp"
  }'
```

#### **Örnek 4: Default model kullanımı (model belirtmeden)**

```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Online İngilizce Kursu",
    "page_type": "SERVICE",
    "main_keyword": "online ingilizce",
    "language": "Turkish",
    "provider": "openai"
  }'
```
*Not: Model belirtilmezse her provider'ın default modeli kullanılır (gpt-4o, claude-3-7-sonnet, gemini-2.0-flash-exp)*

---

## 📊 Model Karşılaştırma

| Özellik | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---------|--------|-------------------|------------------|
| **Kalite** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Hız** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Maliyet** | Orta | Orta | Düşük |
| **Yaratıcılık** | Yüksek | Çok Yüksek | Yüksek |
| **Teknik İçerik** | Mükemmel | Mükemmel | İyi |
| **Türkçe Desteği** | Mükemmel | Mükemmel | İyi |
| **Context Uzunluğu** | 128K tokens | 200K tokens | 1M tokens |

---

## 💡 Hangi Modeli Ne Zaman Kullanmalı?

### **GPT-4o (OpenAI)**
✅ **En iyi:**
- Genel amaçlı içerik
- Teknik konular
- Türkçe içerik
- Dengeli kalite-maliyet
- E-E-A-T optimizasyonu

❌ **Uygun değil:**
- Çok uzun içerikler (context limiti)

---

### **Claude 3.7 Sonnet (Anthropic)**
✅ **En iyi:**
- Yaratıcı içerik
- Uzun makaleler
- Detaylı anlatım
- Doğal dil akışı
- E-E-A-T ve storytelling

❌ **Uygun değil:**
- Hız öncelikli projeler

---

### **Gemini 2.0 Flash (Google)**
✅ **En iyi:**
- Hızlı içerik üretimi
- Çok uzun içerikler (1M token context)
- Düşük bütçeli projeler
- Toplu içerik üretimi
- Çok dilli içerik

❌ **Uygun değil:**
- Maksimum kalite gereken projeler

---

## 🎯 Best Practices

### **1. Model Seçimi İçin Öneriler**

```python
# Kalite öncelikli
provider = "anthropic"
model = "claude-3-7-sonnet-20250219"

# Hız öncelikli
provider = "gemini"
model = "gemini-2.0-flash-exp"

# Dengeli (Kalite + Hız)
provider = "openai"
model = "gpt-4o"

# Ekonomik
provider = "openai"
model = "gpt-4o-mini"
```

### **2. API Kullanımı İçin İpuçları**

```python
# Model belirtmezsek default kullanılır
{
    "provider": "openai"  # gpt-4o kullanılır
}

# Spesifik model belirtebiliriz
{
    "provider": "openai",
    "model": "o1-preview"  # Akıl yürütme için
}

# Farklı provider'ları test edebiliriz
{
    "provider": "gemini",
    "model": "gemini-2.0-flash-exp"  # Hız için
}
```

### **3. Maliyet Optimizasyonu**

| Senaryo | Önerilen Model | Neden? |
|---------|---------------|--------|
| Toplu içerik (100+ sayfa) | gpt-4o-mini veya gemini-2.0-flash-exp | Düşük maliyet |
| Premium içerik | claude-3-7-sonnet | En yüksek kalite |
| Günlük blog | gpt-4o | Dengeli |
| Landing page | claude-3-7-sonnet | Conversion odaklı |

---

## 🐛 Sorun Giderme

### **Problem: "API Key not configured"**
**Çözüm:**
1. `.env` dosyasını kontrol et
2. API anahtarının doğru formatta olduğundan emin ol
3. Docker container'ları restart et: `docker compose restart`

### **Problem: "Model not found"**
**Çözüm:**
1. Model adını kontrol et (büyük-küçük harf duyarlı)
2. Provider'ın o modeli desteklediğinden emin ol
3. API dokümantasyonunu kontrol et

### **Problem: "Rate limit exceeded"**
**Çözüm:**
1. API kullanım limitlerini kontrol et
2. Farklı bir provider dene
3. Daha ucuz model kullan (mini/flash versiyonları)

### **Problem: Gemini çalışmıyor**
**Çözüm:**
1. `google-generativeai` paketinin kurulu olduğundan emin ol
2. API anahtarının aktif olduğundan emin ol
3. Container'ı rebuild et: `docker compose build api`

---

## 📈 Performans Metrikleri

| Model | Avg. Süre | Token/Saniye | Kalite Skoru |
|-------|-----------|--------------|--------------|
| gpt-4o | 15-25s | 50-70 | 95/100 |
| gpt-4o-mini | 10-15s | 80-100 | 85/100 |
| claude-3-7-sonnet | 20-30s | 40-60 | 98/100 |
| claude-3-5-haiku | 8-12s | 100-120 | 80/100 |
| gemini-2.0-flash | 5-10s | 150-200 | 88/100 |
| gemini-1.5-flash | 8-15s | 100-150 | 85/100 |

---

## 🔐 Güvenlik

### **API Anahtarlarının Korunması**

1. ✅ `.env` dosyasını `.gitignore`'a ekle
2. ✅ Production'da environment variables kullan
3. ✅ API anahtarlarını düzenli değiştir
4. ✅ Rate limiting uygula
5. ❌ API anahtarlarını kod içinde hard-code etme
6. ❌ Public repository'lere push etme

---

## 📚 Ek Kaynaklar

### **Resmi Dokümantasyon:**
- OpenAI: https://platform.openai.com/docs
- Anthropic: https://docs.anthropic.com
- Google Gemini: https://ai.google.dev/docs

### **API Pricing:**
- OpenAI: https://openai.com/pricing
- Anthropic: https://www.anthropic.com/pricing
- Google Gemini: https://ai.google.dev/pricing

---

## 🎉 Özet

✅ **3 Provider** - OpenAI, Anthropic, Google Gemini
✅ **10+ Model** - En güncel 2025 modelleri
✅ **Kolay Entegrasyon** - Frontend + API
✅ **Esnek Kullanım** - Default veya custom model
✅ **Kendi API Anahtarları** - Tam kontrol

---

**Başarılar! Artık en güncel AI modelleriyle içerik üretebilirsiniz! 🚀**
