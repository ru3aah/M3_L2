from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=False,
                        widget=forms.TextInput(
                               attrs={'placeholder': 'Enter your Name',
                                      'class':'form-control'
                                      }
                        ), validators=[MinLengthValidator(2,
                            'Name must be greater than 2 characters'),
                                    MaxLengthValidator(100,
                            'Name must be less than 100 characters')
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
