from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.cache import cache

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


def profile_information_update_task():
    """
    Update profile information of users based on cached data

    This function is going to be called as a celery task that
    retrieves profile information from the cache and updates the
    corresponding Profile objects in the database. The cache keys
    are expected to follow the pattern "profile_<user_email>".

    Note: This function assumes the existence of a Profile model with attributes posts_number, subscribers_number,
    and subscriptions_number.

    Usage:
    This function is intended to be used as a Celery task and called asynchronously from other parts of the application.
    """
    user_profiles = cache.keys("profile_*")

    for profile_key in user_profiles:
        """
        profile_key: profile_<user_email>@gmail.com
        """
        email = profile_key.replace("profile_", "")
        data = cache.get(profile_key)

        try:
            profile = Profile.objects.get(user__email=email)

            profile.posts_number = data.get("posts_number") 
            profile.subscribers_number = data.get("subscribers_number") 
            profile.subscriptions_number = data.get("subscriptions_number") 

            profile.save()
        except Exception as e:
            print(e)
