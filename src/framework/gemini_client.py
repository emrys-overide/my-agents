"""
Gemini API Client for Deloitte Multi-Agent Framework.
Zero-dependency, uses standard requests library to interface with Gemini models.
"""

from __future__ import annotations
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any

# Look for .env file if GEMINI_API_KEY is not in environment
ENV_PATH = Path(__file__).parent.parent.parent / ".env"
if ENV_PATH.exists():
    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")


def get_gemini_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()
    return os.getenv("GEMINI_API_KEY")


def call_gemini_api(
    system_prompt: str,
    user_message: str,
    model_name: str = "gemini-2.5-flash",
    api_key: Optional[str] = None,
    temperature: float = 0.4
) -> Optional[str]:
    """
    Calls Google Gemini API directly using REST endpoint.
    """
    key = get_gemini_api_key(api_key)
    if not key:
        return None

    # Supported fast models: gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"System Context & Rules:\n{system_prompt}\n\nUser Request:\n{user_message}"}]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        return None
    except Exception:
        # Gracefully handle DNS/network isolation or timeouts
        return None
