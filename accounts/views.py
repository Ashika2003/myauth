from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile

def home(request):
    return render(request,'accounts/index.html')

def login_user(request):
    if request.method=='POST':
        forms=AuthenticationForm(data=request.POST)
        if forms.is_valid():
            username=forms.cleaned_data['username']
            password=forms.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard/')
        return HttpResponseRedirect('/login/')
        
    forms=AuthenticationForm()
    return render(request,'accounts/login.html',{'forms':forms})

def signup(request):
    if request.method=='POST':
        forms=UserCreationForm(request.POST)
        if forms.is_valid:
            forms.save()
            return HttpResponseRedirect('/login/')
    forms=UserCreationForm()
    return render(request,'accounts/signup.html',{'forms':forms})


@login_required
def manage_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/forms.html', {'form': form,'heading':'PROFILE'})

@login_required
def dashboard(request):


    return render(request,'accounts/dashboard.html',{'user':request.user})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')