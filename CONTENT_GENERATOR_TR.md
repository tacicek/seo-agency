# 🎨 AI Content Generator - Hızlı Başlangıç Kılavuzu

## 📋 Genel Bakış

**AI Content Generator**, E-E-A-T optimize edilmiş, konusal ve bütünsel SEO içerikleri üreten güçlü bir araçtır. GPT-4 ve Claude 3.5 Sonnet gibi gelişmiş AI modelleri kullanarak %100 insan eliyle yazılmış gibi görünen içerikler oluşturur.

---

## ✨ Özellikler

- ✅ **E-E-A-T Optimizasyonu** (Deneyim, Uzmanlık, Otorite, Güvenilirlik)
- ✅ **Topical SEO Stratejisi** ile semantik keyword entegrasyonu
- ✅ **Holistik Kullanıcı Niyeti Kapsamı** tüm müşteri yolculuğu aşamaları için
- ✅ **%100 insan gibi içerik** gelişmiş prompt mühendisliği ile
- ✅ **Çok dilli destek** (Türkçe, İngilizce, Almanca, vb.)
- ✅ **Esnek sayfa tipleri**: Hizmet Sayfası, Blog Yazısı, Landing Page

---

## 🚀 Nasıl Kullanılır?

### 1. Dashboard Üzerinden Kullanım

1. **Dashboard'a git:** `http://localhost:3000`
2. **Sidebar'dan "Content Generator" seçeneğine tıkla**
3. **Formu doldur:**
   - Topic (Konu) *
   - Main Keyword (Ana Anahtar Kelime) *
   - Secondary Keywords (İkincil Anahtar Kelimeler)
   - Target Location (Hedef Konum)
   - Word Count (Kelime Sayısı)
   - vs.
4. **"Generate SEO Content" butonuna tıkla**
5. **İçeriği kopyala ve kullan! 📋**

### 2. API ile Kullanım

```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "İstanbul Evden Eve Nakliyat - Profesyonel Taşıma Hizmeti",
    "page_type": "SERVICE",
    "main_keyword": "istanbul nakliyat",
    "secondary_keywords": ["evden eve nakliyat", "taşımacılık", "eşya taşıma"],
    "target_location": "İstanbul, Türkiye",
    "target_audience": "İstanbul'da taşınmak isteyen aileler ve kurumsal firmalar",
    "language": "Turkish",
    "tone": "professional but friendly",
    "word_count": 1500,
    "local_context": "Kadıköy, Beşiktaş, Şişli gibi merkezi bölgeler",
    "provider": "openai"
  }'
```

---

## 📝 Form Alanları

### Zorunlu Alanlar (*)
- **Topic (Konu)***: İçeriğin ana konusu
  - Örnek: "İstanbul Evden Eve Nakliyat - Profesyonel Taşıma Hizmeti"
- **Main Keyword (Ana Anahtar Kelime)***: SEO için birincil keyword
  - Örnek: "istanbul nakliyat"

### Opsiyonel Alanlar
- **Page Type (Sayfa Tipi)**: SERVICE / BLOG / LANDING PAGE
- **Secondary Keywords (İkincil Kelimeler)**: Virgülle ayrılmış ek keywordler
  - Örnek: "evden eve nakliyat, taşımacılık, eşya taşıma"
- **Target Location (Hedef Konum)**: Coğrafi odak noktası
  - Örnek: "İstanbul, Türkiye"
- **Target Audience (Hedef Kitle)**: İçeriğin hedef kitlesi
  - Örnek: "İstanbul'da taşınmak isteyen aileler ve profesyoneller"
