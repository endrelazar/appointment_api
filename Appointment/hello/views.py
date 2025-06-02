from django.utils.timezone import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from hello.forms import LogMessageForm
from accounts.forms import CustomUserCreationForm
from hello.models import LogMessage
from django.views.generic import ListView
import logging

logger = logging.getLogger('accounts')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"User {user.username} registered and logged in successfully.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hello/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User {user.username} logged in successfully.")
            return redirect('home')
        else:
            logger.warning("Login attempt failed: Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'hello/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} logged out successfully.")
    logout(request)
    return redirect('home')

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")


def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})


