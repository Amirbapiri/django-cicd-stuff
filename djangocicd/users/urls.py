from django.urls import path

from djangocicd.users.apis import RegisterationAPI 

urlpatterns = [
    path("register/", RegisterationAPI.as_view(), name="registeration"),
]
