import os
import sys

# Make sure all local packages resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
from agent.controller import run_agent

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend served on a different port


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Khotwa agent running ✅"})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Expected JSON body:
    {
        "user_id": "alice",          # optional, defaults to "default"
        "message": "je dois faire un rapport",
        "feedback": "fait" | "trop_dur" | null
    }
    """
    data = request.get_json(force=True)
    if not data or "message" not in data:
        return jsonify({"error": "Le champ 'message' est requis."}), 400

    user_id = data.get("user_id", "default")
    message = data["message"].strip()
    feedback = data.get("feedback")  # "fait" | "trop_dur" | None

    if not message:
        return jsonify({"error": "Le message ne peut pas être vide."}), 400

    result = run_agent(user_id=user_id, message=message, feedback=feedback)
    return jsonify(result)


@app.route("/reset", methods=["POST"])
def reset():
    """Reset a user's state — useful for demos."""
    data = request.get_json(force=True) or {}
    user_id = data.get("user_id", "default")

    from agent.memory import save_user
    from models.user_state import UserState
    save_user(UserState(user_id=user_id))
    return jsonify({"status": f"État de '{user_id}' réinitialisé."})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
