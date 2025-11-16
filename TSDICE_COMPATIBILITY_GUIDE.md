# tsDice x my.ket.horse Integration Guide

Complete guide for integrating my.ket.horse URL shortener with tsDice particle playground.

---

## 🎨 Overview

my.ket.horse provides deep integration with tsDice, featuring:
- **Smart emoji URL generation** based on particle configurations
- **Themed result pages** matching tsDice's glassmorphism design
- **Leaderboard** for trending particle configurations
- **Rich social media previews** for Discord, Twitter, Facebook
- **Dedicated API endpoints** for seamless integration

---

## 🚀 Quick Start

### Basic URL Shortening

```javascript
// From tsDice, create a short link for a particle config
const response = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    url: 'https://ket.horse?config=' + encodeURIComponent(JSON.stringify(config)),
    config: JSON.stringify(config) // Optional: enables smart emoji selection
  })
});

const data = await response.json();
console.log(data.short_url); // https://my.ket.horse/🌈✨🎨
```

---

## 📡 API Endpoints

### 1. **Share Particle Configuration**
`POST /api/tsdice/share`

Creates a short URL with automatic emoji selection based on particle config.

**Parameters:**
- `url` (required): The full tsDice URL to shorten
- `config` (optional): JSON particle configuration for smart emoji selection
- `password` (optional): Password protect the link
- `max-clicks` (optional): Maximum number of clicks before expiration

**Request Example:**
```bash
curl -X POST https://my.ket.horse/api/tsdice/share \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://ket.horse?config=%7B%22particles%22%3A100%7D" \
  -d "config={\"particles\":100,\"gravity\":true,\"rainbow\":true}"
```

**Response:**
```json
{
  "short_url": "https://my.ket.horse/🌈🌍✨",
  "long_url": "https://ket.horse?config=%7B%22particles%22%3A100%7D",
  "emoji_alias": "🌈🌍✨",
  "creation_date": "2025-11-16T13:00:00Z",
  "tsdice_config": true
}
```

---

### 2. **View Leaderboard**
`GET /tsdice/leaderboard`

Displays top 20 most popular particle configurations.

**Access:**
```
https://my.ket.horse/tsdice/leaderboard
```

**Features:**
- Medal icons for top 3 (🥇🥈🥉)
- Click counts
- Direct links to configurations
- Glassmorphism design matching tsDice aesthetic

---

### 3. **Analytics API**
`GET /api/tsdice/analytics`

Get aggregated analytics for all tsDice shares.

**Request:**
```bash
curl https://my.ket.horse/api/tsdice/analytics
```

**Response:**
```json
{
  "total_tsdice_shares": 1523,
  "total_clicks": 45678,
  "average_clicks_per_share": 29.97,
  "top_configs": [
    {
      "emoji": "🌈✨🎨",
      "clicks": 2345,
      "created": "2025-11-15T10:30:00Z"
    }
  ],
  "last_24h": 234,
  "last_7d": 892
}
```

---

## 🎯 Smart Emoji Selection

When you pass a `config` parameter, my.ket.horse automatically selects emojis based on your particle configuration:

### Emoji Mapping Logic

| Configuration | Emoji | When Used |
|--------------|-------|-----------|
| `rainbow: true` | 🌈 | Rainbow colors enabled |
| `gravity: true` | 🌍 | Gravity physics enabled |
| `particles > 1000` | ✨ | High particle count |
| `sparkle: true` | ⭐ | Sparkle effect |
| `fire: true` | 🔥 | Fire particles |
| `water: true` | 💧 | Water effect |
| `snow: true` | ❄️ | Snow particles |
| `heart: true` | ❤️ | Heart shapes |
| `star: true` | ⭐ | Star shapes |
| `circle: true` | ⚪ | Circle shapes |
| `explosion: true` | 💥 | Explosion effect |
| `colorful: true` | 🎨 | Multiple colors |
| `unicorn: true` | 🦄 | Unicorn theme |
| Default | 🎲🎮🎯 | Random fun emojis |

**Example:**
```javascript
const config = {
  particles: 1500,
  gravity: true,
  rainbow: true,
  sparkle: true
};

// Automatically generates: 🌈🌍✨
```

---

## 🎨 Integration Methods

