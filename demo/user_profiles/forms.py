from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from user_profiles.models import UserProfile


class AuthenticationForm(forms.Form):
    username = forms.EmailField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'id': "id_user_password"}))

    class Meta:
        model = UserProfile
        exclude = ('user', 'registration_type', 'is_email_verified')

    def clean_email(self):
        user = None
        cleaned_data = super(UserRegistrationForm, self).clean()
        email = cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            pass
        if user:
            raise forms.ValidationError("This email ID is already registered with us.")
        return email


class UserProfileCompleteForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'registration_type', 'is_email_verified')


