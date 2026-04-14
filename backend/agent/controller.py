from agent.memory import load_user, save_user, append_task_history
from agent.reasoning import reason
from agent.decision import decide


def run_agent(user_id: str, message: str, feedback: str | None = None) -> dict:
    """
    Main agent loop:
      1. Load user state from memory
      2. Append feedback from previous turn (if any)
      3. Run reasoning (AI call)
      4. Run decision (difficulty adjustment)
      5. Persist updated state
      6. Return the response dict for the API
    """
    # 1. Load state
    state = load_user(user_id)

    # 2. Record feedback on the previous task
    if feedback and state.current_task:
        append_task_history(state, state.current_task, feedback)
        if feedback == "fait":
            state.streak += 1
        else:
            state.streak = 0

    # 3. Reasoning
    reasoning_result = reason(
        user_message=message,
        history=state.history,
        difficulty=state.current_difficulty,
    )

    # 4. Decision
    task = decide(
        reasoning=reasoning_result,
        feedback=feedback,
        current_difficulty=state.current_difficulty,
    )

    # 5. Update state
    state.current_task = task.content
    state.current_difficulty = task.difficulty
    state.blocage_type = reasoning_result["blocage_type"]

    # Keep conversation history (last 20 turns)
    state.history.append({"role": "user", "content": message})
    state.history.append({"role": "assistant", "content": task.content})
    state.history = state.history[-20:]

    save_user(state)

    # 6. Return response
    return {
        "task": task.content,
        "difficulty": task.difficulty,
        "category": task.category,
        "encouragement": task.encouragement,
        "blocage_type": state.blocage_type,
        "streak": state.streak,
    }
