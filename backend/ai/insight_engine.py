"""
AI Insight Engine
==================
Generates human-readable insights from user data using the OpenAI API.
Configure the OPENAI_API_KEY environment variable to enable live responses.
When the key is absent the engine returns a placeholder message so the rest
of the application keeps working without an API key.
"""

import os

_SYSTEM_PROMPT = """You are a personal productivity and wellness coach.
The user has provided their daily behavioural data (screen time, study hours,
sleep, exercise, expenses).  Answer their question in a clear, empathetic, and
actionable manner.  Keep the response concise (3-5 sentences)."""


def generate_insight(question: str, context: str | None = None) -> str:
    """
    Generate an AI insight for *question*.

    If ``OPENAI_API_KEY`` is set the function calls the OpenAI Chat Completions
    API.  Otherwise it returns a clearly labelled placeholder.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "[AI Insight – placeholder] "
            "Set the OPENAI_API_KEY environment variable to enable live AI responses. "
            f"Your question was: '{question}'"
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
        messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:  # noqa: BLE001
        return f"[AI Insight error] {exc}"