### Method 1: JavaScript Widget (Recommended)

Include the share widget in your tsDice page:

```html
<!-- Add this to your tsDice HTML -->
<button id="shareBtn" class="share-button">Share Configuration 🔗</button>

<script>
async function shareConfig(particleConfig) {
  try {
    const configUrl = `https://ket.horse?config=${encodeURIComponent(JSON.stringify(particleConfig))}`;

    const response = await fetch('https://my.ket.horse/api/tsdice/share', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        url: configUrl,
        config: JSON.stringify(particleConfig)
      })
    });

    const data = await response.json();

    // Copy to clipboard
    await navigator.clipboard.writeText(data.short_url);

    // Show success message
    showToast(`✅ Link copied: ${data.short_url}`);

  } catch (error) {
    console.error('Share failed:', error);
    showToast('❌ Failed to create share link');
  }
}

// Attach to button
document.getElementById('shareBtn').addEventListener('click', () => {
  shareConfig(getCurrentParticleConfig());
});
</script>
```

---

### Method 2: Direct API Integration

```javascript
class TsDiceShareIntegration {
  constructor() {
    this.apiEndpoint = 'https://my.ket.horse/api/tsdice/share';
  }

  async createShareLink(config, options = {}) {
    const configUrl = `https://ket.horse?config=${encodeURIComponent(JSON.stringify(config))}`;

    const params = new URLSearchParams({
      url: configUrl,
      config: JSON.stringify(config),
      ...options // password, max-clicks, etc.
    });

    const response = await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params
    });

    if (!response.ok) {
      throw new Error(`Share failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async shareWithNativeAPI(config) {
    const linkData = await this.createShareLink(config);

    if (navigator.share) {
      await navigator.share({
        title: 'Check out my particle animation!',
        text: `Created with tsDice ${linkData.emoji_alias}`,
        url: linkData.short_url
      });
    } else {
      // Fallback: copy to clipboard
      await navigator.clipboard.writeText(linkData.short_url);
      return linkData.short_url;
    }
  }
}

// Usage
const shareIntegration = new TsDiceShareIntegration();

// Simple share
const link = await shareIntegration.createShareLink(particleConfig);

// Share with native dialog
await shareIntegration.shareWithNativeAPI(particleConfig);

// Share with options
const protectedLink = await shareIntegration.createShareLink(particleConfig, {
  password: 'secret123',
  'max-clicks': 100
});
```

---

### Method 3: URL Parameters

Direct links from tsDice to my.ket.horse:

```javascript
// Redirect user to create a short link
const configUrl = encodeURIComponent(`https://ket.horse?config=${JSON.stringify(config)}`);
window.location.href = `https://my.ket.horse/?url=${configUrl}&tsdice=true`;
```

---

## 📱 Social Media Features

### Rich Preview Support

When shared on social media, tsDice links automatically display:
- Custom title with emoji
- "Created with tsDice" description
- ket.horse banner image
- Automatic redirect after meta tags are parsed

**Supported Platforms:**
- Discord (rich embeds)
- Twitter (cards)
- Facebook (Open Graph)
- Slack (unfurl)
- Telegram (link preview)
- WhatsApp (link preview)

**How it works:**
```javascript
// Social media crawlers see this:
<meta property="og:title" content="Check out my particle animation! 🌈✨">
<meta property="og:description" content="Created with tsDice - Interactive particle playground">
<meta property="og:image" content="https://my.ket.horse/static/images/banner-rounded.png">

// Then auto-redirects to: https://ket.horse?config=...
```

---

## 📊 Analytics & Tracking

### Track Share Performance

```javascript
// Get analytics for your shares
async function getShareAnalytics(emojiAlias) {
  const response = await fetch(
    `https://my.ket.horse/stats/${emojiAlias}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        short_code: emojiAlias
      })
    }
  );

  // Returns detailed analytics page
}
```

### Available Metrics

- **Total clicks** (overall and unique)
- **Geographic data** (country heatmap)
- **Browser/OS breakdown**
- **Referrer sources**
- **Click timeline** (last 7/30 days, all time)
- **Average redirection time**
- **Bot detection** data

---

## 🏆 Leaderboard Integration

### Display Top Configs in tsDice

```javascript
async function getTopConfigs() {
  const response = await fetch('https://my.ket.horse/api/tsdice/leaderboard');
  const data = await response.json();

  return data.top_configs; // Top 20 configs by clicks
}

// Display in your UI
const topConfigs = await getTopConfigs();
topConfigs.forEach((config, index) => {
  console.log(`${index + 1}. ${config.emoji} - ${config.clicks} clicks`);
});
```

**Response Format:**
```json
{
  "top_configs": [
    {
      "emoji": "🌈✨🎨",
      "clicks": 2345,
      "unique_clicks": 1823,
      "created": "2025-11-15T10:30:00Z",
      "url": "https://ket.horse?config=..."
    }
  ],
  "total_configs": 1523,
  "last_updated": "2025-11-16T13:00:00Z"
}
```

---

## 🎨 Themed Result Pages

After creating a share link via the API, users can visit it to see a custom tsDice-themed result page:

**Features:**
- Purple/blue gradient matching ket.horse branding
- Glassmorphism design
- Animated emoji display
- QR code generation
- One-click copy
- Native share button
- Social media sharing buttons

**Access:**
```
https://my.ket.horse/tsdice/result/🌈✨🎨
```

---

## 🔒 Advanced Features

### Password Protection

```javascript
const protectedLink = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  body: new URLSearchParams({
    url: configUrl,
    config: JSON.stringify(config),
    password: 'secret123'
  })
});
```

### Click Limits

```javascript
const limitedLink = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  body: new URLSearchParams({
    url: configUrl,
    config: JSON.stringify(config),
    'max-clicks': 100  // Expires after 100 clicks
  })
});
```

### Bot Blocking

```javascript
const botProtectedLink = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  body: new URLSearchParams({
    url: configUrl,
    config: JSON.stringify(config),
    'block-bots': 'true'  // Block known bots
  })
});
```

---

## 🎯 Best Practices

### 1. **Always Pass Config Data**
```javascript
// ✅ Good - Enables smart emoji selection
await createShare(url, { config: particleConfig });

// ❌ Less optimal - Uses random emojis
await createShare(url);
```

### 2. **Handle Errors Gracefully**
```javascript
try {
  const link = await createShareLink(config);
  showSuccessMessage(link.short_url);
} catch (error) {
  console.error('Share failed:', error);
  // Fallback: show full URL
  showFallbackUrl(fullConfigUrl);
}
```

### 3. **Use Native Share When Available**
```javascript
if (navigator.share) {
  await navigator.share({
    title: 'My Particle Animation',
    url: shortUrl
  });
} else {
  // Fallback to clipboard
  await navigator.clipboard.writeText(shortUrl);
}
```

### 4. **Cache Short URLs**
```javascript
// Don't create duplicate links for same config
const configHash = hashConfig(config);
if (cachedLinks.has(configHash)) {
  return cachedLinks.get(configHash);
}

const newLink = await createShareLink(config);
cachedLinks.set(configHash, newLink);
return newLink;
```

---

## 🌐 Complete Integration Example

```javascript
// complete-integration.js
class TsDiceShareManager {
  constructor() {
    this.apiBase = 'https://my.ket.horse';
    this.cache = new Map();
  }

  // Create and cache share link
  async share(particleConfig, options = {}) {
    const configStr = JSON.stringify(particleConfig);
    const cacheKey = this.hashConfig(configStr);

    // Check cache
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Create share link
    const configUrl = `https://ket.horse?config=${encodeURIComponent(configStr)}`;

    const response = await fetch(`${this.apiBase}/api/tsdice/share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        url: configUrl,
        config: configStr,
        ...options
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to create share link: ${response.statusText}`);
    }

    const data = await response.json();
    this.cache.set(cacheKey, data);
    return data;
  }

  // Share with native API or clipboard fallback
  async shareNative(particleConfig) {
    const shareData = await this.share(particleConfig);

    if (navigator.share) {
      try {
        await navigator.share({
          title: `Check out my particle animation! ${shareData.emoji_alias}`,
          text: 'Created with tsDice - Interactive particle playground',
          url: shareData.short_url
        });
        return { success: true, method: 'native' };
      } catch (err) {
        if (err.name === 'AbortError') {
          return { success: false, reason: 'cancelled' };
        }
        throw err;
      }
    } else {
      // Fallback to clipboard
      await navigator.clipboard.writeText(shareData.short_url);
      return { success: true, method: 'clipboard', url: shareData.short_url };
    }
  }

  // Get analytics for a share
  async getAnalytics(emojiAlias, password = null) {
    const params = new URLSearchParams({ short_code: emojiAlias });
    if (password) params.append('password', password);

    const response = await fetch(`${this.apiBase}/stats`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params
    });

    return response.json();
  }

  // Get leaderboard
  async getLeaderboard() {
    const response = await fetch(`${this.apiBase}/api/tsdice/leaderboard`);
    return response.json();
  }

  // Simple hash for caching
  hashConfig(configStr) {
    let hash = 0;
    for (let i = 0; i < configStr.length; i++) {
      const char = configStr.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(36);
  }
}

// Usage in tsDice
const shareManager = new TsDiceShareManager();

// Add share button to your UI
document.getElementById('shareBtn').addEventListener('click', async () => {
  try {
    const config = getCurrentParticleConfig();
    const result = await shareManager.shareNative(config);

    if (result.success) {
      if (result.method === 'native') {
        showToast('✅ Shared successfully!');
      } else {
        showToast(`✅ Link copied: ${result.url}`);
      }
    }
  } catch (error) {
    console.error('Share error:', error);
    showToast('❌ Failed to share configuration');
  }
});

// Display leaderboard
async function showLeaderboard() {
  const data = await shareManager.getLeaderboard();
  const list = document.getElementById('leaderboard');

  data.top_configs.forEach((config, index) => {
    const medal = index < 3 ? ['🥇', '🥈', '🥉'][index] : '';
    list.innerHTML += `
      <li>
        ${medal} ${index + 1}.
        <a href="https://my.ket.horse/${config.emoji}">${config.emoji}</a>
        - ${config.clicks} clicks
      </li>
    `;
  });
}
```

---

## 🎨 UI Components

### Share Button Example

```html
<button class="tsdice-share-btn" onclick="shareCurrentConfig()">
  <span class="icon">🔗</span>
  <span class="text">Share</span>
</button>

<style>
.tsdice-share-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s;
}

