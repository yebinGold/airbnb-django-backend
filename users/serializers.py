from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
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