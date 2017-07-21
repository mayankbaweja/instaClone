# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from datetime import datetime
from models import User, SessionToken
from django.contrib.auth.hashers import make_password, check_password
def signup_view(request):
    if request.method == "POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            user=User(full_name=full_name,password=make_password(password),email=email,username=username)
            user.save()
            return render(request,"login.html")
    else:
        form=SignUpForm
    return render(request,"index.html",{"form":form})


def login_view(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    print 'User is invalid'
    else:
        form=LoginForm(request)
    return render(request, "login.html", {"form":form})

def feed_view(request):
    render(request, 'feed.html')

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
           return session.user
    else:
        return None

