from django.shortcuts import render, get_object_or_404
from .models import Post


def home(request):
    context = {}
    return render(request, "blog/home.html", context)


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    similar = Post.objects.filter(is_published=True).exclude(pk=post.pk).order_by("-created_at")[:3]
    context = {"post": post, "similar": similar}
    return render(request, "blog/post_detail.html", context)


def about(request):
    context = {}
    return render(request, "blog/about.html", context)