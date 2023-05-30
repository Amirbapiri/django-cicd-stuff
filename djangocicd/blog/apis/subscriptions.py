from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, status
from drf_spectacular.utils import extend_schema

from djangocicd.api.mixins import ApiAuthMixin
from djangocicd.api.pagination import LimitOffsetPagination, get_paginated_response
from djangocicd.blog.models import Subscription
from djangocicd.blog.selectors.posts import get_subscribers
from djangocicd.blog.services.posts import unsubscribe, subscribe 


class SubscribeDetailAPI(ApiAuthMixin, APIView):
    def delete(self, request, email, *args, **kwargs):
        try:
            unsubscribe(user=request.user, email=email)
        except Exception as e:
            return Response({
                "detail": f"Database Error: {e}"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


subscriber_detail_api = SubscribeDetailAPI.as_view()


class SubscribeAPI(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubcribeSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)

    class OutputSubscribeSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subscription
            fields = ("subscriber", "target")
    
    @extend_schema(responses=OutputSubscribeSerializer)
    def get(self, request):
        subscribers = get_subscribers(user=request.user)
        return get_paginated_response(
            request=request,
            pagination_class=self.Pagination,
            queryset=subscribers,
            serializer_class=self.OutputSubscribeSerializer,
            view=self,
        )

    @extend_schema(request=InputSubcribeSerializer, responses=OutputSubscribeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputSubcribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            subscribe_response = subscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as e:
            return Response(
                {"detail": f"Error in subscribing - {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        output_serializer = self.OutputSubscribeSerializer(subscribe_response)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


subscriber_api = SubscribeAPI.as_view()
