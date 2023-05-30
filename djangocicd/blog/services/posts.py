from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.cache import cache
from django.db.models import QuerySet
from django.utils.text import slugify
from rest_framework.generics import get_object_or_404
from djangocicd.blog.filters import PostFilter

from djangocicd.blog.models import Post, Subscription


User = get_user_model()


def count_user_posts(*, user: User) -> int:
    return Post.objects.filter(author=user).count()


def count_user_subscribers(*, user: User) -> int:
    return Subscription.objects.filter(target=user).count()


def count_user_subscriptions(*, user: User) -> int:
    return Subscription.objects.filter(subscriber=user).count()


def cache_profile(user: User):
    profile = {
            "posts_number": count_user_posts(user=user),
            "subscribers_number": count_user_subscribers(user=user),
            "subscriptions_number": count_user_subscriptions(user=user),
            }
    cache.set(f"profile_{user}", profile, timeout=None)


def subscribe(*, user: User, email: str) -> QuerySet[Subscription]:
    target = get_object_or_404(User, email=email)
    subscription = Subscription(target=target, subscriber=user)
    subscription.full_clean()
    subscription.save()
    cache_profile(user=user)
    return subscription


def unsubscribe(*, user: User, email: str) -> None:
    target = get_object_or_404(User, email=email)
    Subscription.objects.get(subscriber=user, target=target).delete()


@transaction.atomic
def create_post(*, user: User, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        slug=slugify(title),
        author=user,
        title=title,
        content=content,
    )
    cache_profile(user=user)
    return post

