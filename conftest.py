import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from djangocicd.tests.factories import (
    UserFactory,
    ProfileFactory,
    SubscriptionFactory,
    PostFactory,
)


User = get_user_model()


@pytest.fixture
def api_client():
    user = User.objects.create(email="testuser@gmail.com", password="testpasswor$")
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    
    return client


@pytest.fixture
def user1():
    return UserFactory()


@pytest.fixture
def user2():
    return UserFactory()


@pytest.fixture
def profile1(user1):
    return ProfileFactory(user=user1)


@pytest.fixture
def post1(user1):
    return PostFactory(author=user1)


@pytest.fixture
def subscription1(user1, user2):
    return SubscriptionFactory(target=user1, subscriber=user2)

