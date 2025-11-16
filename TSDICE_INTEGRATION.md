# 🎨 tsDice Integration Guide

This document explains the deep integration between **my.ket.horse** (link shortener) and **tsDice** (particle playground).

## 🌟 Overview

The tsDice integration provides:

- **Smart emoji URL generation** based on particle configurations
- **Custom API endpoint** with auto-emoji selection
- **Rich social media previews** for shared links
- **Themed result pages** matching tsDice's glassmorphism aesthetic
- **Public leaderboard** showcasing trending particle configs
- **Analytics API** for tracking tsDice shares
- **JavaScript widget** for drop-in integration

---

## 🚀 Quick Start

### 1. Environment Variables

Add these to your `.env` file:

```bash
# tsDice Integration
TSDICE_API_KEY="your-secret-api-key-here"
TSDICE_PUBLIC_KEY="public-key-for-widget"
TSDICE_SHORT_DOMAIN="my.ket.horse"
TSDICE_API_ENDPOINT="https://my.ket.horse/api/tsdice/share"
```

### 2. Test the Integration

```bash
# Start the server
python main.py

# Test the tsDice-specific API
curl -X POST https://my.ket.horse/api/tsdice/share \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d "url=https://ket.horse/?config=example"
```

---

## 📡 API Endpoints

### POST `/api/tsdice/share`

Create a tsDice-themed emoji short URL with enhanced features.

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-API-Key: your-api-key (optional, bypasses rate limits)
Accept: application/json
```

**Parameters:**
- `url` (required): Full URL to shorten
- `emojies` (optional): Custom emoji string (auto-generated if omitted)
- `config` (optional): Particle config data for smart emoji selection
- `password` (optional): Password protect the link
- `max-clicks` (optional): Maximum number of clicks

**Response:**
```json
{
  "short_url": "https://my.ket.horse/🎨✨🌈",
  "stats_url": "https://my.ket.horse/stats/🎨✨🌈",
  "emojis": "🎨✨🌈",
  "domain": "my.ket.horse",
  "original_url": "https://ket.horse/?config=...",
  "api_version": "1.0-tsdice",
  "authenticated": true
}
```

**Example:**
```bash
curl -X POST https://my.ket.horse/api/tsdice/share \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "url=https://ket.horse/?config=rainbow"
```

---

### GET `/api/tsdice/analytics`

Get aggregate statistics for all tsDice shares.

**Response:**
```json
{
  "total_configs_shared": 1234,
  "total_clicks": 56789,
  "avg_clicks_per_config": 46.05,
  "total_configs_shared_display": "1.2K",
  "total_clicks_display": "56.8K"
}
```

**Example:**
```bash
curl https://my.ket.horse/api/tsdice/analytics
```

---

### GET `/tsdice/leaderboard`

View the public leaderboard of top 20 most popular particle configs.

**Features:**
- Live click counts
- Creation dates
- Click-to-visit functionality
- Medal icons for top 3
- Responsive glassmorphism design

**URL:** `https://my.ket.horse/tsdice/leaderboard`

---

### GET `/result/tsdice/<emoji>`

Custom themed result page for tsDice shares.

**Features:**
- Matches tsDice's purple gradient background
- Glassmorphism card design
- One-click copy
- Native share API support
- Link to create own animation

**URL:** `https://my.ket.horse/result/tsdice/🎨✨🌈`

---

### GET `/widget/share.js`

JavaScript widget for embedding share functionality in tsDice.

**Usage in tsDice:**
```html
<script src="https://my.ket.horse/widget/share.js"></script>

<script>
  // Share current config
  const shareButton = document.getElementById('share-btn');
  shareButton.addEventListener('click', async () => {
    const currentUrl = window.location.href;
    const response = await window.KetHorseShare.share(currentUrl, {
      config: getCurrentConfig() // optional
    });
    console.log('Short URL:', response.short_url);
  });
</script>
```

