from django.urls import path, include

urlpatterns = [
    path('blog/', include(('djangocicd.blog.urls', 'blog'), namespace="blog")),
    path('users/', include(('djangocicd.users.urls', 'users'), namespace="users")),
    path('auth/', include(('djangocicd.authentication.urls', 'authentication'), namespace="authentication"))
]

