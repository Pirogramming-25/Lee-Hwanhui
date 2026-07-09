from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from .models import Profile, Post
from .forms import PostForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth.login(request, user)
            return redirect('feed:post_list')
    else:
        form = UserCreationForm()
    return render(request, 'feed/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('feed:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'feed/login.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('feed:login')


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed:post_list')
    else:
        form = PostForm()
    return render(request, 'feed/post_form.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'feed/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('feed:post_list')
    return render(request, 'feed/post_delete.html', {'post': post})


from django.db.models import Q
from django.contrib.auth.models import User

from .models import Like, Comment, Story, StoryImage, Follow
from .forms import CommentForm


@login_required
def post_list(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(
        Q(author=request.user) | Q(author_id__in=following_ids)
    ).order_by('-created_at')

    posts = list(posts)
    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)
    )
    for post in posts:
        post.user_has_liked = post.id in liked_post_ids
        post.like_count = post.likes.count()
        post.comment_form = CommentForm()

    story_authors = User.objects.filter(
        Q(id=request.user.id) | Q(id__in=following_ids), stories__isnull=False
    ).distinct()

    return render(request, 'feed/post_list.html', {
        'posts': posts,
        'story_authors': story_authors,
    })


@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('feed:post_list')


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('feed:post_list')


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('feed:post_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'feed/comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.delete()
    return redirect('feed:post_list')


@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            story, created = Story.objects.get_or_create(author=request.user)
            existing_count = story.images.count()
            for i, image in enumerate(images):
                StoryImage.objects.create(story=story, image=image, order=existing_count + i)
            return redirect('feed:post_list')
    return render(request, 'feed/story_form.html')


@login_required
def story_view(request, pk):
    story = get_object_or_404(Story, pk=pk)
    images = list(story.images.all())
    index = int(request.GET.get('photo', 0))
    index = max(0, min(index, len(images) - 1)) if images else 0

    current_image = images[index] if images else None
    has_prev_photo = index > 0
    has_next_photo = index < len(images) - 1

    return render(request, 'feed/story_view.html', {
        'story': story,
        'current_image': current_image,
        'index': index,
        'has_prev_photo': has_prev_photo,
        'has_next_photo': has_next_photo,
    })


@login_required
def user_search(request):
    query = request.GET.get('q', '')
    results = list(User.objects.filter(username__icontains=query)) if query else []
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    for u in results:
        u.is_following = u.id in following_ids
    return render(request, 'feed/user_search.html', {'results': results, 'query': query})


@login_required
def post_search(request):
    query = request.GET.get('q', '')
    results = list(Post.objects.filter(content__icontains=query)) if query else []
    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=results).values_list('post_id', flat=True)
    )
    for post in results:
        post.user_has_liked = post.id in liked_post_ids
        post.like_count = post.likes.count()
        post.comment_form = CommentForm()
    return render(request, 'feed/post_search.html', {'results': results, 'query': query})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    is_own_profile = (request.user == profile_user)
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'feed/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'post_count': posts.count(),
        'follower_count': profile_user.followers.count(),
        'following_count': profile_user.following.count(),
    })


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
        if not created:
            follow.delete()
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('feed:profile_view', username=username)