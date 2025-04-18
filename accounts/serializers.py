from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from accounts.models import Profile  

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture', 'address', 'city', 'state', 'country']


# Custom User Create Serializer (for registration)
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'role', 'email', 'password', 'phone']  


# Custom User Serializer (for fetching logged-in user info with nested profile)
class UserSerializer(BaseUserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'role', 'phone', 'profile']


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']