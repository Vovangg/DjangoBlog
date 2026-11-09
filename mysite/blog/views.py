from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm


def home(request):
    context = {}
    return render(request, "blog/home.html", context)


def post_list(request):
    query = request.GET.get("q", "").strip()
    posts_qs = Post.objects.filter(is_published=True).order_by("-created_at")

    if query:
        # ищем по заголовку или тексту
        posts_qs = posts_qs.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    # разбиваем по 5 на страницу
    paginator = Paginator(posts_qs, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "posts": page_obj,
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = post.comments.all().order_by("-created_at") # получаем комменты
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # пока не сохраняем в БД
            comment.post = post              # привязываем к текущему посту
            comment.save()                   # теперь сохраняем
            return redirect("post_detail", slug=post.slug) # перезагружаем страницу
    else:
        form = CommentForm()

    # добавляем в контекст похожие посты
    similar = Post.objects.filter(is_published=True).exclude(pk=post.pk).order_by("-created_at")[:3]
    
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar": similar,
    }
    return render(request, "blog/post_detail.html", context)


def about(request):
    context = {}
    return render(request, "blog/about.html", context)

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", slug=post.slug) # ВАЖНО: slug вместо pk
    else:
        form = PostForm()
    
    context = {"form": form}
    return render(request, "blog/post_form.html", context)

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {"form": form, "post": post}
    return render(request, "blog/post_form_edit.html", context)

def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect("post_list")

    context = {"post": post}
    return render(request, "blog/post_confirm_delete.html", context)