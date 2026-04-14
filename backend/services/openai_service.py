import json
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY", "")

SYSTEM_PROMPT = """Tu es Khotwa, un agent anti-procrastination.
Ton rôle est d'analyser le message de l'utilisateur et de proposer UNE seule micro-action.

Règles absolues :
- La tâche doit être si petite qu'elle est impossible à refuser
- Jamais de conseil long
- Jamais de liste
- UNE seule action concrète

Réponds UNIQUEMENT avec un objet JSON valide (pas de markdown, pas de texte autour) :
{
  "blocage_type": "fatigue" | "confusion" | "surcharge" | "other",
  "suggested_task": "texte de la micro-action",
  "category": "writing" | "reading" | "admin" | "coding" | "other",
  "difficulty": 1 à 5 (1 = trivial, 5 = effort réel)
}"""


def analyze_message(user_message: str, history: list, difficulty_hint: int = 3) -> dict:
    """
    Call the OpenAI API to analyse the user's message.
    Returns a dict with keys: blocage_type, suggested_task, category, difficulty.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history[-10:],  # last 10 turns for context window efficiency
        {
            "role": "user",
            "content": (
                f"[Niveau de difficulté cible: {difficulty_hint}/5]\n"
                f"{user_message}"
            ),
        },
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=300,
    )

    raw = response.choices[0].message.content
    return json.loads(raw)
