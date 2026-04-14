from services.openai_service import analyze_message
from services.task_generator import get_fallback_task
from utils.helpers import clamp


def reason(user_message: str, history: list, difficulty: int) -> dict:
    """
    Call the AI to understand the user's blocage and propose a micro-task.
    Falls back to template-based generation if the API call fails.

    Returns a dict:
      { blocage_type, suggested_task, category, difficulty }
    """
    try:
        result = analyze_message(user_message, history, difficulty_hint=difficulty)
        # Validate required keys
        result.setdefault("blocage_type", "other")
        result.setdefault("category", "other")
        result["difficulty"] = clamp(int(result.get("difficulty", difficulty)), 1, 5)
        return result
    except Exception as exc:
        print(f"[reasoning] OpenAI call failed: {exc}")
        fallback_task = get_fallback_task("other", difficulty)
        return {
            "blocage_type": "other",
            "suggested_task": fallback_task,
            "category": "other",
            "difficulty": difficulty,
        }
