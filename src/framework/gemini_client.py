"""
Unified LLM Client for Deloitte Autonomous Multi-Agent Framework.
Supports Google Gemini API (2.5 Flash, 1.5 Pro) and Local LLMs (Ollama Qwen2.5-Coder, DeepSeek, LM Studio).
Provides zero-failure fallback with intelligent persona reasoning.
"""

from __future__ import annotations
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List

# Load .env if present
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
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=12)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        return None
    except Exception:
        return None


def call_ollama_api(
    system_prompt: str,
    user_message: str,
    model_name: str = "qwen2.5-coder:3b",
    host: str = "http://localhost:11434",
    temperature: float = 0.4
) -> Optional[str]:
    """
    Calls local Ollama API instance (e.g. qwen2.5-coder:3b, deepseek-coder).
    """
    url = f"{host}/api/generate"
    combined_prompt = f"<system>\n{system_prompt}\n</system>\n<user>\n{user_message}\n</user>\n<assistant>\n"
    payload = {
        "model": model_name,
        "prompt": combined_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024
        }
    }
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if response.status_code == 200:
            data = response.json()
            res = data.get("response", "").strip()
            if res:
                return res
        return None
    except Exception:
        return None


def call_unified_llm(
    system_prompt: str,
    user_message: str,
    preferred_model: Optional[str] = None,
    gemini_key: Optional[str] = None,
    temperature: float = 0.4
) -> Dict[str, Any]:
    """
    Unified entry point for all agent intelligence.
    Routes to:
    1. Gemini API (if key available)
    2. Ollama Local LLM (if Ollama running)
    3. Intelligent Persona Fallback
    """
    # 1. Try Gemini API
    gemini_reply = call_gemini_api(
        system_prompt=system_prompt,
        user_message=user_message,
        model_name="gemini-2.5-flash",
        api_key=gemini_key,
        temperature=temperature
    )
    if gemini_reply and not gemini_reply.startswith("[API Error"):
        return {
            "reply": gemini_reply,
            "provider": "gemini-2.5-flash",
            "is_live_llm": True
        }

    # 2. Try Ollama Local LLM
    ollama_reply = call_ollama_api(
        system_prompt=system_prompt,
        user_message=user_message,
        model_name="qwen2.5-coder:3b",
        temperature=temperature
    )
    if ollama_reply:
        return {
            "reply": ollama_reply,
            "provider": "ollama (qwen2.5-coder:3b)",
            "is_live_llm": True
        }

    # 3. Fallback
    return {
        "reply": None,
        "provider": "persona_playbook",
        "is_live_llm": False
    }
