from .models import Post, Comment, Yayinevi
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "yayin",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "name",
            "content",
        ]


class Form2(forms.ModelForm):
    class Meta:
        model = Yayinevi
        fields = [
            "user",
            "ad",
            "kisa_ad",
        ]




class BookModelForm(BSModalModelForm):
    publication_date = forms.DateField(
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )

    class Meta:
        model = Post
        exclude = ['timestamp']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
