# tsDice Integration - Quick Reference Card

## ✅ Integration Status

**100% Compatible** - No code changes required

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Required in .env
MONGODB_URI="mongodb://localhost:27017/"
MONGO_DB_NAME="url-shortener"
TSDICE_SHORT_DOMAIN="share.ket.horse"
```

### 2. Deploy

```bash
vercel --prod
```

### 3. Configure DNS

```
Type  Name   Value
CNAME my     cname.vercel-dns.com
CNAME share  cname.vercel-dns.com
```

---

## 📡 API Endpoint

### Request Format

```http
POST /api/tsdice/share
Host: my.ket.horse
Accept: application/json
Content-Type: application/x-www-form-urlencoded

url=https://zophiezlan.github.io/tsdice/#config=...&emojies=🐎🦄🌀✨🎉🪐👽🛸
```

### Response Format

```json
{
  "short_url": "https://share.ket.horse/🐎🦄🌀✨🎉🪐👽🛸"
}
```

---

## 🔧 Test Commands

### Test API

```bash
curl -X POST https://my.ket.horse/api/tsdice/share \
  -H "Accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://example.com&emojies=🎨🎭🎪🎯🎲🎰✨🌟"
```

### Test Redirect

```bash
curl -I https://share.ket.horse/🎨🎭🎪🎯🎲🎰✨🌟
```

---

## 📊 Monitoring URLs

- **Leaderboard:** https://my.ket.horse/tsdice/leaderboard
- **Analytics:** https://my.ket.horse/api/tsdice/analytics
- **Stats:** https://my.ket.horse/stats/{emoji-string}

---

## ⚙️ Key Configuration

| Variable | Value | Purpose |
|----------|-------|---------|
| `TSDICE_SHORT_DOMAIN` | `share.ket.horse` | Short URL domain |
| `TSDICE_API_KEY` | `secret-key` | Rate limit bypass |
| `MONGODB_URI` | MongoDB connection | Database storage |

---

## 🔍 Compatibility Matrix

| Feature | tsDice Sends | API Accepts | Status |
|---------|--------------|-------------|--------|
| Emoji Count | 8 emojis | 1-15 emojis | ✅ |
| Parameter Name | `emojies` | `emojies` | ✅ |
| Content-Type | `x-www-form-urlencoded` | Supported | ✅ |
| Accept Header | `application/json` | Required | ✅ |
| Response Field | `short_url` | `short_url` | ✅ |
| CORS | Required | Enabled | ✅ |
| CSRF | Must bypass | Bypassed | ✅ |

---

## 🛠️ Troubleshooting

### Wrong Domain in short_url

```bash
# Set in Vercel environment variables
TSDICE_SHORT_DOMAIN=share.ket.horse
```

### MongoDB Connection Error

```bash
# Check MongoDB is running
systemctl status mongodb

# Test connection
mongosh "mongodb://localhost:27017/"
```

### CORS Error

```python
# Already enabled in main.py
CORS(app)  # Allows all origins
```

---

## 📚 Full Documentation

- **Integration Analysis:** `TSDICE_INTEGRATION_ANALYSIS.md`
- **Deployment Guide:** `docs/TSDICE_DEPLOYMENT_GUIDE.md`
- **Test Suite:** `test_tsdice_integration.py`

---

## ✨ Features for tsDice

- ✅ Emoji-based short URLs (8 emojis)
- ✅ Analytics & click tracking
- ✅ Public leaderboard
- ✅ Password protection (optional)
- ✅ Click limits (optional)
- ✅ Browser/country/device analytics
- ✅ Export stats (CSV, JSON, XLSX, XML)

---

## 🎯 Success Checklist

- [x] API endpoint functional
- [x] Emoji validation supports 8 emojis
- [x] CORS enabled for GitHub Pages
- [x] CSRF bypassed for API requests
- [x] Response includes `short_url` field
- [x] Redirect works for emoji URLs
- [x] MongoDB storage configured
- [x] Environment variables documented
- [x] Deployment guide created
- [x] Test suite available

---

**Status:** ✅ Production Ready

**Last Updated:** 2025-11-30

**Next Step:** Deploy to production and test with tsDice
