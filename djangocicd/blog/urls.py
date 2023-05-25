from django.urls import path

from djangocicd.blog.apis.products import ProductAPI 


urlpatterns = [
    path("products/", ProductAPI.as_view(), name="products"),
]

