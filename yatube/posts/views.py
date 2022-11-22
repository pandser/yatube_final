from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Group, Follow, Post, User
from .forms import PostForm, CommentForm
from .utils import paginator


def index(request):
    posts = Post.objects.select_related('author')
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginator(request, posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('author').filter(author=author)
    page_obj = paginator(request, posts)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=get_object_or_404(User, username=username),
    ).exists()
    context = {
        'author': author,
        'following': following,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    posts = Post.objects.select_related('author')
    post = get_object_or_404(posts, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required()
def post_create(request):
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None,
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', request.user)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required()
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(
        request,
        'posts/create_post.html',
        {
            'form': form,
            'is_edit': True,
        }
    )


@login_required()
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required()
def follow_index(request):
    posts = Post.objects.select_related('author').filter(
        author__following__user=request.user
    )
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required()
def profile_follow(request, username):
    if request.user.username != username:
        if not Follow.objects.filter(
            user=request.user,
            author=get_object_or_404(User, username=username),
        ).exists():
            Follow(
                user=request.user,
                author=get_object_or_404(User, username=username),
            ).save()
    return redirect('posts:profile', username=username)


@login_required()
def profile_unfollow(request, username):
    if Follow.objects.filter(
        user=request.user,
        author=get_object_or_404(User, username=username),
    ).exists():
        Follow.objects.filter(
            user=request.user,
            author=get_object_or_404(User, username=username),
        ).delete()
    return redirect('posts:profile', username=username)
