import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import NewPost

from .models import User,Post


def index(request):
    getPosts = Post.objects.all().order_by('-posted_at')
    return render(request, "network/index.html",
                  {
                      "form":NewPost(),
                      "posts":getPosts,
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

    return render(request, 'your_template.html', {'form': form})


@login_required
def handleLikes(request, postId):
    try:
        post = Post.objects.get(id=postId)
        user = request.user

        if not user.is_authenticated:
            # User is not authenticated, return an error response
            return redirect('login')
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
def editPost(request, editId):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=editId, user=request.user)
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
