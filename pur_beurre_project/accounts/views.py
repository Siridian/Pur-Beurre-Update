from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from accounts.admin import UserCreationForm


def signup(request):
    #Displays a page containing the signup form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data.get('email')
            form.save()
            username = form.cleaned_data.get('email')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
            
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    #Displays an account management page to a connected user
    context = {"user": request.user}
    return render(request, 'accounts/dashboard.html', context)