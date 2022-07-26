from cmath import log
import re
from django.shortcuts import render
from app.forms import *
from django.core.mail import send_mail
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from app.models import *

def home(request):
    if request.session.get('username'):
        d={'username':request.session.get('username')}
        return render(request,'home.html',d)
    return render(request,'home.html')


def registration(request):
    UF=UserForm()
    PF=ProfileForm()
    d={'UF':UF,'PF':PF}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid() and PD.is_valid():
            user1=UD.save(commit=False)
            user1.set_password(UD.cleaned_data['password'])
            user1.save()
            profile=PD.save(commit=False)
            profile.user=user1
            profile.save()
            send_mail('registration',
            'Registration is successfull',
            'harshadvali1431@gmail.com',
            [user1.email],
            fail_silently=False)
            return HttpResponse('registration is successfull')

    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))

        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_details(request):
    username=request.session['username']
    ud=User.objects.get(username=username)
    pd=Profile.objects.get(user=ud)
    print(ud)
    d={'ud':ud,'pd':pd}
    return render(request,'display_details.html',d)
@login_required
def change_password(request):
    if request.method=='POST':
        nw=request.POST['nw']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(nw)
        UO.save()
        return HttpResponse('changed successfully')
    return render(request,'change_password.html')



