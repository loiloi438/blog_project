from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    """Modèle pour les articles du blog"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    cover_image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name="Image de couverture")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class Like(models.Model):
    """Modèle pour les likes (support utilisateurs authentifiés et anonymes)"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='article_likes')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['article', 'user'], ['article', 'ip_address']]
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        if self.user:
            return f"Like de {self.user.username} sur '{self.article.title}'"
        return f"Like anonyme sur '{self.article.title}' ({self.ip_address})"


class Comment(models.Model):
    """Modèle pour les commentaires (avec support des réponses hiérarchiques)"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __str__(self):
        return f"Commentaire de {self.author.username} sur '{self.article.title}'"

    def get_replies(self):
        """Récupère les réponses directes à ce commentaire"""
        return self.replies.all()
