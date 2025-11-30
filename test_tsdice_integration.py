#!/usr/bin/env python3
"""
Test script to verify tsDice integration compatibility
Simulates the exact request format that tsDice sends
"""

import sys
import requests
from urllib.parse import urlencode

def test_tsdice_api():
    """Test the /api/tsdice/share endpoint with tsDice's exact request format"""

    # Base URL - adjust if needed
    base_url = "http://127.0.0.1:5000"
    endpoint = f"{base_url}/api/tsdice/share"

    # Test data matching tsDice's exact format
    test_url = "https://zophiezlan.github.io/tsdice/#config=N4IgdghgtgpiBcIQBoQGcD2AnAlgFwgewHsZ0IBXAS0mOigB0ZCQAPABwHMBKAZRgF0AogHkA8gBkAogFEAqhWEAZMYOHCRomQEYADHKkAmKQGYpigCxTFATm0mALNoDsJgKxmArJ42mrASQBCAJIAEq4ADgASAIIAKgCC-q72-v4BQSD+-oEh4RFRMXEJScmpGVm5+YUl5ZXV1bX1jc0tbR2dXb39g8Ojo+OTU9Ozc-MLi8ur6xubW9u7ewcHx8enZ+cXl1c3t3cPj09Pz-eP9y8vb2+f355f3p8+3z8-vj-fPr4_3z4_Pr8_P74_P76_P7-fP7-fP76_v76_v7-fv7-fv76_v7-fv7-fv76"
    test_emojis = "🐎🦄🌀✨🎉🪐👽🛸"

    # Prepare request data (application/x-www-form-urlencoded)
    data = {
        "url": test_url,
        "emojies": test_emojis
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print("=" * 70)
    print("Testing tsDice API Integration")
    print("=" * 70)
    print(f"\nEndpoint: {endpoint}")
    print(f"Method: POST")
    print(f"Headers: {headers}")
    print(f"Data:")
    print(f"  url: {test_url[:60]}...")
    print(f"  emojies: {test_emojis} (count: {len(test_emojis)})")
    print("\n" + "-" * 70)

    try:
        # Make the request
        response = requests.post(
            endpoint,
            data=urlencode(data),
            headers=headers,
            timeout=5
        )

        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")

        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"\nReturned Data:")
            for key, value in result.items():
                print(f"  {key}: {value}")

            # Verify required fields
            print("\n" + "=" * 70)
            print("Validation Checks:")
            print("=" * 70)

            required_field = "short_url"
            if required_field in result:
                print(f"✅ Required field '{required_field}' present")
                print(f"   Value: {result[required_field]}")
            else:
                print(f"❌ Required field '{required_field}' MISSING")
                return False

            # Verify emoji is in the short URL
            if test_emojis in result.get("short_url", ""):
                print(f"✅ Emoji string present in short_url")
            else:
                print(f"❌ Emoji string NOT in short_url")
                print(f"   Expected: {test_emojis}")
                print(f"   Got: {result.get('short_url', '')}")
                return False

            print("\n✅ All validation checks passed!")
            return True

        else:
            print(f"❌ FAILED with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server.")
        print("   Make sure the Flask app is running on http://127.0.0.1:5000")
        print("   Start it with: python main.py")
        return False
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False


def test_emoji_validation():
    """Test that emoji validation supports 8 emojis"""
    print("\n" + "=" * 70)
    print("Testing Emoji Validation")
    print("=" * 70)

    from utils.url_utils import validate_emoji_alias

    test_cases = [
        ("🐎🦄🌀", "3 emojis", True),
        ("🐎🦄🌀✨🎉🪐👽🛸", "8 emojis (tsDice format)", True),
        ("🐎" * 15, "15 emojis (max)", True),
        ("🐎" * 16, "16 emojis (too many)", False),
        ("abc", "Not emojis", False),
        ("", "Empty string", False),
    ]

    all_passed = True
    for test_input, description, expected in test_cases:
        result = validate_emoji_alias(test_input)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}: {result} (expected {expected})")
        if result != expected:
            all_passed = False

    return all_passed


def test_redirect():
    """Test that emoji URLs redirect properly"""
    print("\n" + "=" * 70)
    print("Testing Emoji URL Redirect")
    print("=" * 70)

    base_url = "http://127.0.0.1:5000"

    # First create a short URL
    endpoint = f"{base_url}/api/tsdice/share"
    test_url = "https://example.com/test"
    test_emojis = "🎨🎭🎪"

    data = urlencode({"url": test_url, "emojies": test_emojis})
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        # Create short URL
        response = requests.post(endpoint, data=data, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"❌ Failed to create short URL: {response.status_code}")
            return False

        result = response.json()
        short_url = result.get("short_url", "")
        print(f"Created: {short_url}")

        # Test redirect (without following redirects to check it exists)
        redirect_response = requests.get(
            f"{base_url}/{test_emojis}",
            allow_redirects=False,
            timeout=5
        )

        if redirect_response.status_code in [301, 302, 303, 307, 308]:
            print(f"✅ Redirect works! Status: {redirect_response.status_code}")
            location = redirect_response.headers.get("Location", "")
            print(f"   Redirects to: {location}")
            if location == test_url:
                print(f"✅ Redirect target matches original URL")
                return True
            else:
                print(f"❌ Redirect target mismatch")
                print(f"   Expected: {test_url}")
                print(f"   Got: {location}")
                return False
        else:
            print(f"❌ Expected redirect status, got {redirect_response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    print("\n🐎 tsDice Integration Test Suite\n")

    results = []

    # Test 1: Emoji validation (doesn't require server)
    print("Test 1: Emoji Validation")
    results.append(("Emoji Validation", test_emoji_validation()))

    # Test 2: API endpoint
    print("\n\nTest 2: API Endpoint")
    results.append(("API Endpoint", test_tsdice_api()))

    # Test 3: Redirect functionality
    print("\n\nTest 3: Redirect Functionality")
    results.append(("Redirect", test_redirect()))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n🎉 All tests passed! Integration is ready for tsDice.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        sys.exit(1)
