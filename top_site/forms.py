'''
    INTELL The Craft of Intelligence
        https://github.com/dylan-wright/cs499-intell
        https://intellproject.com

        /top_site/forms.py
            Django forms
                UserCreationForm
'''

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

'''
UserCreationForm
    form adds first name to user registration form provided
    from django.contrib.auth.forms.UserCreationForm
'''
class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username","first_name","password1","password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user
