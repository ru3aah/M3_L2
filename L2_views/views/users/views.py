from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('blog:post_list')

    return render(request, 'users/login.html')


@login_required
def log_out(request):
    logout(request)
    return render(request, 'users/login.html')
