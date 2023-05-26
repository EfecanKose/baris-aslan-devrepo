from django import forms
from .models import Support, AdminMessage


class Support1(forms.ModelForm):

    class Meta:
        model = Support
        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]


class Admin(forms.ModelForm):

    class Meta:
        model = AdminMessage
        fields = [
            "message",
        ]