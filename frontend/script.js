/* ─── Config ──────────────────────────────────────────────── */
const API_BASE = "http://localhost:5000";
const USER_ID  = "user_" + Math.random().toString(36).slice(2, 8); // simple per-session ID

/* ─── State ───────────────────────────────────────────────── */
let hasTask     = false;   // Whether the agent has given a task yet
let lastMessage = "";      // Last user message (to resend with feedback)

/* ─── DOM refs ────────────────────────────────────────────── */
const taskText      = document.getElementById("taskText");
const blocageBadge  = document.getElementById("blocageBadge");
const streakDisplay = document.getElementById("streakDisplay");
const streakCount   = document.getElementById("streakCount");
const encouragement = document.getElementById("encouragement");
const feedbackRow   = document.getElementById("feedbackRow");
const diffDots      = document.getElementById("diffDots").querySelectorAll(".dot");
const userInput     = document.getElementById("userInput");
const sendBtn       = document.getElementById("sendBtn");

/* ─── Keyboard shortcut ───────────────────────────────────── */
function handleKey(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
}

/* ─── Send initial message ────────────────────────────────── */
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  lastMessage = message;
  userInput.value = "";
  await callAgent(message, null);
}

/* ─── Send feedback ───────────────────────────────────────── */
async function sendFeedback(feedback) {
  // Disable buttons briefly to prevent double-tap
  feedbackRow.querySelectorAll("button").forEach(b => b.disabled = true);
  await callAgent(lastMessage, feedback);
  feedbackRow.querySelectorAll("button").forEach(b => b.disabled = false);
}

/* ─── Core API call ───────────────────────────────────────── */
async function callAgent(message, feedback) {
  setLoading(true);

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: USER_ID, message, feedback }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Erreur serveur ${res.status}`);
    }

    const data = await res.json();
    renderResponse(data);

  } catch (err) {
    console.error(err);
    showError("Impossible de contacter l'agent. Vérifie que le backend tourne sur le port 5000.");
  } finally {
    setLoading(false);
  }
}

/* ─── Render response ─────────────────────────────────────── */
function renderResponse(data) {
  // Task text with animation
  taskText.classList.remove("new-task");
  void taskText.offsetWidth; // reflow trick to re-trigger animation
  taskText.textContent = data.task;
  taskText.classList.add("new-task");

  // Blocage badge
  const bt = data.blocage_type || "other";
  blocageBadge.textContent = badgeLabel(bt);
  blocageBadge.className = `badge ${bt}`;

  // Encouragement
  if (data.encouragement) {
    encouragement.textContent = data.encouragement;
    encouragement.classList.add("visible");
    setTimeout(() => encouragement.classList.remove("visible"), 3500);
  } else {
    encouragement.textContent = "";
    encouragement.classList.remove("visible");
  }

  // Difficulty dots
  const diff = data.difficulty || 1;
  diffDots.forEach((dot, i) => {
    dot.classList.toggle("active", i < diff);
  });

  // Streak
  if (data.streak > 1) {
    streakCount.textContent = data.streak;
    streakDisplay.style.display = "flex";
  } else {
    streakDisplay.style.display = "none";
  }

  // Show feedback buttons after first task
  hasTask = true;
  feedbackRow.style.display = "flex";
}

/* ─── Loading state ───────────────────────────────────────── */
function setLoading(active) {
  if (active) {
    taskText.classList.add("loading");
    sendBtn.innerHTML = `<span class="spinner"></span>`;
    sendBtn.disabled = true;
  } else {
    taskText.classList.remove("loading");
    sendBtn.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <line x1="22" y1="2" x2="11" y2="13"/>
        <polygon points="22 2 15 22 11 13 2 9 22 2"/>
      </svg>`;
    sendBtn.disabled = false;
  }
}

/* ─── Error display ───────────────────────────────────────── */
function showError(msg) {
  taskText.textContent = `⚠️ ${msg}`;
  taskText.classList.remove("loading");
}

/* ─── Reset session ───────────────────────────────────────── */
async function resetSession() {
  try {
    await fetch(`${API_BASE}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: USER_ID }),
    });
  } catch (_) {}

  taskText.innerHTML = `Dis-moi ce qui te bloque.<br/>Je vais te donner <em>une seule</em> action.`;
  blocageBadge.textContent = "En attente…";
  blocageBadge.className = "badge";
  encouragement.textContent = "";
  encouragement.classList.remove("visible");
  feedbackRow.style.display = "none";
  streakDisplay.style.display = "none";
  diffDots.forEach(d => d.classList.remove("active"));
  hasTask = false;
  userInput.focus();
}

/* ─── Helpers ─────────────────────────────────────────────── */
function badgeLabel(type) {
  const labels = {
    fatigue:   "😴 Fatigue",
    confusion: "🤔 Confusion",
    surcharge: "🌊 Surcharge",
    other:     "🎯 Focus",
  };
  return labels[type] || "🎯 Focus";
}

/* ─── Init ────────────────────────────────────────────────── */
userInput.focus();
