from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True, null=True)
    email = models.EmailField(unique=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})