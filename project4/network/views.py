from django.core.paginator import Paginator
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import NewPost

from .models import User,Post,Profile


def index(request):
    getPosts = Post.objects.all().order_by('-posted_at')
    paginator = Paginator(getPosts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",
                  {
                      "form":NewPost(),
                    #   "posts":getPosts,
                      "page_obj": page_obj,
                  })
    
@login_required    
def handlePost(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            # Save the post or perform any other actions
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')  # Redirect after successful form submission
    else:
        form = NewPost()

    return render(request, 'network/index.html', {'form': form})


@login_required
def handleLikes(request, postId):
    try:
        post = Post.objects.get(id=postId)
        user = request.user

        if not user.is_authenticated:
            # User is not authenticated, return an error response
            return JsonResponse({'error': 'User not authenticated', 'redirect_url': redirect('login')})
        else:
            
            if user in post.likes.all():
                # User has already liked the post, so unlike it
                post.likes.remove(user)
                liked = False
                
            else:
                # User hasn't liked the post, so like it
                post.likes.add(user)
                liked = True
                
                
            countLikes = post.count_likes()

            return JsonResponse({'message': 'Post liked/unliked', 'liked': liked, 'countLikes':countLikes})
            # return redirect('index')

    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'})

# edit post
def editPost(request, editPostId):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=editPostId, user=request.user)
            if request.user == post.user:
                    data = json.loads(request.body)
                    new_content = data.get('content', '')

                    post.content = new_content
                    post.save()

                    return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'You do not have permission to edit this post.'}, status=403)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def profile(request, userId):
    user = get_object_or_404(User, id=userId)
    print(user)
    profile_user = get_object_or_404(Profile, user=user)
    # print(profile_user.username)
    followers_count = profile_user.followers_count()
    following_count = profile_user.following_count()
    # posts = Post.objects.filter(user=user).order_by('-posted_at')
    getPosts = Post.objects.filter(user=user).order_by('-posted_at')
    paginator = Paginator(getPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if the current user is following the profile user
    is_following = False
    if request.user.is_authenticated:
        current_user = request.user
        is_following = current_user in profile_user.followers.all()

    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'page_obj': page_obj,
        'is_following': is_following,
    })

def handleFollows(request, profileId):
    profile_user = get_object_or_404(User, id=profileId)

    if request.user == profile_user:
        # Users can't follow/unfollow themselves, redirect or show an error message
        return JsonResponse({'error': 'You cannot follow/unfollow yourself.'}, status=400)

    current_user_profile = request.user.userProfile

    if profile_user in current_user_profile.followers.all():
        # User is currently following the profile user, so unfollow them.
        current_user_profile.followers.remove(profile_user)
    else:
        # User is not following the profile user, so follow them.
        current_user_profile.followers.add(profile_user)
    # com_t = comment_text.save(commit=False)
    #         com_t.comment_on = list_auction
    #         com_t.comment_by = request.user
    #         com_t.save()
    current_user_profile.save()

    # Redirect back to the profile page after the follow/unfollow action.
    return redirect('userprofile', userId=profileId)


@login_required
def followingPosts(request):
    # Get the list of users that the current user follows
    following_users = request.user.userProfile.followers.all()

    # Get posts by users that the current user follows
    following_posts = Post.objects.filter(user__in=following_users).order_by('-posted_at')

    # Paginate the posts (similar to your "All Posts" view)
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/following.html', {
        'page_obj': page_obj,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
