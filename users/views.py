from django.shortcuts import render , redirect
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has created! you can log in now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def logout(request):
    logout_auth(request)
    messages.success(request, 'You have successful logout')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance= request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES ,instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
        return redirect('profile')

    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)

    context ={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)