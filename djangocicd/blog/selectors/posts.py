from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from djangocicd.blog.filters import PostFilter

from djangocicd.blog.models import Post, Subscription


User = get_user_model()


def get_all_posts(*, filters=None, user: User, self_include: bool = True) -> QuerySet[Post]:
    filters = filters or ()
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list("target"))
    if self_include:
        subscriptions.append(user.id)

    if subscriptions:
        qs = Post.objects.filter(author__in=subscriptions)
        return PostFilter(filters, qs).qs
    return Post.objects.none()


def get_post(*, slug: str, user: User, self_include: bool = True) -> Post:
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscriptions.append(user.id)
    return Post.objects.get(slug=slug, author__in=subscriptions)


def get_subscribers(*, user: User) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)

