# 🇹🇷 Supabase Tablo Oluşturma Rehberi

## 🎯 Amaç
SEO analizlerini saklamak için veritabanında bir tablo oluşturacağız.

---

## 📸 Görsel Adımlar

### Adım 1: Tarayıcıda Supabase'i Açın

1. **Web tarayıcınızı açın** (Chrome, Safari, Firefox)

2. **Bu adresi kopyalayıp adres çubuğuna yapıştırın:**
   ```
   https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new
   ```

3. **Enter'a basın**

---

### Adım 2: Giriş Yapın (Gerekirse)

Eğer giriş yapmadıysanız:
- Email ve şifrenizi girin
- "Sign in" butonuna tıklayın

---

### Adım 3: SQL Editor Ekranı

Şöyle bir ekran göreceksiniz:

```
┌─────────────────────────────────────────────────────────────┐
│ Supabase Dashboard                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sol Menü:                                                  │
│  • Table Editor                                             │
│  • SQL Editor  ← BU SAYFADA OLACAKSINIZ                   │
│  • Database                                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SQL Editor - New Query                                     │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │                                                    │    │
│  │  [BURAYA SQL KODU YAPIŞTIRACAKSINIZ]              │    │
│  │                                                    │    │
│  │                                                    │    │
│  │                                                    │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│                                   [▶ RUN] ← BURAYA TIKLA  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Adım 4: SQL Kodunu Yapıştırın

Büyük beyaz kutunun içine **tıklayın** ve şu kodu **yapıştırın** (Cmd+V veya Ctrl+V):

```sql
create table if not exists public.seo_reports (
  id text primary key,
  payload jsonb not null,
  created_at timestamp with time zone default now()
);
```

---

### Adım 5: Çalıştırın

1. **Sağ altta** veya **sağ üstte** yeşil **"RUN"** butonunu bulun
2. **Butona tıklayın** ▶️
3. **Bekleyin** (1-2 saniye)

---

### Adım 6: Sonuç

Başarılı olduğunda şunu göreceksiniz:

```
✅ Success. No rows returned
```

veya

```
✅ Success
```

**TEBRIKLER!** 🎉 Tablo oluşturuldu!

---

## 🧪 Test Edin

Terminal'e dönün ve şunu çalıştırın:

```bash
./scripts/create_table.sh
```

Şunu görmelisiniz:
```
✅ Table exists! (empty)
🎉 Supabase ist vollständig konfiguriert!
```

---

## ❓ Sorunlar mı var?

### "Table Editor bulamıyorum"
→ Sol menüde **"SQL Editor"** yazısını arayın (📝 ikonu)

### "Permission denied" hatası
→ Doğru Supabase projesinde olduğunuzdan emin olun

### "Already exists" hatası
→ Sorun yok! Tablo zaten var demektir ✅

### Başka bir hata
→ Hatayı tam olarak kopyalayıp bana gönderin

---

## 🎬 Özet - 3 Basit Adım:

1. **Linke git**: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new

2. **Kodu yapıştır**:
   ```sql
   create table if not exists public.seo_reports (
     id text primary key,
     payload jsonb not null,
     created_at timestamp with time zone default now()
   );
   ```

3. **"RUN" butonuna tıkla** ▶️

**HEPSI BU KADAR!** 🎉

---

## 📞 Yardıma ihtiyacınız varsa:

Ekran görüntüsü alıp bana gönderin, size yardımcı olabilirim!
