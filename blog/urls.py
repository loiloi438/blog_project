from django.urls import path
from . import views


urlpatterns = [

    # Accueil
    path('', views.home, name='home'),

    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),

    # Likes
    path('article/<int:pk>/like/', views.toggle_like, name='toggle_like'),

    # Commentaires
    path('article/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # Recherche
    path('search/', views.search_articles, name='search'),
]
