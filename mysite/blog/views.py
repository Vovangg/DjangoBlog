from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm


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