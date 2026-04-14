"""
Fallback task generation without AI — used when the API is unavailable
or for seeding the very first interaction.
"""

DIFFICULTY_TEMPLATES = {
    "writing": {
        1: "Écris 1 mot.",
        2: "Écris une phrase.",
        3: "Écris un paragraphe court.",
        4: "Rédige une section complète.",
        5: "Écris tout le contenu de cette partie.",
    },
    "reading": {
        1: "Lis le titre du document.",
        2: "Lis l'introduction.",
        3: "Lis les 2 premières pages.",
        4: "Lis un chapitre entier.",
        5: "Termine le document.",
    },
    "admin": {
        1: "Ouvre le fichier concerné.",
        2: "Remplis un seul champ.",
        3: "Complète une section du formulaire.",
        4: "Finalise le document.",
        5: "Envoie le tout.",
    },
    "coding": {
        1: "Ouvre ton éditeur de code.",
        2: "Écris le nom de la fonction.",
        3: "Implémente une fonction simple.",
        4: "Écris les tests pour ce module.",
        5: "Finalise et commite le tout.",
    },
    "other": {
        1: "Commence par juste t'asseoir et respirer.",
        2: "Prépare ton espace de travail.",
        3: "Fais la première petite étape.",
        4: "Continue jusqu'à mi-chemin.",
        5: "Termine cette tâche.",
    },
}


def get_fallback_task(category: str, difficulty: int) -> str:
    cat = category if category in DIFFICULTY_TEMPLATES else "other"
    diff = max(1, min(5, difficulty))
    return DIFFICULTY_TEMPLATES[cat][diff]
