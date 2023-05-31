import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_empty_post_api(api_client):
    endpoint = reverse("api:blog:posts")

    response = api_client.get(endpoint, content_type="application/json")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data.get("results") == list()
    assert data.get("limit") == 10

