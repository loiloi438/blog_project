"""Service pour générer des URLs d'images basées sur les mots-clés.

Fonctions:
- _clean_keywords(title): nettoie le titre pour garder les mots-clés
- get_image_url_from_title(title, size): retourne une URL Unsplash
- get_thumbnail_image_url(title): raccourci pour la vignette
"""

import re
import unicodedata
from typing import Optional


def _clean_keywords(title: Optional[str]) -> str:
    """Nettoie un titre en supprimant les caractères non alphanumériques
    et conserve les trois premiers mots.
    """
    keywords = (title or "").lower()
    # Normaliser Unicode (supprimer accents) puis supprimer les caractères spéciaux
    keywords = unicodedata.normalize('NFKD', keywords)
    keywords = keywords.encode('ascii', 'ignore').decode('ascii')
    keywords = re.sub(r"[^\w\s]", "", keywords)
    # Garder les 3 premiers mots
    keywords = " ".join(keywords.split()[:3])
    return keywords or "blog"


def get_image_url_from_title(title: Optional[str], size: str = "medium", seed: Optional[str] = None) -> str:
    """Retourne une URL d'image en utilisant Picsum (seedable) basée sur le titre.

    size: 'thumb' -> 400x300, 'medium' -> 800x400, 'large' -> 1200x400
    seed: facultatif, si fourni sera utilisé pour garantir une image stable/unique.
    """
    keywords = _clean_keywords(title)
    if size == "thumb":
        w, h = 400, 300
    elif size == "large":
        w, h = 1200, 400
    else:
        w, h = 800, 400

    # Prefer seed if provided (e.g., article.pk), else use cleaned keywords
    use_seed = seed or keywords.replace(' ', '-') or 'blog'
    # Picsum seeded URL
    return f"https://picsum.photos/seed/{use_seed}/{w}/{h}"


def get_thumbnail_image_url(title: Optional[str]) -> str:
    return get_image_url_from_title(title, size="thumb")

