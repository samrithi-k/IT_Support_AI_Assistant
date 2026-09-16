import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.7-flash"


async def generate_response(question, context):

    if not GEMINI_API_KEY:
        return create_fallback_response(context)

    prompt = f"""
You are an IT support assistant.

User question:
{question}

Knowledge base:
{context}

Give concise, clear troubleshooting steps.
Use the knowledge base as the primary source.
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:

            response = await client.post(
                url,
                headers=headers,
                json=payload
            )

        if response.status_code == 200:

            data = response.json()

            return (
                data["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

    except Exception:
        pass

    # Gemini unavailable — use knowledge-base fallback
    return create_fallback_response(context)


def create_fallback_response(context):

    return (
        "Here are the recommended troubleshooting steps "
        "based on the available IT knowledge base:\n\n"
        + context
    )