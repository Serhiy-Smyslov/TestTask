from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserPost


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['content'].label = 'Content'
        self.fields['image'].label = 'Image'

    class Meta:
        model = UserPost
        fields = ('title', 'content', 'image')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Not correct login!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(required=False)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm password'
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.fields['name'].label = 'Name'
        self.fields['email'].label = 'Email address'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():  # Not repeat email
            raise forms.ValidationError('This email address is already taken!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken!')
        return username

    def clean(self):
        """Equal two password fields on correct."""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords is not the same!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'name', 'password', 'confirm_password'
        )
