# agent/llm_client.py
import os
import requests

def call_llm(prompt: str) -> str:
    token = os.environ.get("AIPROXY_TOKEN")
    if not token:
        raise Exception("AIPROXY_TOKEN environment variable not set")
    # For demonstration, we assume the LLM endpoint is as below.
    # Replace the URL with the actual endpoint if available.
    url = "https://api.ai-proxy.example/llm"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "prompt": prompt,
        "max_tokens": 50
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", "").strip()
        else:
            raise Exception(f"LLM API returned status {response.status_code}")
    except Exception as e:
        # For simulation purposes, return dummy values based on the prompt.
        if "Extract the sender's email" in prompt:
            return "sender@example.com"
        elif "Extract the credit card number" in prompt:
            return "1234123412341234"
        else:
            return "dummy_result"

