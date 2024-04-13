from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from .models import User

# Create your views here.
def index(request):
    return render(request, "accounts/index.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        userpass = request.POST.get("password")
        user = authenticate(request, username=username, password=userpass)
        if user is not None:
            auth_login(request, user)
            return redirect("accounts:index")
        else:
            pass # 로그인 실패 처리
    return render(request, "accounts/login.html")

def logout(request):
    auth_logout(request)
    return redirect("accounts:index")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        userpass = request.POST.get("password")
        email = request.POST.get("email")
        profile_pic = request.FILES.get("profile_pic")
        print(profile_pic)
        introduce = request.POST.get("introduce")
        User.objects.create_user(username=username, password=userpass, email=email, profile_pic=profile_pic, introduce=introduce)
        # 회원가입 성공 처리
        return redirect("accounts:login")
    return render(request, "accounts/signup.html")

def profile(request):
    return render(request, "accounts/profile.html")

def update(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.profile_pic = request.FILES.get("profile_pic")
        user.introduce = request.POST.get("introduce")
        user.save()
        return redirect("accounts:profile")
    return render(request, "accounts/update.html")

def delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("accounts:index")
    return render(request, "accounts/delete.html")