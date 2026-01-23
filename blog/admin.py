from django.contrib import admin
from .models import Article, Comment, Like


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations', {
            'fields': ('title', 'author', 'content', 'cover_image')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Commentaires'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at', 'is_reply')
    list_filter = ('created_at', 'author', 'article')
    search_fields = ('body', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

    def is_reply(self, obj):
        return 'Oui' if obj.parent else 'Non'
    is_reply.short_description = 'Est une réponse?'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('article', 'get_author', 'get_ip', 'created_at')
    list_filter = ('created_at', 'article', 'user')
    search_fields = ('article__title', 'user__username', 'ip_address')
    readonly_fields = ('created_at', 'article')

    def get_author(self, obj):
        return obj.user.username if obj.user else f"Anonyme ({obj.ip_address})"
    get_author.short_description = 'Auteur'

    def get_ip(self, obj):
        return obj.ip_address if obj.ip_address else "N/A"
    get_ip.short_description = 'Adresse IP'
