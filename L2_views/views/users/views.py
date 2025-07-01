from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import RegistrationForm
from .models import User


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login') #returns view URL by view name


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user  # Always return the current logged-in user


class AuthorDetailView(DetailView):
    model = get_user_model()
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('posts').annotate(
            post_count = Count('posts')
        )