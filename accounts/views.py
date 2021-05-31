from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from .forms import CustomUserCreationForm


# Create your views here.
def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'{form.cleaned_data["email"]} registered successfully!')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, mark_safe(f'You are already logged in as <b>{request.user.username}</b>. To switch user'
                                         f' <a href="#" data-toggle="modal" data-target="#logoutModal"></i>'
                                         f'log out here.</a>'))
        return redirect('website:index')

    username = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'User {user.username} logged in successfully!')
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('website:index')
        else:
            messages.warning(request, 'Could not authenticate, check credentials.')

    return render(request, 'accounts/login.html', context={"username": username})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('accounts:login')
