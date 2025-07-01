from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'avatar', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'id': 'username-field'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'id': 'email-field'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            })
        }

        labels = {
            'username': 'Nickname:',
            'email': 'E-mail:',
            'avatar': 'Avatar:',
            'password1': 'Password:',
            'password2': 'Confirm Password:',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help text from all fields
        for field_name in self.fields:
            self.fields[field_name].help_text = None

        # Customize username field
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'username-field'
                        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'email-field'
        })

        # Customize password1 field
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password1-field'
                        })

        # Customize password2 field
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'password2-field'
                        })

        # Customize avatar field
        self.fields['avatar'].widget = forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*',
        })


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
            'Provided e-mail already exists. Please use another one or login.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))