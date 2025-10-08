# 🔗 MOZ API Entegrasyonu

## ✅ Durum: Tamamlandı!

MOZ API başarıyla sisteme entegre edildi.

---

## 📊 Sağlanan Metrikler

MOZ API aşağıdaki SEO metriklerini sağlar:

### 1. **Domain Authority (DA)**
- 0-100 arası skor
- Domain'in genel otoritesi
- Yüksek DA = Daha güvenilir site

### 2. **Page Authority (PA)**
- 0-100 arası skor
- Belirli bir sayfanın otoritesi
- Arama motorlarında sıralama potansiyeli

### 3. **Spam Score**
- 0-100 arası skor
- Sitenin spam olma olasılığı
- Düşük spam score = Daha iyi

### 4. **Backlink Metrikleri**
- Root domains linking (Kaç farklı domain link veriyor)
- External links (Toplam dış link sayısı)
- Link kalite metrikleri (MozRank, MozTrust)

### 5. **SEO Score**
- Otomatik hesaplanan genel skor
- DA, PA ve Spam Score'dan türetilir

---

## 🔧 Yapılan Değişiklikler

### 1. Yeni Dosyalar:
- ✅ `apps/api/analyzers/moz.py` - MOZ API analyzer modülü
- ✅ `scripts/test_moz.py` - MOZ API test scripti

### 2. Güncellenmiş Dosyalar:
- ✅ `apps/api/main.py` - MOZ entegrasyonu eklendi
- ✅ `.env` - MOZ API credentials eklendi

### 3. Yeni API Endpoints:
- ✅ `GET /moz/test` - MOZ API bağlantı testi
- ✅ `POST /analyze` - Artık MOZ metriklerini de içeriyor

---

## 🧪 Test Etme

### Terminal'den Test:

```bash
cd /Users/tuncaycicek/Desktop/seo-analyzer-starter
python3 scripts/test_moz.py
```

### API Üzerinden Test:

1. **Sistemi başlatın:**
   ```bash
   ./scripts/start_manual.sh
   ```

2. **MOZ bağlantısını test edin:**
   ```bash
   curl http://localhost:8000/moz/test
   ```

3. **Tam analiz yapın:**
   ```bash
   curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
   ```

---

## 📋 API Response Örneği

Artık `/analyze` endpoint'i şu yapıyı döndürür:

```json
{
  "reportId": "1234567890",
  "report": {
    "url": "https://example.com",
    "onpage": { ... },
    "keywords": { ... },
    "performance": { ... },
    "moz": {
      "backlink_metrics": {
        "domain_authority": 93,
        "page_authority": 96,
        "spam_score": 1,
        "seo_score": 93.55,
        "root_domains_linking": 5287,
        "external_links": 15234
      },
      "link_quality": {
        "mozrank": 8.5,
        "moztrust": 9.2
      },
      "full_metrics": { ... }
    }
  }
}
```

---

## 🔍 Endpoint Detayları

### GET /moz/test

MOZ API bağlantısını test eder.

**Response:**
```json
{
  "status": "success",
  "message": "MOZ API connection successful",
  "test_metrics": {
    "domain_authority": 93,
    "page_authority": 96
  }
}
```

### POST /analyze

URL analizi yapar (artık MOZ metrikleriyle birlikte).

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:** Yukarıdaki örneğe bakın.

---

## ⚠️ Önemli Notlar

### Rate Limits
- MOZ API'nin kullanım limitleri vardır
- Ücretsiz plan: Ayda ~10,000 sorgu
- Rate limit aşımında `429` hatası döner

### Error Handling
- Credentials yoksa: Analiz devam eder, sadece MOZ kısmı error döner
- API hatası: Diğer metrikler etkilenmez
- Timeout: 30 saniye sonra timeout

### Güvenlik
- API keys `.env` dosyasında saklanır
- `.env` dosyası **asla** git'e commit edilmemeli
- Credentials'ları kimseyle paylaşmayın

---

## 📈 Kullanım Senaryoları

### 1. Competitor Analizi
```python
# Rakip site analizi
result = get_backlink_summary("https://competitor.com")
print(f"Rakip DA: {result['backlink_metrics']['domain_authority']}")
```

### 2. Link Building Hedefleri
```python
# Yüksek DA'lı siteleri belirle
if result['backlink_metrics']['domain_authority'] > 50:
    print("Değerli backlink hedefi!")
```

### 3. Spam Kontrolü
```python
# Spam sitelerden kaçın
if result['backlink_metrics']['spam_score'] > 30:
    print("⚠️ Yüksek spam riski!")
```

---

## 🚀 Gelecek Geliştirmeler

### Planlanabilecek Özellikler:

1. **Link Explorer**
   - Backlink listesi
   - Anchor text analizi
   - Link velocity

2. **Competitor Comparison**
   - Birden fazla domain karşılaştırma
   - Grafik görselleştirme

3. **Historical Data**
   - DA/PA değişim grafiği
   - Trend analizi

4. **Batch Analysis**
   - Toplu URL analizi
   - CSV export

---

## 📚 MOZ API Dökümantasyonu

Resmi döküman: https://moz.com/api/v2/url-metrics

---

**Oluşturma Tarihi:** 7 Ekim 2025  
**Durum:** ✅ Aktif ve Kullanıma Hazır
