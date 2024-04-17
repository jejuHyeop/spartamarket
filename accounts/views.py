from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import User
import json

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
        userpass = request.POST.get("regpass")
        email = request.POST.get("usermail")
        profile_pic = request.FILES.get("profile_pic")
        introduce = request.POST.get("introduce")
        User.objects.create_user(username=username, password=userpass, email=email, profile_pic=profile_pic, introduce=introduce)
        # 회원가입 성공 처리
        return redirect("accounts:login")
    return render(request, "accounts/signup.html")

def profile(request):
    return render(request, "accounts/profile.html")       

def seller(request, name):
    user = User.objects.get(username=name)
    context = {
        "userdata" : user,
    }
    return render(request, "products/seller.html", context)

def update(request):
    if request.method == "POST":
        user = request.user
        changePic, changeComment, changePass = request.FILES.get("changePic"), request.POST.get("changeComment"), request.POST.get("changePass")
        if changePic:
            user.profile_pic.delete()
            user.profile_pic = changePic
        if changeComment:
            user.introduce = changeComment
        if changePass:
            user.set_password(changePass)
            user.save()
            # password 변경 후 재로그인 안내
            return redirect("accounts:login")
        # 변경사항 저장
        user.save()
    return render(request, "accounts/profile.html")

def delete(request):
    if request.method == "POST":
        request.user.profile_pic.delete()
        request.user.delete()
        auth_logout(request)
        return redirect("accounts:index")

def nameDuplicate(request):
    username = request.POST.get("username")
    result = User.objects.filter(username=username).exists()
    return JsonResponse({"result": result})

def mailDuplicate(request):
    email = request.POST.get("usermail")
    result = User.objects.filter(email=email).exists()
    return JsonResponse({"result": result})

def checkpassword(request):
    print(request.POST)
    password = request.POST.get("password")
    result = check_password(password, request.user.password)
    return JsonResponse({"result": result})

def follow(request, name):
    user = request.user
    target = User.objects.get(username=name)
    if user != target:
        if target in user.following.all():
            user.following.remove(target)
        else:
            user.following.add(target)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
