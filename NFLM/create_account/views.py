from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from login.models import UserProfile
# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == 'abcdef':
                user = form.save()
                user_profile = UserProfile.objects.create(user=user, user_type='organizer')
                user.save()
            else:
                user = form.save()
                user_profile = UserProfile.objects.create(user=user, user_type='user')
                form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/create_account.html', {
        'form':form,
    })
