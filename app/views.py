from django.http import HttpResponse
from django.shortcuts import render
from app.forms import *
# Create your views here.
from django.core.mail import send_mail
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
            'harshadvali1432@gmail.com',
            [user1.email],
            fail_silently=False)
            return HttpResponse('registration is successfull')
    return render(request,'registration.html',d)






