from cmath import log
import re
from django.shortcuts import render
from app.forms import *
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    if request.session.get('username'):
        d={'username':request.session.get('username')}
        return render(request,'home.html',d)
    return render(request,'home.html')


def registration(request):
    UF=UserForm()
    PF=ProfileForm()
    d={'UF':UF,'PF':PF}
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        user=authenticate(username=un,password=pw)
        if user and user.is_active:
            login(request,user)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))

        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))








