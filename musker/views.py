from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, ("Your Meep Has Been Posted!!"))
                return redirect ('home')

        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "meeps" : meeps, "form" : form })
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', { "meeps" : meeps })




def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")

        #Post Form Logic
        if request.method == 'POST':
            # Get Current User
            current_user_profile = request.user.profile
            # Get Form Data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "meeps": meeps})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page"))
        return redirect('home')
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,  user)
            messages.success(request, ("You Have Been Logged In!  Get MEEPING!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in.  Please try again."))
            return redirect('login')            
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out.  Sorry to Meep you go..."))
    return redirect('home')

def register_user(request):
    form=SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            #Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have successfully registered!!! WELCOME!!"))
            return redirect ('home')

    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        #Get Forms
        user_form = SignUpForm(request.POST or None,request.FILES or None , instance = current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None , instance = profile_user)
        if user_form.is_valid() and profile_form.is_valid :
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Your Profile Has Been Updated!!"))
            return redirect ('home')               
        return render(request, "update_user.html", {'user_form':user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect ('home')             
    
