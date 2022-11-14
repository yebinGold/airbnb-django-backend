from rest_framework.serializers import ModelSerializer
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name", "description"
        )
        
        
class RoomListSerializer(ModelSerializer):
    class Meta():
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


class RoomDetailSerializer(ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True) # owner FK를 확장할 때 이 serializer를 사용해라
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta():
        model = Room
        fields = "__all__"

