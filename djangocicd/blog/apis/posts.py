from django.urls import reverse_lazy, reverse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, status
from drf_spectacular.utils import extend_schema

from djangocicd.api.mixins import ApiAuthMixin
from djangocicd.api.pagination import LimitOffsetPagination, get_paginated_response
from djangocicd.blog.models import Post
from djangocicd.blog.services.posts import create_post
from djangocicd.blog.selectors.posts import get_all_posts, get_post


class PostAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100, required=False)
        search = serializers.CharField(max_length=100, required=False)
        created_at__range = serializers.CharField(max_length=100, required=False)
        author__in = serializers.CharField(max_length=100, required=False)
        slug = serializers.CharField(max_length=100, required=False)
        content = serializers.CharField(max_length=100, required=False)

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        content = serializers.CharField()
    
    class PostOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Post
            fields = ("url", "title", "author")

        def get_author(self, post):
            return post.author.email

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse_lazy("api:blog:post_detail", kwargs={"slug": post.slug})
            # return request.build_absolute_uri(path)
            return path

    @extend_schema(parameters=[FilterSerializer], responses=PostOutputSerializer)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            posts = get_all_posts(
                filters=filters_serializer.validated_data, 
                user=request.user,
            )
        except Exception as e:
            return Response(
                {"detail": f"Error in getting posts - {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.PostOutputSerializer,
            queryset=posts,
            request=request,
            view=self,
        )

    @extend_schema(request=PostInputSerializer, responses=PostOutputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = create_post(
                user=request.user,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
            )
        except Exception as e:
            return Response({
                "detail": f"Error in creating new post - {e}",
            }, status=status.HTTP_400_BAD_REQUEST,)
        return Response(self.PostOutputSerializer(post, context={"request": request}).data, status=status.HTTP_201_CREATED)


post_api = PostAPI.as_view()


class PostDetailAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class PostDetailOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.email

    @extend_schema(responses=PostDetailOutputSerializer)
    def get(self, request, slug):
        print(request.user)
        try:
            post = get_post(slug=slug, user=request.user)
        except Exception as e:
            return Response({"detail": f"Error in getting post's detail - {e}"})
        post_serializer = self.PostDetailOutputSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)


post_detail_api = PostDetailAPI.as_view()

