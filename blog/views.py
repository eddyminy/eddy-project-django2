from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm


# --- Solo requiere login ---
@login_required
def article_list(request):
    """Cualquier usuario autenticado puede ver la lista.
    Muestra articulos publicados y los no publicados del usuario actual."""
    from django.db.models import Q
    articles = Article.objects.filter(
        Q(published=True) | Q(author=request.user)
    ).distinct()
    return render(request, 'blog/article_list.html', {'articles': articles})


# --- Requiere permiso especifico ---
@permission_required('blog.add_article', raise_exception=True)
def article_create(request):
    """Solo usuarios con permiso 'add_article' pueden crear."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            # Si marcó publicar y tiene permiso, publicar el articulo
            if form.cleaned_data.get('publish') and request.user.has_perm('blog.publish_article'):
                article.published = True
            article.save()
            messages.success(request, 'Articulo creado.' + (' y publicado.' if article.published else ''))
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


# --- Requiere login + permiso (combinados) ---
@login_required
@permission_required('blog.delete_article', raise_exception=True)
def article_delete(request, pk):
    """Solo usuarios con permiso 'delete_article' pueden eliminar."""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Articulo eliminado.')
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


# --- Permiso personalizado ---
@permission_required('blog.publish_article', raise_exception=True)
def article_publish(request, pk):
    """Solo Editores pueden publicar articulos."""
    article = get_object_or_404(Article, pk=pk)
    article.published = True
    article.save()
    messages.success(request, f'"{article.title}" ha sido publicado.')
    return redirect('article_list')
