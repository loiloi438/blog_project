from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.db import IntegrityError, transaction
import traceback
from django.db import IntegrityError
import logging
from pathlib import Path

# Logger for like toggles: write traces to logs/like_errors.log
logs_dir = Path(__file__).resolve().parent.parent / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)
like_log = logging.getLogger('blog.toggle_like')
if not like_log.handlers:
    fh = logging.FileHandler(logs_dir / 'like_errors.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    like_log.addHandler(fh)
like_log.setLevel(logging.DEBUG)
from .models import Article, Comment, Like
from .forms import CustomUserCreationForm, UserLoginForm, ArticleForm, CommentForm


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ========== VUE D'ACCUEIL ==========
def home(request):
    """Page d'accueil avec la liste des articles"""
    articles = Article.objects.all()
    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'total_users': User.objects.count()
    }
    return render(request, 'blog/home.html', context)


# ========== AUTHENTIFICATION ==========
def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """Connexion d'un utilisateur"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = UserLoginForm()

    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    """Déconnexion d'un utilisateur"""
    logout(request)
    return redirect('home')


# ========== GESTION DES ARTICLES ==========
def article_list(request):
    """Liste des articles (alternative à home)"""
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'blog/article_list.html', context)


@login_required(login_url='login')
def article_create(request):
    """Créer un nouvel article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Créer un article'})


def article_detail(request, pk):
    """Détail d'un article avec commentaires"""
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.filter(parent__isnull=True)  # Seulement les commentaires parents
    other_articles = article.author.articles.exclude(pk=pk).order_by('-created_at')[:5]

    # Vérifier si l'utilisateur actuel a aimé (seulement pour utilisateurs authentifiés)
    user_likes = False
    if request.user.is_authenticated:
        user_likes = Like.objects.filter(article=article, user=request.user).exists()

    context = {
        'article': article,
        'comments': comments,
        'other_articles': other_articles,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
        'user_likes': user_likes,
    }
    return render(request, 'blog/article_detail.html', context)


@login_required(login_url='login')
def article_edit(request, pk):
    """Modifier un article (seulement l'auteur)"""
    article = get_object_or_404(Article, pk=pk)

    # Vérifier que c'est l'auteur
    if article.author != request.user and not request.user.is_staff:
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {'form': form, 'article': article, 'title': 'Modifier l\'article'})


@login_required(login_url='login')
def article_delete(request, pk):
    """Supprimer un article (seulement l'auteur)"""
    article = get_object_or_404(Article, pk=pk)

    # Vérifier que c'est l'auteur
    if article.author != request.user and not request.user.is_staff:
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        article.delete()
        return redirect('home')

    return render(request, 'blog/article_confirm_delete.html', {'article': article})


# ========== SYSTÈME DE LIKES ==========
@require_http_methods(["POST"])
def toggle_like(request, pk):
    """Ajouter/retirer un like sur un article (supports utilisateurs authentifiés et anonymes)"""
    article = get_object_or_404(Article, pk=pk)
    # Debug logging to trace client requests during development
    try:
        like_log.debug(f"[toggle_like] user={request.user} authenticated={request.user.is_authenticated} path={request.path} X-Requested-With={request.headers.get('X-Requested-With')} csrf_cookie={'csrftoken' in request.COOKIES}")
    except Exception:
        like_log.exception('Failed to log toggle_like entry')
    # Support both authenticated users and anonymous visitors (via IP) for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            if request.user.is_authenticated:
                ip = get_client_ip(request)
                # first look for a user-associated like
                like_obj = Like.objects.filter(article=article, user=request.user).first()
                if like_obj:
                    # delete user like and also any anonymous like from same IP
                    with transaction.atomic():
                        like_log.debug(f"[toggle_like] deleting user like (user={request.user})")
                        like_obj.delete()
                        if ip:
                            anon_deleted = Like.objects.filter(article=article, ip_address=ip).delete()
                            if anon_deleted[0]:
                                like_log.debug(f"[toggle_like] also deleted anonymous like(s) for ip={ip}")
                    liked = False
                else:
                    # create user like and remove anonymous like from same IP to avoid duplicates
                    try:
                        with transaction.atomic():
                            like_log.debug(f"[toggle_like] creating user like (user={request.user})")
                            Like.objects.create(article=article, user=request.user)
                            if ip:
                                anon_deleted = Like.objects.filter(article=article, ip_address=ip).delete()
                                if anon_deleted[0]:
                                    like_log.debug(f"[toggle_like] removed anonymous like(s) for ip={ip} after creating user like")
                        liked = True
                    except IntegrityError as ie:
                        like_log.debug('[toggle_like] IntegrityError creating user like, retrying lookup %s', ie)
                        like_obj = Like.objects.filter(article=article, user=request.user).first()
                        liked = bool(like_obj)
            else:
                # anonymous like via IP
                ip = get_client_ip(request)
                if not ip:
                    return JsonResponse({'error': 'no_ip'}, status=400)
                like_obj = Like.objects.filter(article=article, ip_address=ip).first()
                if like_obj:
                    with transaction.atomic():
                        like_log.debug(f"[toggle_like] deleting anonymous like for ip={ip}")
                        like_obj.delete()
                    liked = False
                else:
                    try:
                        with transaction.atomic():
                            Like.objects.create(article=article, ip_address=ip)
                        liked = True
                    except IntegrityError as ie:
                        like_log.debug('[toggle_like] IntegrityError on anonymous create, retrying lookup %s', ie)
                        like_obj = Like.objects.filter(article=article, ip_address=ip).first()
                        liked = bool(like_obj)
            return JsonResponse({
                'liked': liked,
                'likes_count': article.likes.count()
            })
        except Exception as exc:
            # Log full traceback to file and return JSON error for client
            like_log.exception('[toggle_like] exception: %s', exc)
            return JsonResponse({'error': 'server_error', 'message': str(exc)}, status=500)

    # Non-AJAX requests: require authentication and redirect to login
    if not request.user.is_authenticated:
        return redirect('login')

    return redirect('article_detail', pk=pk)


# ========== SYSTÈME DE COMMENTAIRES ==========
@login_required(login_url='login')
def add_comment(request, pk):
    """Ajouter un commentaire ou une réponse à un article"""
    article = get_object_or_404(Article, pk=pk)
    parent_id = request.POST.get('parent_id')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user

            # Si c'est une réponse
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect('article_detail', pk=article.pk)

    return redirect('article_detail', pk=pk)


@login_required(login_url='login')
def comment_delete(request, pk):
    """Supprimer un commentaire (seulement l'auteur)"""
    comment = get_object_or_404(Comment, pk=pk)
    article = comment.article

    # Vérifier que c'est l'auteur
    if comment.author != request.user and not request.user.is_staff:
        return redirect('article_detail', pk=article.pk)

    if request.method == 'POST':
        comment.delete()

    return redirect('article_detail', pk=article.pk)


# ========== RECHERCHE (BONUS) ==========
def search_articles(request):
    """Rechercher des articles"""
    query = request.GET.get('q', '')
    articles = Article.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else Article.objects.none()

    context = {
        'articles': articles,
        'query': query
    }
    return render(request, 'blog/search_results.html', context)
