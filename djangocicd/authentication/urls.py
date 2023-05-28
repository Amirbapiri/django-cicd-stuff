from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify


urlpatterns = [
    path("jwt/", include(([
        path("login/", token_obtain_pair, name="login"),
        path("refresh/", token_refresh, name="refresh"),
        path("verify/", token_verify, name="verify"),
    ], "jwt"), namespace="jwt"), name="jwt"),
]
