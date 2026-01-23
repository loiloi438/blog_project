"""
Contexte template personnalisé pour ajouter les images générées
"""
from django import template
from django.templatetags.static import static
import re
from .. import image_service

register = template.Library()


@register.filter
def generate_image_url(title):
    """Legacy filter: generate medium unsplash image from title."""
    return image_service.get_image_url_from_title(title, size='medium')


@register.filter
def generate_thumbnail_url(title):
    """Legacy filter: generate thumbnail unsplash image from title."""
    return image_service.get_thumbnail_image_url(title)


@register.simple_tag
def article_image(article, size='medium'):
    """
    Retourne l'URL de l'image pour un `article`:
    1) l'image uploadée (`article.cover_image`) si présente
    2) sinon une image Unsplash générée selon le titre
    3) sinon une image statique par défaut
    Usage: {% article_image article 'large' %}
    """
    # 1) couverture uploadée
    try:
        if hasattr(article, 'cover_image') and article.cover_image:
            return article.cover_image.url
    except Exception:
        pass

    # 2) Unsplash
    try:
        # Prefer using the article PK as seed so each article has a stable, unique image
        pk = getattr(article, 'pk', None)
        title = getattr(article, 'title', '') or ''
        return image_service.get_image_url_from_title(title, size=size, seed=str(pk) if pk else None)
    except Exception:
        pass

    # 3) fallback statique
    return static('images/default_article.svg')
