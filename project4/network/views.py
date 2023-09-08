from datetime import datetime
import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpResponseNotFound

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post,Like


def index(request):
    posts = Post.objects.order_by('-timestamp')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts": page_obj
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
@csrf_exempt    
@login_required   
def newPost(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST request required"}, status=400)
    data = json.loads(request.body)
    date = datetime.today().strftime('%Y-%m-%d')
    # get text from form
    text = data.get("text")
    post = Post(user = request.user, text = text, timestamp=date)
    post.save()
    return JsonResponse({"success":"New post created successfully!"}, status=201)

@login_required
def get_following(request):
        loggedInUser = request.user
        following_users = loggedInUser.following.all()
        posts = Post.objects.filter(user__in=following_users)
        posts = posts.order_by("-timestamp")
        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html",{"posts":page_obj})

def get_posts(request, post_type):
    loggedInUser = request.user
    try:
        if post_type == "following":
            following_users = loggedInUser.following.all()
            posts = Post.objects.filter(user__in=following_users)
        else:
            target_user = User.objects.get(username=post_type)
            posts = Post.objects.filter(user=target_user)
    except User.DoesNotExist:
        print("user does not exist")
        posts = Post.objects.all()

    posts = posts.order_by("-timestamp")
    return JsonResponse([post.serialize() for post in posts], safe=False)



@csrf_exempt
@login_required
def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        currentUser = request.user
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        # Check if the current user has liked the post
        liked = Like.objects.filter(user=currentUser, post=post).exists()

        # Calculate the like count for the specific post
        like_count = post.liked_by.count()

        serialized_post = {
            "id": post.id,
            "user": post.user.serialize(),
            "text": post.text,
            "timestamp": post.timestamp,
            "likes": post.likes,
            "liked": liked,  # Include the liked status in the response
            "like_count": like_count,  # Include the like count in the response
        }

        return JsonResponse(serialized_post)

    elif request.method == "PUT":
        data = json.loads(request.body)
        try:
            like = Like.objects.get(user=currentUser, post=post)
            like.delete()
        except Like.DoesNotExist:
            Like.objects.create(user=currentUser, post=post)

        # Calculate the new like count for the post
        post.likes = post.liked_by.count()
        post.save()

        return HttpResponse(status=204)  # Return a successful response for PUT requests

    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)


@csrf_exempt
def get_user_info(request, username):
    TargetUser = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=TargetUser).order_by('-timestamp')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/user.html", {
        "targetuser": TargetUser,
        "followers" : TargetUser.followers.all,
        "followersnum": TargetUser.followers.count(),
        "following": TargetUser.following.count(),
        "posts": page_obj
    })

@csrf_exempt
@login_required
def getUser(request, user_id):
    try :
        TargetUser = User.objects.get(pk=int(user_id))
        currentUser = request.user
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"},status=404)
    if request.method == "GET":
        return JsonResponse( TargetUser.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("followers") == True:
            TargetUser.followers.add(currentUser)
            TargetUser.save()
            return HttpResponse(status=204)
        elif data.get("followers") == False:
            TargetUser.followers.remove(currentUser)
            TargetUser.save()
            return HttpResponse(status=204)
    else:
        return JsonResponse({"error":"GET or PUT request required"},status=400)
@login_required
@csrf_exempt
def editPost(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        post.text = data
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)
@login_required
def liked_posts(request):
    if request.method == "GET":
        user = request.user
        liked_posts = user.liked_posts.all()  # Get all the liked posts for the user
        liked_post_ids = [post.id for post in liked_posts]  # Extract the IDs of liked posts
        return JsonResponse({"liked_post_ids": liked_post_ids})
