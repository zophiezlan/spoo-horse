"""
tsDice Integration Blueprint
Custom endpoints and features for deep integration with tsDice particle playground
"""

from flask import Blueprint, request, jsonify, render_template, redirect
from utils.url_utils import (
    get_client_ip,
    validate_password,
    validate_url,
    validate_emoji_alias,
    generate_emoji_alias,
)
from utils.mongo_utils import (
    insert_emoji_url,
    load_emoji_url,
    check_if_emoji_alias_exists,
    validate_blocked_url,
    urls_collection,
    emoji_urls_collection,
)
from utils.general import humanize_number
from datetime import datetime
from urllib.parse import unquote
import os
import json
import re

tsdice = Blueprint("tsdice", __name__)


def select_emojis_for_config(config_data):
    """
    Smart emoji selection based on particle configuration
    Analyzes config and picks themed emojis
    """
    emojis = []

    # Try to extract meaningful data from config
    # tsdice config is compressed, so this is best-effort
    config_str = str(config_data).lower() if config_data else ""

    # Theme-based selection
    if "dark" in config_str or "night" in config_str:
        emojis.append("🌙")
    elif "light" in config_str or "bright" in config_str:
        emojis.append("☀️")

    # Color-based selection
    if "rainbow" in config_str or "multicolor" in config_str:
        emojis.append("🌈")
    elif "blue" in config_str:
        emojis.append("💙")
    elif "red" in config_str:
        emojis.append("❤️")
    elif "green" in config_str:
        emojis.append("💚")
    elif "purple" in config_str:
        emojis.append("💜")
    elif "yellow" in config_str or "gold" in config_str:
        emojis.append("💛")

    # Effect-based selection
    if "gravity" in config_str:
        emojis.append("🌍")
    if "sparkle" in config_str or "twinkle" in config_str:
        emojis.append("✨")
    if "fire" in config_str or "flame" in config_str:
        emojis.append("🔥")
    if "water" in config_str or "wave" in config_str:
        emojis.append("🌊")
    if "star" in config_str:
        emojis.append("⭐")
    if "heart" in config_str:
        emojis.append("💖")

    # General creative emojis for particle playground
    creative_emojis = ["🎨", "🎭", "🎪", "🎯", "🎲", "🎰", "✨", "🌟", "💫", "🔮"]

    # Fill remaining slots with creative emojis
    while len(emojis) < 3:
        from random import choice
        emoji = choice(creative_emojis)
        if emoji not in emojis:  # Avoid duplicates
            emojis.append(emoji)

    return "".join(emojis[:3])


@tsdice.route("/api/tsdice/share", methods=["POST"])
def share_particle_config():
    """
    tsDice-specific endpoint with enhanced features:
    - Auto-emoji selection based on config
    - Stores config metadata for rich previews
    - No rate limiting for tsDice API key
    - Returns additional metadata
    """

    # Check for API key (optional - provides bypass for rate limits)
    api_key = request.headers.get("X-API-Key")
    tsdice_api_key = os.getenv("TSDICE_API_KEY", "tsdice-default-key")
    is_authenticated = api_key == tsdice_api_key

    # Get parameters
    url = request.values.get("url")
    emojies = request.values.get("emojies")
    password = request.values.get("password")
    max_clicks = request.values.get("max-clicks")
    config_data = request.values.get("config")  # Optional: raw config data

    # Validate URL
    if not url:
        return jsonify({"UrlError": "URL is required"}), 400

    if not validate_url(url):
        return jsonify({
            "UrlError": "Invalid URL, URL must have a valid protocol and follow RFC patterns"
        }), 400

    if not validate_blocked_url(url):
        return jsonify({"UrlError": "Blocked URL ⛔"}), 403

    # Handle emoji selection
    if emojies:
        if not validate_emoji_alias(emojies):
            return jsonify({"EmojiError": "Invalid emoji"}), 400
        if check_if_emoji_alias_exists(emojies):
            return jsonify({"EmojiError": "Emoji already exists"}), 400
    else:
        # Try smart selection first, fallback to random
        if config_data:
            try:
                emojies = select_emojis_for_config(config_data)
                # Check for collision
                if check_if_emoji_alias_exists(emojies):
                    emojies = generate_emoji_alias()
            except:
                emojies = generate_emoji_alias()
        else:
            emojies = generate_emoji_alias()

        # Ensure uniqueness
        attempts = 0
        while check_if_emoji_alias_exists(emojies) and attempts < 10:
            emojies = generate_emoji_alias()
            attempts += 1

    # Build data object
    data = {
        "url": url,
        "counter": {},
        "total-clicks": 0,
        "ips": [],
        "creation-date": datetime.now().strftime("%Y-%m-%d"),
        "creation-time": datetime.now().strftime("%H:%M:%S"),
        "creation-ip-address": get_client_ip(),
        "tsdice-config": True,  # Mark as tsdice link
        "source": "tsdice-api",
    }

    # Store config data if provided (for future features)
    if config_data:
        data["config-preview"] = str(config_data)[:500]  # Store first 500 chars

    # Optional features
    if password and validate_password(password):
        data["password"] = password

    if max_clicks and str(max_clicks).isdigit():
        data["max-clicks"] = str(abs(int(max_clicks)))

    # Insert into database
    insert_emoji_url(emojies, data)

    # Return enhanced response
    short_domain = os.getenv("TSDICE_SHORT_DOMAIN", request.host)

    return jsonify({
        "short_url": f"https://{short_domain}/{emojies}",
        "stats_url": f"https://{request.host}/stats/{emojies}",
        "emojis": emojies,
        "domain": short_domain,
        "original_url": url,
        "api_version": "1.0-tsdice",
        "authenticated": is_authenticated
    })


