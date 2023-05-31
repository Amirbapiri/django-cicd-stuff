import json

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from djangocicd.blog.models import Post


User = get_user_model()


@pytest.mark.django_db
def test_unauthenticated_create_post_api():
    client = Client()
    endpoint = reverse("api:blog:posts")

    response = client.post(endpoint, content_type="application/json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_post_api(api_client):
    endpoint = reverse("api:blog:posts")

    response = api_client.get(endpoint, content_type="application/json")

    assert response.status_code == 200


@pytest.mark.django_db
def test_login(user1):
    user = User.objects.create_user(email="djangounchained@gmail.com", password="testpass")
    client = APIClient()
    endpoint = reverse("api:authentication:jwt:login")

    body = {"email": user.email, "password": "testpass"}
    response = client.post(endpoint, json.dumps(body), content_type="application/json")
    auth = json.loads(response.content)
    access = auth.get("access")
    refresh = auth.get("refresh")

    assert access != None
    assert refresh != None


