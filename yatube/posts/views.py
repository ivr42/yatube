from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import SlugField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User

POSTS_PER_PAGE = 10


def index(request: HttpRequest) -> HttpResponse:
    template = "posts/index.html"
    posts = Post.objects.all()

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Последние обновления на сайте",
        "page_obj": page_obj,
        "index": True,
    }

    return render(request, template, context)


def group_posts(request: HttpRequest, slug: SlugField) -> HttpResponse:
    """To view posts in certain community"""
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "group": group,
        "page_obj": page_obj,
    }

    return render(request, template, context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """To view user profile and his posts"""
    template = "posts/profile.html"
    author = get_object_or_404(User, username=username)

    following = (
        request.user.is_authenticated
        and User.objects.filter(
            username=author, following__user=request.user
        ).exists()
    )

    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "username": author,
        "posts_count": posts.count(),
        "page_obj": page_obj,
        "following": following,
    }
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """To view single post"""
    template = "posts/post_detail.html"
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.filter(author=post.author).count()
    comments = Comment.objects.filter(post=post)

    context = {
        "post": post,
        "posts_count": posts_count,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, template, context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """Creates a new post"""
    template = "posts/create_post.html"

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect("posts:profile", request.user)

    context = {
        "title": "Новый пост",
        "form": form,
        "is_edit": False,
    }

    return render(request, template, context)


def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """Edit a post"""
    template = "posts/create_post.html"

    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect("posts:post_detail", post_id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)

    context = {
        "title": f"Изменить: {post.text[:30]}",
        "form": form,
        "is_edit": True,
    }

    return render(request, template, context)


@login_required
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    """Add comment"""
    post = get_object_or_404(Post, id=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    """View posts of subscribed authors"""
    template = "posts/index.html"
    posts = Post.objects.filter(author__following__user=request.user)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Сообщения авторов, на которых вы подписаны",
        "page_obj": page_obj,
        "follow": True,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Follow the author"""
    author = get_object_or_404(User, username=username)
    if (
        not User.objects.filter(
            username=author,
            following__user=request.user,
        ).exists()
        and author != request.user
    ):
        Follow.objects.create(author=author, user=request.user)

    return redirect("posts:profile", username=author)


@login_required
def profile_unfollow(request, username):
    """Unfollow (dislike) the author"""
    author = get_object_or_404(User, username=username)

    Follow.objects.filter(author=author, user=request.user).delete()

    return redirect("posts:profile", username=author)
