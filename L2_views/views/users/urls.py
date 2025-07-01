from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from . import views
from .views import RegisterView, ProfileView
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        form_class = LoginForm
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/<int:pk>/', ProfileView.as_view(), name='profile')
]