@tsdice.route("/tsdice/leaderboard")
def tsdice_leaderboard():
    """
    Public leaderboard of most popular particle configs
    Shows top 20 most clicked tsdice links
    """

    # Get top configs from both collections
    top_configs = list(emoji_urls_collection.find(
        {"tsdice-config": True}
    ).sort("total-clicks", -1).limit(20))

    # Calculate stats
    total_configs = emoji_urls_collection.count_documents({"tsdice-config": True})
    total_clicks = sum(config.get("total-clicks", 0) for config in top_configs)

    return render_template(
        "tsdice_leaderboard.html",
        configs=top_configs,
        total_configs=humanize_number(total_configs),
        total_clicks=humanize_number(total_clicks),
        host_url=request.host_url
    )


@tsdice.route("/api/tsdice/analytics")
def tsdice_analytics():
    """
    Aggregate analytics for all tsdice links
    Public endpoint for embedding stats
    """

    pipeline = [
        {"$match": {"tsdice-config": True}},
        {"$group": {
            "_id": None,
            "total_configs_shared": {"$sum": 1},
            "total_clicks": {"$sum": "$total-clicks"},
            "avg_clicks_per_config": {"$avg": "$total-clicks"}
        }},
        {"$project": {
            "_id": 0,
            "total_configs_shared": 1,
            "total_clicks": 1,
            "avg_clicks_per_config": {"$round": ["$avg_clicks_per_config", 2]}
        }}
    ]

    try:
        result = list(emoji_urls_collection.aggregate(pipeline))
        if result:
            stats = result[0]
        else:
            stats = {
                "total_configs_shared": 0,
                "total_clicks": 0,
                "avg_clicks_per_config": 0
            }

        # Add humanized versions
        stats["total_configs_shared_display"] = humanize_number(stats["total_configs_shared"])
        stats["total_clicks_display"] = humanize_number(stats["total_clicks"])

        return jsonify(stats)
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch analytics",
            "total_configs_shared": 0,
            "total_clicks": 0
        }), 500


@tsdice.route("/result/tsdice/<short_code>")
def tsdice_result(short_code):
    """
    Custom result page with tsdice branding
    Matches the glassmorphism aesthetic of tsdice
    """
    short_code = unquote(short_code)
    url_data = load_emoji_url(short_code)

    if url_data:
        short_url = f"{request.host_url}{short_code}"
        return render_template(
            "tsdice_result.html",
            short_url=short_url,
            short_code=short_code,
            emojis=short_code,
            config=url_data.get("config-preview", ""),
            host_url=request.host_url,
            tsdice_url="https://ket.horse"
        )
    else:
        return render_template(
            "error.html",
            error_code="404",
            error_message="URL NOT FOUND",
            host_url=request.host_url
        ), 404


@tsdice.route("/widget/share.js")
def share_widget():
    """
    JavaScript widget for embedding in tsdice
    Drop-in solution for sharing functionality
    """

    api_endpoint = os.getenv("TSDICE_API_ENDPOINT", f"https://{request.host}/api/tsdice/share")
    api_key = os.getenv("TSDICE_PUBLIC_KEY", "")

    widget_js = f"""
/**
 * KetHorse Share Widget for tsDice
 * Auto-integrated sharing with emoji URL generation
 */
(function() {{
    window.KetHorseShare = {{
        apiEndpoint: '{api_endpoint}',
        apiKey: '{api_key}',

        /**
         * Share a particle configuration
         * @param {{string}} url - Full URL with config
         * @param {{object}} options - Optional config data
         * @returns {{Promise<object>}} Response with short_url
         */
        share: async function(url, options = {{}}) {{
            try {{
                const formData = new URLSearchParams({{
                    url: url,
                    ...(options.emojis && {{ emojies: options.emojis }}),
                    ...(options.config && {{ config: JSON.stringify(options.config) }})
                }});

                const response = await fetch(this.apiEndpoint, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/json',
                        ...(this.apiKey && {{ 'X-API-Key': this.apiKey }})
                    }},
                    body: formData
                }});

                if (!response.ok) {{
                    throw new Error(`HTTP ${{response.status}}`);
                }}

                const data = await response.json();

                // Auto-copy to clipboard
                if (navigator.clipboard && data.short_url) {{
                    await navigator.clipboard.writeText(data.short_url);
                    this.showToast('✨ ' + data.emojis + ' copied to clipboard!');
                }}

                return data;
            }} catch (error) {{
                console.error('KetHorseShare error:', error);
                this.showToast('❌ Failed to create short URL', true);
                throw error;
            }}
        }},

        /**
         * Show toast notification
         */
        showToast: function(message, isError = false) {{
            const toast = document.createElement('div');
            toast.className = 'ket-toast' + (isError ? ' ket-toast-error' : '');
            toast.textContent = message;
            toast.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: ${{isError ? '#ff4444' : '#6a5cf4'}};
                color: white;
                padding: 15px 24px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 500;
                z-index: 99999;
                animation: slideIn 0.3s ease;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            `;

            document.body.appendChild(toast);
            setTimeout(() => {{
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }}, 3000);
        }}
    }};

    // Add animations if not present
    if (!document.getElementById('ket-share-animations')) {{
        const style = document.createElement('style');
        style.id = 'ket-share-animations';
        style.textContent = `
            @keyframes slideIn {{
                from {{ transform: translateX(400px); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            @keyframes slideOut {{
                from {{ transform: translateX(0); opacity: 1; }}
                to {{ transform: translateX(400px); opacity: 0; }}
            }}
        `;
        document.head.appendChild(style);
    }}

    console.log('🐎 KetHorse Share Widget loaded');
}})();
"""

    return widget_js, 200, {'Content-Type': 'application/javascript'}
