# tsDice Integration - Deployment Guide

This guide provides step-by-step instructions for deploying the spoo-horse URL shortener to work with tsDice.

## Prerequisites

- MongoDB instance (local or cloud)
- Domain access for DNS configuration
- Vercel account (or alternative hosting)
- Git repository access

---

## Step 1: Environment Configuration

### Create `.env` file

Copy the example environment file:

```bash
cp .env.example .env
```

### Configure Required Variables

Edit `.env` and set the following:

```bash
# MongoDB (REQUIRED)
MONGODB_URI="mongodb://your-mongodb-uri:27017/"
MONGO_DB_NAME="url-shortener"

# tsDice Short Domain (REQUIRED for correct short URLs)
TSDICE_SHORT_DOMAIN="share.ket.horse"

# API Endpoint (optional - defaults to request host)
TSDICE_API_ENDPOINT="https://my.ket.horse/api/tsdice/share"
```

### Optional Configuration

```bash
# Redis (for caching - improves performance)
REDIS_URI="redis://localhost:6379"
REDIS_TTL_SECONDS=3600

# API Key (for rate limit bypass)
TSDICE_API_KEY="your-secret-api-key-here"

# hCaptcha (for contact/report forms)
HCAPTCHA_SECRET="your-hcaptcha-secret"
```

---

## Step 2: DNS Configuration

Configure DNS records for your domains:

### Option A: Separate Domains (Recommended)

**API Domain:** `my.ket.horse`
```
Type: CNAME
Name: my
Value: cname.vercel-dns.com
```

**Short URL Domain:** `share.ket.horse`
```
Type: CNAME
Name: share
Value: cname.vercel-dns.com
```

### Option B: Single Domain

**API & Short URLs:** `spoo.me`
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

Update `.env`:
```bash
TSDICE_SHORT_DOMAIN="spoo.me"
TSDICE_API_ENDPOINT="https://spoo.me/api/tsdice/share"
```

---

## Step 3: MongoDB Setup

### Option A: Local MongoDB

1. Install MongoDB:
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community
```

2. Start MongoDB:
```bash
# Ubuntu/Debian
sudo systemctl start mongodb

# macOS
brew services start mongodb-community
```

3. Configure `.env`:
```bash
MONGODB_URI="mongodb://localhost:27017/"
MONGO_DB_NAME="url-shortener"
```

### Option B: MongoDB Atlas (Cloud)

1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string
4. Configure `.env`:
```bash
MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
MONGO_DB_NAME="url-shortener"
```

### Create Indexes (Performance Optimization)

```javascript
// Connect to MongoDB and run:
db.emoji_urls.createIndex({ "_id": 1 })
db.emoji_urls.createIndex({ "tsdice-config": 1 })
db.emoji_urls.createIndex({ "total-clicks": -1 })
db.emoji_urls.createIndex({ "creation-date": 1 })
```

---

## Step 4: Deploy to Vercel

### Install Vercel CLI

```bash
npm install -g vercel
```

### Login to Vercel

```bash
vercel login
```

### Deploy

```bash
# First deployment
vercel

# Production deployment
vercel --prod
```

### Configure Environment Variables in Vercel

```bash
# Add each environment variable
vercel env add MONGODB_URI production
vercel env add MONGO_DB_NAME production
vercel env add TSDICE_SHORT_DOMAIN production
vercel env add TSDICE_API_ENDPOINT production
# ... add other variables as needed
```

Or use Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add each variable from your `.env` file

### Configure Custom Domains in Vercel

1. Go to your project settings
2. Navigate to "Domains"
3. Add domains:
   - `my.ket.horse` (API endpoint)
   - `share.ket.horse` (short URLs)
4. Verify DNS configuration

---

## Step 5: Verify Deployment

### Test API Endpoint

```bash
curl -X POST https://my.ket.horse/api/tsdice/share \
  -H "Accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://example.com&emojies=🐎🦄🌀✨🎉🪐👽🛸"
```

Expected response:
```json
{
  "short_url": "https://share.ket.horse/🐎🦄🌀✨🎉🪐👽🛸",
  "stats_url": "https://my.ket.horse/stats/🐎🦄🌀✨🎉🪐👽🛸",
  "emojis": "🐎🦄🌀✨🎉🪐👽🛸",
  "domain": "share.ket.horse",
  "original_url": "https://example.com",
  "api_version": "1.0-tsdice",
  "authenticated": false
}
```

### Test Redirect

```bash
curl -I https://share.ket.horse/🐎🦄🌀✨🎉🪐👽🛸
```

Expected: HTTP 302 redirect

### Test in Browser

1. Visit: https://my.ket.horse/ (should show homepage)
2. Visit: https://share.ket.horse/🐎🦄🌀✨🎉🪐👽🛸 (should redirect)
3. Visit: https://my.ket.horse/tsdice/leaderboard (should show leaderboard)

---

## Step 6: Integrate with tsDice

### Update tsDice Configuration

**File:** `js/main.js` (in tsDice repository)

Verify the endpoint URL:

```javascript
const response = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    url: fullUrl,
    emojies: randomEmojis
  })
});
```

### Optional: Add API Key

For rate limit bypass, add API key to tsDice:

```javascript
headers: {
  'Accept': 'application/json',
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-API-Key': 'your-tsdice-api-key'  // Add this line
}
```

Set the same key in `.env`:
```bash
TSDICE_API_KEY="your-tsdice-api-key"
```

---

## Step 7: Monitor & Maintain

### View Logs

```bash
# Vercel logs
vercel logs

