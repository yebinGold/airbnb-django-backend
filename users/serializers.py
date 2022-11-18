from rest_framework.serializers import ModelSerializer
from .models import User

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_photo",
            "username"
        )
        

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password", 
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions"
        )
        

class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "profile_photo",
            "username",
            "gender",
            "language",
            "currency",
        )