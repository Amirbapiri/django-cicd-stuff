from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from djangocicd.api.pagination import LimitOffsetPagination
from djangocicd.blog.models import Product
from djangocicd.blog.selectors.products import get_products
from djangocicd.blog.services.products import create_product
from drf_spectacular.utils import extend_schema


class ProductAPI(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ("name", "created_at", "updated_at")

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        products = get_products()
        products_serializer = self.OutputSerializer(products, context={"request"}, many=True)
        return Response(products_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = create_product(name=serializer.validated_data.get("name"))
        except Exception as e:
            return Response(f"Database Error {e}", status=status.HTTP_400_BAD_REQUEST)

        product_serializer = self.OutputSerializer(product, context={"request": request})
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

