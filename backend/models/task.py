from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    content: str                   # The micro-task text shown to user
    difficulty: int                # 1–5
    category: str                  # e.g. "writing", "reading", "admin"
    encouragement: Optional[str] = None   # Short motivational message

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "difficulty": self.difficulty,
            "category": self.category,
            "encouragement": self.encouragement,
        }
