from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UserState:
    user_id: str
    current_task: Optional[str] = None
    current_difficulty: int = 3  # 1 (easiest) to 5 (hardest)
    blocage_type: Optional[str] = None  # fatigue | confusion | surcharge | other
    history: List[dict] = field(default_factory=list)  # conversation history
    task_history: List[dict] = field(default_factory=list)  # completed/failed tasks
    streak: int = 0  # consecutive "fait" responses

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "current_task": self.current_task,
            "current_difficulty": self.current_difficulty,
            "blocage_type": self.blocage_type,
            "history": self.history,
            "task_history": self.task_history,
            "streak": self.streak,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserState":
        return UserState(
            user_id=data.get("user_id", "default"),
            current_task=data.get("current_task"),
            current_difficulty=data.get("current_difficulty", 3),
            blocage_type=data.get("blocage_type"),
            history=data.get("history", []),
            task_history=data.get("task_history", []),
            streak=data.get("streak", 0),
        )
