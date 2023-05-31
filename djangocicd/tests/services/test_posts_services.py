import pytest

from djangocicd.blog.services.posts import create_post


@pytest.mark.django_db
def test_create_post(user2, user1, subscription1, profile1, post1):
    post = create_post(user=user1, title="test title", content="test content")

    assert post.author == user1
    assert post.title == "test title"
    assert post.content == "test content"

