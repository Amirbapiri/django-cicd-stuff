import pytest

from djangocicd.blog.selectors.posts import get_subscribers, get_all_posts


@pytest.mark.django_db
def test_get_all_posts(user2, user1, subscription1, profile1, post1):
    posts = get_all_posts(user=user1)
    assert posts.first() == post1


@pytest.mark.django_db
def test_get_subscribers(user2, user1, subscription1, profile1, post1):
    subscribers = get_subscribers(user=user1)
    assert subscribers.count() == 0

