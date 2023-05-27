from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from .models import Profile


User = get_user_model()


def create_profile(*, user: User, bio: str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)


def create_user(user_data) -> User:
    bio = user_data.pop("bio")
    user = User.objects.create_user(**user_data)
    profile = create_profile(user=user, bio=bio)
    return user

@transaction.atomic
def register_user(**user_data) -> User:
    user = create_user(user_data)
    return user
