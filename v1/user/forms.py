from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


# class MyUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = '__all__'

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#         return user