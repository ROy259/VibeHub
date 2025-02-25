from django.shortcuts import render,redirect
from .models import Tweet
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.


# def base(request):
#     return render(request,"base.html")

def tweet_list(request):
    tweets=Tweet.objects.all()
    if request.GET.get('search'):
        tweets = Tweet.objects.filter(user__username__icontains=request.GET.get('search'))
        
    return render(request,"tweet_list.html",{"tweets":tweets})


@login_required
def create_tweet(request):
    if request.method=="POST":
        text=request.POST.get("text")
        photo = request.FILES.get("photo")
        Tweet.objects.create(text=text,photo=photo,user=request.user)

        return redirect("tweet_list")

    
    return render(request,"create_tweet.html")


@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    # tweet = Tweet.objects.get(id=tweet_id)

    if tweet.user == request.user:
        tweet.delete()

    return redirect("tweet_list")




@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.method == "POST":
        text = request.POST.get("text")
        photo = request.FILES.get("photo")

        tweet.text = text
        if photo:
            tweet.photo = photo
        tweet.save()

        return redirect("tweet_list")

    return render(request, "edit_tweet.html", {"tweet": tweet})


def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

         # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        
        # Check if passwords match
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("register")
        
        user=User.objects.create(username=username, email=email, password=make_password(password))
        login(request, user)
        

        messages.success(request, "Registration successful! Please log in.")
        return redirect("tweet_list")




    return render(request,"registration/register.html")

   