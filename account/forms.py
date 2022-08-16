from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'bio', 'avatar', 'github',
                  'linkedin', 'country']

        slug_field = 'username'


class CustomUserCreationForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
