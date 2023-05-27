from django.urls import path

from .apis import ProfileAPI, RegisterationAPI 

urlpatterns = [
    path("register/", RegisterationAPI.as_view(), name="registeration"),
    path("profile/", ProfileAPI.as_view(), name="profile"),
]
