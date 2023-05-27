from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()


def get_user_profile(user: User) -> Profile:
    return Profile.objects.get(user=user)

