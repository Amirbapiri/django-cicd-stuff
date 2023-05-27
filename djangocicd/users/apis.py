from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, status
from drf_spectacular.utils import extend_schema

from djangocicd.users.services.users import register_user


User = get_user_model()


class RegisterationAPI(APIView):
    class RegistrationInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=255)
        confirm_password = serializers.CharField(max_length=255)

    class RegistrationOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("email", )

    @extend_schema(request=RegistrationInputSerializer, responses=RegistrationOutputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register_user(**serializer.validated_data)
        except Exception as e:
            return Response(
                f"Error in creating user: {e}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.RegistrationOutputSerializer(user, context={"request": request}).data)