.tsdice-share-btn:hover {
  transform: translateY(-2px);
}

.tsdice-share-btn:active {
  transform: translateY(0);
}
</style>

<script>
async function shareCurrentConfig() {
  const config = getCurrentParticleConfig();
  const shareManager = new TsDiceShareManager();

  try {
    const result = await shareManager.shareNative(config);
    if (result.success && result.method === 'clipboard') {
      showToast(`✅ Link copied: ${result.url}`);
    }
  } catch (error) {
    console.error('Share failed:', error);
  }
}
</script>
```

---

## 📝 Summary

### Key Integration Points

1. **Create Share Links**: `POST /api/tsdice/share`
2. **View Leaderboard**: `GET /tsdice/leaderboard`
3. **Get Analytics**: `GET /api/tsdice/analytics`
4. **View Stats**: `POST /stats`

### Why Use my.ket.horse?

✅ **Smart emoji URLs** - Memorable and fun
✅ **Automatic config detection** - Emojis match your particles
✅ **Beautiful result pages** - Matching tsDice aesthetic
✅ **Social media ready** - Rich previews everywhere
✅ **Analytics included** - Track your shares
✅ **Leaderboard** - See trending configs
✅ **Fast & reliable** - Vercel edge network

---

## 🆘 Support & Issues

- **Documentation**: This guide
- **API Status**: https://my.ket.horse/api
- **Leaderboard**: https://my.ket.horse/tsdice/leaderboard
- **Technical Integration**: See `TSDICE_INTEGRATION.md` for backend details

---

## 🎉 Let's Make Sharing Awesome!

Start integrating today and make your particle configurations go viral! 🚀

```javascript
// It's this easy!
const link = await fetch('https://my.ket.horse/api/tsdice/share', {
  method: 'POST',
  body: new URLSearchParams({
    url: 'https://ket.horse?config=...',
    config: JSON.stringify(yourConfig)
  })
}).then(r => r.json());

console.log(link.short_url); // 🌈✨🎨
```

Happy sharing! 🎨✨
