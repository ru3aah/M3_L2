from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.template.defaultfilters import default

from .models import Post, Category, Comment
from .validators import validate_spam


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=False,
                        widget=forms.TextInput(
                               attrs={'placeholder': 'Enter your Name',
                                      'class':'form-control'
                                      }
                        ), validators=[MinLengthValidator(2,
                            'Name must be greater than 2 characters'),
                                    MaxLengthValidator(100,
                            'Name must be less than 100 characters'),
                                       validate_spam
                                       ]
    )
    email = forms.EmailField(label='E-mail',
                            widget=forms.EmailInput(
                                 attrs={'placeholder': 'your E-mail',
                                        'class':'form-control'
                                        }
                            ),
                    error_messages={'invalid': 'Enter a valid email address.',
                                    'required': 'This field is required.'
                                    }
    )
    subject = forms.CharField(max_length=100,
                            widget=forms.TextInput(
                                  attrs={'placeholder': 'Enter Subject',
                                         'class':'form-control'}
                            )
    )
    message = forms.CharField(widget=forms.Textarea(attrs={
                                        'class':'form-control',
                                        'placeholder': 'Enter your Message'}
                            )
    )


    def clean_message(self):
        message = self.cleaned_data['message']
        if 'spam' in message.lower():
            raise forms.ValidationError('Message cannot contain spam')
        return message


    def clean_name(self):
        name = self.cleaned_data['name']
        if 'spam' in name.lower():
            raise forms.ValidationError('Name cannot contain spam')
        return name

class PostForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_spam])
    content = forms.CharField(validators=[validate_spam],
                              widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
            'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'title': {
                'required': 'Title is required',
                'max_length': 'Title cannot be greater than 200 characters'
            },
            'content': {'required': 'Content is required'},
        }
        labels = {
            'title': 'Title:',
            'image': 'Logo:',
            'content': 'Content:',
            'category': 'Category:',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Your comment here'
            }),
        }
        labels = {
            'content': 'Comment:',
        }
        error_messages = {
            'content': {
                'required': 'Please enter your comment.',
            }
        }