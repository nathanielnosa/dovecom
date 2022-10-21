from django.shortcuts import render,redirect
# Create your views here.
from .forms import Userprofile ,Updateprofile

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login ,logout, authenticate

from stores.models import Order


def register(request):
    if request.user.is_authenticated:
        redirect('dashboard')

    show = Userprofile()

    if request.method == 'POST':
        form = Userprofile(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(username = username):
                messages.warning(request, 'Username already exist')
                return redirect('register')

            if User.objects.filter(email = email):
                messages.warning(request, 'Email already exist')
                return redirect('register')

            if password != password2:
                messages.warning(request, 'Password not match')
                return redirect('register')

            user = User.objects.create_user(username,email,password)
            form = form.save(commit=False)
            form.user = user

            form.save()
            messages.success(request, 'Registration Successful')
            if "next" in request.GET:
                next_url=request.GET.get("next")
                return redirect(next_url)
            else:
                return redirect('loginuser')
    context = {
        'form':show
    }
    return render(request, 'users/register.html',context)


def loginuser(request):
    if request.user.is_authenticated:
        redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password= request.POST.get('pwd')

        user = authenticate(username = username , password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfully')
            if "next" in request.GET:
                next_url=request.GET.get("next")
                return redirect(next_url)
            else:
                return redirect('loginuser')
        else:
            messages.warning(request, 'Invalid Username/Password')
    return render(request, 'users/login.html')


def logoutuser(request):
    logout(request)
    messages.success(request, 'User logged out successfully')
    return redirect('loginuser')


def dashboard(request):
    profile = request.user.profile
    orders = Order.objects.filter(cart__profile = profile)
    context ={
        'profile':profile,
        'orders':orders
    }
    return render(request, 'users/dashboard.html',context)

def updateprofile(request):
    if request.user.profile and request.user:
        user = request.user.profile
        form = Updateprofile(instance=user)
        if request.method == 'POST':
            form = Updateprofile(request.POST,request.FILES, instance = user)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    context = {
        'form':form
    }
    return render(request, 'users/updateprofile.html',context)



