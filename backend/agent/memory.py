import json
import os
from models.user_state import UserState

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "user_data.json")


def _load_all() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_all(data: dict) -> None:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_user(user_id: str) -> UserState:
    all_data = _load_all()
    if user_id in all_data:
        return UserState.from_dict(all_data[user_id])
    return UserState(user_id=user_id)


def save_user(state: UserState) -> None:
    all_data = _load_all()
    all_data[state.user_id] = state.to_dict()
    _save_all(all_data)


def append_task_history(state: UserState, task: str, feedback: str | None) -> None:
    """Record what the user was asked to do and how they responded."""
    state.task_history.append({"task": task, "feedback": feedback})
    # Keep only the last 50 entries to avoid unbounded growth
    state.task_history = state.task_history[-50:]