**Widget API:**
```javascript
window.KetHorseShare.share(url, options)
  // url: Full URL to shorten
  // options: { config, emojis }
  // Returns: Promise<{short_url, emojis, ...}>

window.KetHorseShare.showToast(message, isError)
  // message: Text to display
  // isError: boolean (default: false)
```

---

## 🎯 Smart Emoji Selection

The API automatically selects themed emojis based on config content:

| Config Content | Emoji Selected |
|----------------|----------------|
| "dark", "night" | 🌙 |
| "light", "bright" | ☀️ |
| "rainbow", "multicolor" | 🌈 |
| "blue" | 💙 |
| "red" | ❤️ |
| "green" | 💚 |
| "purple" | 💜 |
| "gravity" | 🌍 |
| "sparkle", "twinkle" | ✨ |
| "fire", "flame" | 🔥 |
| "water", "wave" | 🌊 |
| "star" | ⭐ |
| Default | 🎨🎭🎪🎯 (random creative emojis) |

---

## 🌐 Social Media Previews

When a tsDice link is shared on social media, crawlers receive a rich preview:

**Platforms Supported:**
- Facebook
- Twitter
- LinkedIn
- Discord
- Slack
- WhatsApp
- Telegram
- Pinterest

**Preview Includes:**
- Title: "Check out my particle animation! {{ emojis }}"
- Description: "Created with tsDice - Interactive particle playground"
- Image: tsDice banner
- Auto-redirect after metadata is read

**How it works:**
1. Social crawler visits `my.ket.horse/🎨✨`
2. Server detects User-Agent
3. Returns special preview page with Open Graph tags
4. Crawler reads metadata
5. Regular users are redirected immediately

---

## 🎨 Themed Pages

### Result Page

- **URL:** `/result/tsdice/<emoji>`
- **Design:** Matches tsDice glassmorphism aesthetic
- **Features:**
  - Purple gradient background
  - Glassmorphism card with blur effect
  - Animated emoji display
  - One-click copy to clipboard
  - Native share button
  - Link to tsDice
  - Stats link

### Leaderboard Page

- **URL:** `/tsdice/leaderboard`
- **Design:** Glassmorphism cards with animations
- **Features:**
  - Top 20 configs by clicks
  - Medal icons for top 3 (🥇🥈🥉)
  - Live statistics bar
  - Click to visit config
  - Slide-in animations
  - CTA to create own

---

## 🔧 Integration in tsDice

### Current Integration

tsDice already uses the API at `share.ket.horse/emoji`. To use the enhanced tsDice-specific endpoint:

**Update in `/tmp/tsdice/js/main.js` (lines 71-103):**

```javascript
// BEFORE (current)
const response = await fetch('https://share.ket.horse/emoji', {
  method: 'POST',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    url: longUrl,
    emojies: generateRandomEmojiString(8),
  }),
});

// AFTER (enhanced)
const response = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-API-Key': 'your-public-key', // Optional, for higher rate limits
  },
  body: new URLSearchParams({
    url: longUrl,
    // emojies: auto-selected based on config!
    config: JSON.stringify(getCurrentConfig()), // Enables smart emoji selection
  }),
});
```

### Alternative: Use the Widget

For even easier integration:

```html
<!-- Add to tsDice index.html -->
<script src="https://my.ket.horse/widget/share.js"></script>

<script type="module">
  // In your share function
  async function shareConfig() {
    try {
      const data = await window.KetHorseShare.share(window.location.href, {
        config: getCurrentConfig()
      });
      // Toast already shown by widget!
      return data.short_url;
    } catch (error) {
      console.error('Share failed:', error);
    }
  }
</script>
```

---

## 📊 Analytics & Monitoring

### Embed Live Stats in tsDice

