import os
import requests

XAI_API_KEY = os.getenv("XAI_API_KEY")

# -- Grok API function --

def translate_with_grok(text, target_language):

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-4.3",
        "messages": [
            {
                "role": "system",
                "content": (
                f"You are a high-quality social media translation engine like X (Twitter). "
                f"Translate everything into {target_language}. "
                "Keep tone, slang, emotion. "
                "Output ONLY the translation, no explanation."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.3
    }

    res = requests.post(url, headers=headers, json=data)

    # 看真实返回和出错终止运行
    print("STATUS:", res.status_code)
    print("BODY:", res.text)
    #print("REQUEST:", data)

    res.raise_for_status()
    
    return res.json()["choices"][0]["message"]["content"]
