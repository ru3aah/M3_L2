from django import forms
from django.utils.deconstruct import deconstructible


def validate_spam(value):
    if 'spam' in value.lower():
        raise forms.ValidationError('spam is prohibited')
    return value

@deconstructible
class CommentMaxLengthValidator:
    def __init__(self, max_length = 300):
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            raise forms.ValidationError(f'Ensure this value has at most '
                                        f'{self.max_length} characters')