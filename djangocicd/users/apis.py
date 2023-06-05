from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView, status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import RefreshToken
from djangocicd.users.models import Profile

from djangocicd.api.mixins import ApiAuthMixin
from djangocicd.users.selectors import get_user_profile 
from djangocicd.users.services import register_user
from djangocicd.users.validators import digits_validator, letters_validator, special_chars_validator, validate_email


User = get_user_model()


class ProfileAPI(ApiAuthMixin, APIView):
    class ProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            exclude = ("id", "user")

        def to_representation(self, instance):
            repr = super().to_representation(instance)
            user_email = instance.user.email
            # getting cached data based onthe user's email
            # key of cached data is expected to be the following pattern:
            # profile_<user_email>
            profile_cache = cache.get(f"profile_{user_email}", {})
            if profile_cache:
                repr["posts_number"] = profile_cache.get("posts_number")
                repr["subscriber_number"] = profile_cache.get("subscriber_number", 0)
                repr["subscription_number"] = profile_cache.get("subscription_number", 0)
            return repr

    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request):
        profile = get_user_profile(user=request.user)
        serializer = self.ProfileOutputSerializer(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterationAPI(APIView):
    class RegistrationInputSerializer(serializers.Serializer):
        email = serializers.EmailField(validators=[validate_email])
        bio = serializers.CharField(max_length=300, required=False)
        password = serializers.CharField(max_length=255, validators=[
            MinLengthValidator(limit_value=10),
            digits_validator, 
            letters_validator, 
            special_chars_validator,
        ])
        confirm_password = serializers.CharField(max_length=255)

        def validate(self, attrs):
            if not attrs.get("password") or not attrs.get("confirm_password"):
                raise serializers.ValidationError("'password' and 'password confirmation' fields are required")

            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError("passwords don't match")
            
            return super().validate(attrs)
        

    class RegistrationOutputSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = User
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            token_class = RefreshToken
            data = dict()

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=RegistrationInputSerializer, responses=RegistrationOutputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.validated_data.pop("confirm_password")
            user = register_user(**serializer.validated_data)
        except Exception as e:
            return Response(
                f"Error in creating user: {e}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.RegistrationOutputSerializer(user, context={"request": request}).data, status=status.HTTP_201_CREATED)

