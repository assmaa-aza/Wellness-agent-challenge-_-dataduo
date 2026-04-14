from models.task import Task
from utils.helpers import scale_difficulty, get_encouragement, clamp


def decide(reasoning: dict, feedback: str | None, current_difficulty: int) -> Task:
    """
    Given the reasoning output and the latest user feedback,
    decide what micro-task to surface next and at what difficulty.

    feedback: "fait" | "trop_dur" | None
    """
    new_difficulty = scale_difficulty(current_difficulty, feedback)

    # If the AI already returned a difficulty suggestion, blend it in
    ai_difficulty = reasoning.get("difficulty", new_difficulty)
    # Weighted average: 70% our adjustment, 30% AI suggestion
    blended = round(0.7 * new_difficulty + 0.3 * ai_difficulty)
    final_difficulty = clamp(blended, 1, 5)

    encouragement = get_encouragement(feedback)

    return Task(
        content=reasoning["suggested_task"],
        difficulty=final_difficulty,
        category=reasoning.get("category", "other"),
        encouragement=encouragement,
    )
