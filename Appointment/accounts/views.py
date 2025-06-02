from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
import logging

logger = logging.getLogger('accounts')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        logger.info(f"User {user.username} deleted their account.")
        return redirect('home')
    return render(request, 'hello/delete_account_confirm.html')

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