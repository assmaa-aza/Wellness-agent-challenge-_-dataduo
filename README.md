# خطوة — Khotwa

> Un pas. Une action. Maintenant.

Agent IA anti-procrastination qui décompose n'importe quelle tâche en **une seule micro-action impossible à refuser**.

---

## 🚀 Installation rapide

### 1. Cloner et préparer l'environnement

```bash
git clone <repo-url>
cd Khotwa

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurer la clé API

Crée un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=sk-...
```

Ou exporte-la directement :

```bash
export OPENAI_API_KEY=sk-...
```

### 3. Lancer le backend

```bash
cd backend
python app.py
```

Le serveur démarre sur `http://localhost:5000`.

### 4. Ouvrir le frontend

Ouvre simplement `frontend/index.html` dans ton navigateur.  
Pour éviter les problèmes CORS avec Chrome, tu peux utiliser :

```bash
cd frontend
python -m http.server 8080
# puis ouvre http://localhost:8080
```

---

## 📁 Structure du projet

```
Khotwa/
├── backend/
│   ├── app.py                  # Point d'entrée Flask
│   ├── agent/
│   │   ├── controller.py       # Boucle principale de l'agent
│   │   ├── reasoning.py        # Analyse via OpenAI
│   │   ├── decision.py         # Ajustement de la difficulté
│   │   └── memory.py           # Persistance de l'état utilisateur
│   ├── services/
│   │   ├── openai_service.py   # Wrapper OpenAI API
│   │   └── task_generator.py   # Générateur de tâches de secours
│   ├── models/
│   │   ├── user_state.py       # Dataclass état utilisateur
│   │   └── task.py             # Dataclass micro-tâche
│   └── utils/
│       └── helpers.py          # Utilitaires (scaling, encouragements)
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── data/
│   └── user_data.json          # Stockage JSON des états utilisateurs
├── requirements.txt
└── README.md
```

---

## 🔌 API endpoints

### `POST /chat`
Envoie un message et obtient une micro-tâche.

```json
// Request
{
  "user_id": "alice",
  "message": "je dois faire un rapport mais je bloque",
  "feedback": null
}

// Response
{
  "task": "Ouvre ton document",
  "difficulty": 2,
  "category": "writing",
  "encouragement": null,
  "blocage_type": "surcharge",
  "streak": 0
}
```

### `POST /chat` (avec feedback)
```json
{
  "user_id": "alice",
  "message": "je dois faire un rapport",
  "feedback": "fait"
}
```

### `POST /reset`
Réinitialise l'état d'un utilisateur.
```json
{ "user_id": "alice" }
```

---

## 🧠 Comment ça marche

```
Message utilisateur
        │
        ▼
  controller.py ──► memory.py (charger l'état)
        │
        ├──► reasoning.py ──► OpenAI API (analyser le blocage)
        │
        ├──► decision.py (ajuster la difficulté selon le feedback)
        │
        └──► memory.py (sauvegarder) ──► Réponse JSON
```

---

## 🔮 Pistes d'évolution

- Intégration Google Calendar (rappels intelligents)
- Notifications push (web/mobile)
- Gamification (niveaux, badges)
- Analyse comportementale long terme
- Version mobile React Native
