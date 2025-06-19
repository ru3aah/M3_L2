from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=False,
                        widget=forms.TextInput(
                               attrs={'placeholder': 'Enter your Name',
                                      'class':'form-control'}
                        )
    )
    email = forms.EmailField(label='E-mail',
                            widget=forms.EmailInput(
                                 attrs={'placeholder': 'your E-mail',
                                        'class':'form-control'}
                            )
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
