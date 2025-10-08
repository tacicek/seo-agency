# 🐳 Docker Desktop Kurulum Rehberi (Apple Silicon için)

## 🎯 Neden Docker?

Docker, uygulamanızı ve tüm bağımlılıklarını bir "konteyner" içinde çalıştırır.
Bu sayede:
- ✅ Hiçbir şey kurmanıza gerek yok (Python, Node.js, vs.)
- ✅ Her şey izole çalışır
- ✅ Tek komutla başlatıp durdurabilirsiniz
- ✅ Farklı bilgisayarlarda aynı şekilde çalışır

---

## 📥 Adım 1: Docker Desktop İndir

### Otomatik İndirme (Tarayıcıda açılacak):

Terminal'de şunu çalıştırın:
```bash
open "https://desktop.docker.com/mac/main/arm64/Docker.dmg"
```

### Manuel İndirme:

Bu linki tarayıcınıza kopyalayın:
```
https://desktop.docker.com/mac/main/arm64/Docker.dmg
```

📦 Dosya boyutu: ~600 MB (birkaç dakika sürebilir)

---

## 📦 Adım 2: Docker Desktop'ı Kur

### 2.1. DMG Dosyasını Aç
1. İndirilen **Docker.dmg** dosyasına çift tıklayın
2. Yeni bir pencere açılacak

### 2.2. Applications Klasörüne Sürükle
1. **Docker** ikonunu göreceksiniz
2. Onu **Applications** klasörüne **sürükleyin**
3. Birkaç saniye bekleyin (kopyalanıyor)

### 2.3. İlk Çalıştırma
1. **Applications** klasörünü açın (Finder → Applications)
2. **Docker** uygulamasını bulun
3. **Çift tıklayın** veya sağ tıklayıp "Open" seçin
4. "Are you sure?" derse → **"Open"** tıklayın

---

## ⚙️ Adım 3: Docker'ı Başlat

### 3.1. İlk Açılış
Docker Desktop açılınca:
1. "Docker Desktop needs privileged access" derse → **Şifrenizi girin**
2. "Terms of Service" çıkarsa → **Accept** tıklayın
3. "Skip tutorial" seçebilirsiniz

### 3.2. Docker'ın Hazır Olmasını Bekleyin
Docker simgesi menü çubuğunda (üst bar) görünecek:
- 🟡 **Sarı/Turuncu**: Docker başlıyor (bekleyin)
- 🟢 **Yeşil**: Docker hazır! ✅

**İpucu:** İlk başlangıç 1-2 dakika sürebilir.

---

## ✅ Adım 4: Docker'ın Çalıştığını Kontrol Et

Terminal'de şunu çalıştırın:
```bash
docker --version
```

Şöyle bir çıktı görmelisiniz:
```
Docker version 24.x.x, build ...
```

✅ Gördüyseniz Docker hazır!

---

## 🚀 Adım 5: SEO Analyzer'ı Başlat

Artık sistemi başlatabilirsiniz:

```bash
cd /Users/tuncaycicek/Desktop/seo-analyzer-starter
docker compose up --build
```

**Ne olacak:**
- Docker, gerekli tüm yazılımları indirecek (ilk seferinde)
- API'yi başlatacak (port 8000)
- Web uygulamasını başlatacak (port 3000)
- İlk seferinde 5-10 dakika sürebilir

**Tamamlandığında göreceksiniz:**
```
✔ Container seo-api  Started
✔ Container seo-web  Started
```

---

## 🌐 Adım 6: Uygulamayı Kullan

Terminal'de "Started" mesajlarını gördükten sonra:

**Tarayıcınızda açın:**
```
http://localhost:3000
```

🎉 **SEO Analyzer çalışıyor!**

---

## 🛑 Durdurmak İçin

Terminal'de:
- **Ctrl+C** tuşlarına basın

Tamamen temizlemek için:
```bash
docker compose down
```

---

## 📝 Önemli Notlar

### Docker Desktop'ı Her Açışta:
- Bilgisayarı başlattığınızda Docker otomatik başlamayabilir
- Applications'dan Docker'ı manuel açmanız gerekebilir
- Veya Docker ayarlarından "Start Docker Desktop when you log in" seçeneğini aktifleştirin

### İlk Çalıştırma:
- İlk `docker compose up` komutunda her şeyi indirecek
- 5-10 dakika sürebilir
- Sonraki başlatmalar çok daha hızlı olacak (saniyeler)

### Sorun mu var?
1. Docker Desktop'ın açık olduğundan emin olun (menü çubuğunda 🐳)
2. Docker'ın yeşil 🟢 olduğundan emin olun
3. Terminal'de şunu deneyin: `docker ps`

---

## 🎬 Özet - 6 Basit Adım

1. ⬇️ **Docker.dmg'yi indir** → `open "https://desktop.docker.com/mac/main/arm64/Docker.dmg"`
2. 📦 **Kur** → Docker'ı Applications'a sürükle
3. 🚀 **Aç** → Applications → Docker (çift tıkla)
4. ⏳ **Bekle** → Yeşil 🟢 olana kadar
5. ✅ **Test et** → `docker --version`
6. 🎉 **Başlat** → `docker compose up --build`

---

**Şimdi ne yapacağız?**

1. Docker'ı indirmek için linki açalım mı?
2. Yoksa zaten Docker kurulu mu kontrol edelim mi?

Hazırsanız, bir sonraki adımı söyleyin! 😊
