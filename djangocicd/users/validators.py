import re
from django.utils.text import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers



User = get_user_model()


def validate_email(email):
    user_exists = User.objects.filter(email=email).exists()
    
    if user_exists:
        raise serializers.ValidationError(f"given email {email} is already taken")

def digits_validator(password):
    regex = re.compile(r"\d")
    if regex.search(password) is None:
        raise serializers.ValidationError(
            _("password must contain digits"),
            code="password_must_contain_digits",
        )

def letters_validator(password):
    regex = re.compile(r"[a-zA-Z]")
    if regex.search(password) is None:
        raise serializers.ValidationError(
            _("Password must contain letters"),
            code="password_must_contain_letters",
        )

def special_chars_validator(password):
    regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    if regex.search(password) is None:
        raise serializers.ValidationError(
            "Password must contain special characters",
            code="password_must_contain_special_chars"
        )