```javascript
// Fetch tsDice-specific analytics
const response = await fetch('https://my.ket.horse/api/tsdice/analytics');
const stats = await response.json();

console.log(`${stats.total_configs_shared_display} configs shared`);
console.log(`${stats.total_clicks_display} total clicks`);
console.log(`${stats.avg_clicks_per_config} avg clicks per config`);
```

### Embed Leaderboard

```html
<!-- Add to tsDice homepage -->
<section class="community-showcase">
  <h2>🔥 Trending Particle Configs</h2>
  <iframe
    src="https://my.ket.horse/tsdice/leaderboard"
    width="100%"
    height="600"
    frameborder="0"
    style="border-radius: 16px; background: transparent;">
  </iframe>
</section>
```

---

## 🔐 Security & Rate Limiting

### Rate Limits

**Without API Key:**
- 10 requests/minute
- 100 requests/hour
- 500 requests/day

**With Valid API Key:**
- No rate limits
- Priority processing
- Enhanced analytics

### API Key Setup

1. Generate a secure API key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Add to `.env`:
```bash
TSDICE_API_KEY="your-generated-key-here"
```

3. Use in tsDice requests:
```javascript
headers: {
  'X-API-Key': 'your-generated-key-here'
}
```

---

## 🎁 Features Summary

| Feature | Description | URL |
|---------|-------------|-----|
| **Smart Emoji URLs** | Auto-selected based on config | `/api/tsdice/share` |
| **Themed Result Page** | Glassmorphism design | `/result/tsdice/<emoji>` |
| **Social Media Previews** | Rich Open Graph cards | Automatic |
| **Leaderboard** | Top 20 configs | `/tsdice/leaderboard` |
| **Analytics API** | Aggregate stats | `/api/tsdice/analytics` |
| **Share Widget** | Drop-in JavaScript | `/widget/share.js` |
| **Password Protection** | Optional link security | Via `password` param |
| **Max Clicks** | Self-destructing links | Via `max-clicks` param |

---

## 🐛 Troubleshooting

### Emoji URLs Not Working

**Issue:** Emoji URLs return 404

**Solution:** Ensure:
1. Blueprint is registered in `main.py`
2. MongoDB connection is active
3. Emoji validation is working (`utils/url_utils.py`)

### Social Previews Not Showing

**Issue:** Links don't show previews on Discord/Twitter

**Solution:**
1. Verify `tsdice-config: True` is set in database
2. Check User-Agent detection in redirector
3. Test with: `curl -A "Twitterbot" https://my.ket.horse/<emoji>`
4. Ensure banner image exists at `static/images/banner-rounded.png`

### Rate Limiting Issues

**Issue:** Getting 429 errors

**Solution:**
1. Add `X-API-Key` header
2. Verify API key in `.env` matches request
3. Check MongoDB for IP whitelisting

---

## 📚 Related Files

```
spoo-horse/
├── blueprints/
│   └── tsdice_integration.py      # Main tsDice blueprint
├── templates/
│   ├── tsdice_result.html         # Themed result page
│   ├── tsdice_leaderboard.html    # Public leaderboard
│   └── tsdice_preview.html        # Social media preview
├── main.py                         # Blueprint registration
├── blueprints/redirector.py        # Social crawler detection
└── .env.example                    # Configuration template
```

---

## 🚀 Next Steps

1. **Update tsDice** to use `/api/tsdice/share` endpoint
2. **Set API key** in tsDice for higher rate limits
3. **Add leaderboard iframe** to tsDice homepage
4. **Test social sharing** on Discord/Twitter
5. **Monitor analytics** via `/api/tsdice/analytics`

---

## 💡 Pro Tips

1. **Use config parameter** for smart emoji selection
2. **Set up API key** to bypass rate limits
3. **Embed leaderboard** for community engagement
4. **Track popular configs** via analytics API
5. **Use password protection** for exclusive shares
6. **Set max-clicks** for limited-time shares

---

**Questions?** Open an issue or contact the team!

✨ Happy particle animating! 🎨
