from django.urls import path

from .apis.posts import post_api, post_detail_api
from .apis.subscriptions import subscriber_api, subscriber_detail_api

urlpatterns = [
    path("subscribe/", subscriber_api, name="subscribe"),
    path("subscribe/<str:email>/", subscriber_detail_api, name="subscribe_detail"),
    path("posts/", post_api, name="posts"),
    path("posts/<slug:slug>/", post_detail_api, name="post_detail"),
]