# Or in Vercel Dashboard
# Project > Deployments > [deployment] > Logs
```

### Monitor Analytics

- **Leaderboard:** https://my.ket.horse/tsdice/leaderboard
- **Analytics API:** https://my.ket.horse/api/tsdice/analytics
- **Stats per URL:** https://my.ket.horse/stats/🐎🦄...

### Database Maintenance

```javascript
// View total tsDice configs
db.emoji_urls.countDocuments({ "tsdice-config": true })

// View top configs
db.emoji_urls.find({ "tsdice-config": true })
  .sort({ "total-clicks": -1 })
  .limit(10)

// Clean up old configs (optional)
db.emoji_urls.deleteMany({
  "tsdice-config": true,
  "total-clicks": 0,
  "creation-date": { $lt: "2025-01-01" }
})
```

---

## Troubleshooting

### Issue: 404 Not Found

**Problem:** API endpoint returns 404

**Solution:**
- Verify deployment is live: `vercel ls`
- Check domain configuration in Vercel
- Verify DNS propagation: `dig my.ket.horse`

### Issue: 500 Internal Server Error

**Problem:** MongoDB connection error

**Solution:**
- Check MongoDB is running
- Verify `MONGODB_URI` in environment variables
- Check MongoDB logs
- Test connection: `mongosh "mongodb://your-uri"`

### Issue: CORS Error

**Problem:** Browser shows CORS error from tsDice

**Solution:**
- CORS is enabled by default
- If restricted, update `main.py`:
```python
CORS(app, origins=["https://zophiezlan.github.io"])
```

### Issue: Short URL has wrong domain

**Problem:** Short URL returns `http://localhost/...` or wrong domain

**Solution:**
- Set `TSDICE_SHORT_DOMAIN` in environment variables
- Redeploy: `vercel --prod`
- Clear environment cache: `vercel env rm TSDICE_SHORT_DOMAIN production`
- Re-add: `vercel env add TSDICE_SHORT_DOMAIN production`

### Issue: Emoji not working in URL

**Problem:** Emoji URLs return 404 or fail to encode

**Solution:**
- Emojis are URL-encoded automatically by browsers
- Test with curl using escaped emojis:
```bash
curl "https://share.ket.horse/%F0%9F%90%8E%F0%9F%A6%84..."
```

---

## Performance Optimization

### Enable Redis Caching

1. Install Redis
2. Configure `.env`:
```bash
REDIS_URI="redis://localhost:6379"
REDIS_TTL_SECONDS=3600
```

### Add CDN (Cloudflare)

1. Add site to Cloudflare
2. Update DNS to Cloudflare nameservers
3. Enable caching rules:
   - Cache everything
   - Edge cache TTL: 1 hour

### Database Optimization

- Create indexes (see Step 3)
- Use connection pooling
- Monitor slow queries

---

## Security Hardening

### Restrict CORS Origins

```python
# main.py
from flask_cors import CORS

CORS(app, origins=[
    "https://zophiezlan.github.io",
    "https://tsdice.ket.horse",
    "https://ket.horse"
])
```

### Add Rate Limiting

Already configured in `blueprints/limiter.py`:
- 10 requests/minute
- 100 requests/hour
- 500 requests/day

### Block Malicious URLs

Add to MongoDB `blocked-urls` collection:
```javascript
db["blocked-urls"].insertOne({
  url: "malicious-domain.com",
  pattern: ".*malicious.*",
  reason: "Phishing site"
})
```

---

## Rollback Plan

### Rollback Deployment

```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel rollback [deployment-url]
```

### Database Backup

```bash
# Backup MongoDB
mongodump --uri="mongodb://your-uri" --out=./backup

# Restore MongoDB
mongorestore --uri="mongodb://your-uri" ./backup
```

---

## Success Metrics

After deployment, monitor these metrics:

- ✅ API response time <500ms
- ✅ Successful emoji creation rate >99%
- ✅ Redirect success rate >99.9%
- ✅ Zero CORS errors from tsDice
- ✅ Zero 500 errors in logs

---

## Next Steps

1. Monitor initial traffic from tsDice
2. Set up alerts for errors
3. Optimize database queries if needed
4. Add custom analytics dashboard (optional)
5. Consider adding features:
   - Emoji analytics
   - Popular config recommendations
   - Social media preview cards

---

## Support & Resources

- **Documentation:** `/docs/TSDICE_INTEGRATION_ANALYSIS.md`
- **Test Suite:** `python3 test_tsdice_integration.py`
- **Repository:** https://github.com/zophiezlan/spoo-horse
- **tsDice Repository:** https://github.com/zophiezlan/tsdice

For issues or questions, refer to the repository documentation or create an issue on GitHub.

---

**Last Updated:** 2025-11-30
**Version:** 1.0
**Status:** Production Ready ✅
