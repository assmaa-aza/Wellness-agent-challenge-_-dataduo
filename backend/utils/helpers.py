import re


def clean_text(text: str) -> str:
    """Strip extra whitespace and normalise line endings."""
    return re.sub(r"\s+", " ", text.strip())


def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp an integer between min_val and max_val."""
    return max(min_val, min(max_val, value))


def scale_difficulty(current: int, feedback: str | None) -> int:
    """
    Adjust difficulty level based on user feedback.
    feedback: "fait" | "trop_dur" | None
    """
    if feedback == "trop_dur":
        return clamp(current - 1, 1, 5)
    elif feedback == "fait":
        return clamp(current + 1, 1, 5)
    return current


ENCOURAGEMENTS = {
    "fait": [
        "Excellent ! 🎉 Tu avances !",
        "Super ! Chaque pas compte. 💪",
        "Parfait ! Continue comme ça ! ✅",
        "Bravo ! Tu es en train de le faire ! 🚀",
    ],
    "trop_dur": [
        "Pas de souci, on simplifie. 😌",
        "Aucun problème, une étape plus petite. 🔽",
        "On y va doucement. Voici quelque chose de plus simple.",
    ],
}


def get_encouragement(feedback: str | None) -> str | None:
    import random
    if feedback in ENCOURAGEMENTS:
        return random.choice(ENCOURAGEMENTS[feedback])
    return None
