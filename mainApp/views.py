from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(Request):
    return render(Request,"index.html")


def loginPage(Request):
    if(Request.method=="POST"):
        username = Request.POST.get('username')
        pass1 = Request.POST.get('pass') 
        user = authenticate(Request,username=username,password=pass1)
        if user is not None:
            login(Request,user)
            if(user.is_superuser):
                return redirect('/admin')
            else:
                return redirect("/profile")
        else:
            messages.error(Request,"Invaild Username Or Password")
    return render(Request,"login.html")


def singupPage(Request):
    if(Request.method=="POST"):
        uname = Request.POST.get('username')
        email = Request.POST.get('email')
        pass1 = Request.POST.get('password1')
        pass2 = Request.POST.get('password2')
        if(pass1==pass2):
            my_user = User.objects.create_user(uname,email,pass1)
            if(my_user):
                my_user.set_password(pass1)
                my_user.save()
                return redirect('/login')
            else:
                messages.error(Request,"Username already Taken!")
                
        else:
            messages.error(Request,"Your password and confirm password not matched!")
             
    return render(Request,"signup.html")

@login_required(login_url='/login')
def profilePage(Request):
    return render(Request,"profile.html")


def logoutPage(Request):
    logout(Request)
    return redirect("/login")