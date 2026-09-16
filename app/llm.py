import os

import httpx

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = "gemini-3.7-flash"


async def generate_response(
    question,
    context
):

    # If Gemini API key is unavailable
    if not GEMINI_API_KEY:

        return create_fallback_response(
            context
        )


    prompt = f"""
You are an IT support assistant.

User's technical problem:
{question}

Relevant knowledge-base information:
{context}

Instructions:
- Give a clear and concise troubleshooting solution.
- Use the knowledge base as the primary source.
- Do not mention the knowledge base.
- Do not mention ticket numbers.
- Do not include unrelated problems.
- Give simple step-by-step instructions.
- If there is no relevant information, clearly say that the issue is not covered by the current knowledge base.
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

        "x-goog-api-key":
            GEMINI_API_KEY,

        "Content-Type":
            "application/json"
    }


    try:

        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:

            response = await client.post(
                url,
                headers=headers,
                json=payload
            )


        if response.status_code == 200:

            data = response.json()

            candidates = data.get(
                "candidates",
                []
            )


            if candidates:

                content = candidates[0].get(
                    "content",
                    {}
                )


                parts = content.get(
                    "parts",
                    []
                )


                if parts:

                    text = parts[0].get(
                        "text"
                    )


                    if text:

                        return text.strip()


    except Exception as error:

        print(
            "Gemini API error:",
            str(error)
        )


    # Always return a valid response
    return create_fallback_response(
        context
    )


def create_fallback_response(context):

    if context.startswith(
        "No relevant knowledge-base information"
    ):

        return (
            "I couldn't find a relevant solution "
            "for this issue in the current IT "
            "support knowledge base. Please provide "
            "more details about the problem."
        )


    # Extract only the solution
    if "Solution:" in context:

        solution = context.split(
            "Solution:",
            1
        )[1].strip()

        return solution


    return context