import json
from dataclasses import dataclass

from groq import Groq

from app.core.config import settings


@dataclass
class InteractionAIResult:
    summary: str
    sentiment: str
    suggested_follow_up: str
    provider: str


POSITIVE_WORDS = {
    "interested",
    "positive",
    "agreed",
    "requested",
    "engaged",
    "helpful",
}

NEGATIVE_WORDS = {
    "concern",
    "concerns",
    "rejected",
    "negative",
    "unhappy",
    "objection",
    "objections",
}


def analyze_interaction_fallback(notes: str) -> InteractionAIResult:
    cleaned_notes = " ".join(notes.split())
    lowered_notes = cleaned_notes.lower()

    positive_score = sum(
        word in lowered_notes
        for word in POSITIVE_WORDS
    )

    negative_score = sum(
        word in lowered_notes
        for word in NEGATIVE_WORDS
    )

    if positive_score > negative_score:
        sentiment = "positive"
    elif negative_score > positive_score:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    if len(cleaned_notes) > 240:
        summary = cleaned_notes[:237].rstrip() + "..."
    else:
        summary = cleaned_notes

    if "safety" in lowered_notes:
        suggested_follow_up = (
            "Share relevant safety evidence and schedule a follow-up discussion."
        )
    elif "data" in lowered_notes or "evidence" in lowered_notes:
        suggested_follow_up = (
            "Share supporting clinical evidence and confirm next steps."
        )
    else:
        suggested_follow_up = (
            "Schedule a follow-up to confirm needs and next actions."
        )

    return InteractionAIResult(
        summary=summary,
        sentiment=sentiment,
        suggested_follow_up=suggested_follow_up,
        provider="groq",
    )


def analyze_interaction(notes: str) -> InteractionAIResult:
    if not settings.groq_api_key:
        return analyze_interaction_fallback(notes)

    try:
        client = Groq(api_key=settings.groq_api_key)

        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze healthcare professional CRM interaction notes. "
                        "Return only valid JSON with exactly these keys: "
                        "summary, sentiment, suggested_follow_up. "
                        "The sentiment must be positive, neutral, or negative. "
                        "Do not include markdown or extra text."
                    ),
                },
                {
                    "role": "user",
                    "content": notes,
                },
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Groq returned empty content.")

        data = json.loads(content)

        summary = str(data["summary"]).strip()
        sentiment = str(data["sentiment"]).strip().lower()
        suggested_follow_up = str(
            data["suggested_follow_up"]
        ).strip()

        if sentiment not in {"positive", "neutral", "negative"}:
            raise ValueError("Invalid sentiment returned by Groq.")

        if not summary or not suggested_follow_up:
            raise ValueError("Incomplete analysis returned by Groq.")

        return InteractionAIResult(
            summary=summary,
            sentiment=sentiment,
            suggested_follow_up=suggested_follow_up,
        )

    except Exception:
        return analyze_interaction_fallback(notes)