- **Language (Dil)**: İçerik dili (Turkish / English / German)
- **Tone (Ton)**: İçeriğin tonu (professional / casual / technical)
- **Word Count (Kelime Sayısı)**: Hedef kelime sayısı (800-3000)
- **Competitor URLs (Rakip URL'leri)**: Rakip sitelerden örnekler
- **Local Context (Yerel Bağlam)**: Yerel detaylar ve özellikler
- **AI Provider (AI Sağlayıcısı)**: openai (GPT-4) / anthropic (Claude 3.5)

---

## 🎯 Oluşturulan İçerik - Yapısı

### 1. Meta Etiketleri
- Meta Title (55-60 karakter)
- Meta Description (150-160 karakter)

### 2. Başlık Hiyerarşisi
- H1 (Ana başlık)
- H2 (Bölüm başlıkları)
- H3 (Alt bölümler)

### 3. İçerik Bölümleri
- **Giriş**: Problem tanımı ve değer önerisi
- **Ana Bölüm**: Topical kapsam ve semantik keywordler
- **SSS (FAQ)**: Sıkça sorulan sorular (5-7 soru)
- **CTA**: Dönüşüm odaklı eylem çağrısı

### 4. SEO Optimizasyonu
- Keyword yoğunluğu: Ana keyword için %1-2
- Keyword varyasyonları
- İç link önerileri
- LSI keyword entegrasyonu
- E-E-A-T sinyalleri

---

## 💡 Örnek Kullanımlar

### Örnek 1: Hizmet Sayfası
```json
{
  "topic": "İstanbul Web Tasarım Hizmetleri - Kurumsal ve E-ticaret",
  "page_type": "SERVICE",
  "main_keyword": "web tasarım istanbul",
  "secondary_keywords": ["kurumsal web sitesi", "e-ticaret sitesi", "responsive tasarım"],
  "target_location": "İstanbul, Türkiye",
  "target_audience": "KOBİ'ler ve startup'lar",
  "language": "Turkish",
  "word_count": 1500,
  "local_context": "Kadıköy, Beşiktaş, Şişli merkezi iş bölgeleri",
  "provider": "openai"
}
```

### Örnek 2: Blog Yazısı
```json
{
  "topic": "2025'te SEO Trendleri ve Dijital Pazarlama Stratejileri",
  "page_type": "BLOG",
  "main_keyword": "seo trendleri 2025",
  "secondary_keywords": ["dijital pazarlama", "google algoritması", "yapay zeka seo"],
  "target_audience": "Dijital pazarlamacılar ve web site sahipleri",
  "language": "Turkish",
  "tone": "educational but engaging",
  "word_count": 2000,
  "provider": "anthropic"
}
```

### Örnek 3: Landing Page
```json
{
  "topic": "Online İngilizce Kursu - İngilizce Öğrenmenin En Hızlı Yolu",
  "page_type": "LANDING PAGE",
  "main_keyword": "online ingilizce kursu",
  "secondary_keywords": ["ingilizce öğren", "online eğitim", "canlı ders"],
  "target_audience": "İngilizce öğrenmek isteyen öğrenciler ve çalışanlar",
  "language": "Turkish",
  "tone": "motivating and friendly",
  "word_count": 1200,
  "provider": "openai"
}
```

---

## 🔧 Teknik Gereksinimler

### API Anahtarları
`.env` dosyasında şu anahtarlar tanımlanmalı:

```bash
# OpenAI (GPT-4)
OPENAI_API_KEY=sk-proj-your-key-here

# Anthropic (Claude 3.5) - Opsiyonel
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Docker Container'ları Başlatma
```bash
# Container'ları durdur
docker compose down

# Yeniden build et
docker compose build

# Başlat
docker compose up -d

# Logları kontrol et
docker compose logs -f api
```

---

## 📊 Performans Metrikleri

| Metrik | Değer |
|--------|-------|
| Ortalama Üretim Süresi | 15-30 saniye |
| Token Kullanımı (GPT-4) | 1200-2000 Token |
| Token Kullanımı (Claude 3.5) | 1500-2500 Token |
| Maksimum Kelime Sayısı | 3000 kelime |
| Desteklenen Diller | 50+ dil |

---

## 🎯 En İyi Uygulamalar

### ✅ YAPILMASI GEREKENLER
1. **Detaylı konu başlığı**: "İstanbul Web Tasarım - KOBİ'ler için Özel Çözümler"
2. **3-5 ikincil keyword**: Ana kelimeye semantik olarak ilişkili
3. **Spesifik hedef kitle**: "Kadıköy'deki küçük işletmeler"
4. **Yerel bağlam ekleme**: "Bağdat Caddesi, Moda, Caddebostan"
5. **2-3 rakip URL**: Yüksek kaliteli içerikler

### ❌ YAPILMAMASI GEREKENLER
1. Kısa ve belirsiz konular: "Web tasarım"
2. Tek keyword kullanımı
3. Genel hedef kitle: "herkes"
4. Genel konum: "Türkiye"
5. 10+ rakip URL veya hiç URL yok

---

## 🐛 Sorun Giderme

### "API Key Missing" Hatası
**Çözüm:** `.env` dosyasında `OPENAI_API_KEY` veya `ANTHROPIC_API_KEY` anahtarlarını tanımlayın.

### İçerik Çok Kısa
**Çözüm:** 
- `word_count` değerini artırın
- Daha fazla `secondary_keywords` ekleyin
- `local_context` alanını doldurun

### İçerik Genel ve Sıradan
**Çözüm:**
- Detaylı `local_context` ekleyin
- Daha spesifik `target_audience` tanımlayın
- `competitor_urls` ile referans verin

### Timeout Hatası
**Çözüm:**
- `word_count` değerini 2000'in altına düşürün
- Farklı bir `provider` deneyin (anthropic → openai)

---

## 📞 Yardım

### Logları Kontrol Etme
```bash
# API logları
docker compose logs -f api

# Web logları
docker compose logs -f web

# Tüm loglar
docker compose logs -f
```

### API Dökümantasyonu
Tarayıcıda aç: `http://localhost:8000/docs`

### Endpoint Testi
```bash
# Health check
curl http://localhost:8000/health

# Content generator test
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{"topic":"Test","page_type":"BLOG","main_keyword":"test","provider":"openai"}'
```

---

## 🎓 İpuçları

1. **İlk kullanımda kısa içerikle başlayın** (800-1000 kelime)
2. **Farklı tonları deneyin**: professional / casual / technical
3. **Her iki AI provider'ı test edin**: GPT-4 vs Claude 3.5
4. **Oluşturulan içeriği gözden geçirin** ve ihtiyaç halinde düzenleyin
5. **Yerel SEO için mutlaka konum bilgisi ekleyin**

---

## 🚀 Sonraki Adımlar

1. ✅ Dashboard'da Content Generator'ı aç
2. ✅ İlk test içeriğini oluştur
3. ✅ Parametreleri optimize et
4. ✅ API'yi iş akışına entegre et
5. ✅ Özel promptlar geliştir

---

**Başarılar! İçerik üretimi çok daha kolay olacak! 🎉**
