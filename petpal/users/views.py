from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from .forms import RegisterForm, LoginForm

def home(request):
    return render(request, 'home.html')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            messages.success(request, "Registration successful!")
            return redirect('users:login')

        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Redirect **always to home**, navbar will change automatically
                return redirect('home')

            messages.error(request, "Invalid username or password")
            return render(request, 'login.html', {'form': form})

        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect('users:login')
