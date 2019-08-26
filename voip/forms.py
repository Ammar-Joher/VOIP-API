from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, CharField, TextInput, PasswordInput

from .models import voip_user


class voip_user_form(ModelForm):
    name = CharField()
    location = CharField()
    phone_number = CharField()
    notes = CharField()

    class Meta:
        model = voip_user
        exclude = {'received_count'}

class LoginForm(AuthenticationForm):
    """
    This function overrides the backend allows authentication of inactive users
    Django's detault behavior is to reject login from users who have is_active
    flag set to false. This method overrides it so inactive users can be logged
    in.
    """
    def confirm_login_allowed(self, user):
        pass

    username = CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))