from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name", "description"
        )
        
        
class RoomListSerializer(ModelSerializer):
    
    rating = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta():
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "photos",
        )
        
    def get_rating(self, room):
        return room.average_rating()


class RoomDetailSerializer(ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True) # owner FK를 확장할 때 이 serializer를 사용해라
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta():
        model = Room
        fields = "__all__"
        
    # 메소드 이름은 무조건 **get_속성이름**
    # 파라미터 -> self, 현재 serializing하고 있는 객체
    def get_rating(self, room):
        return room.average_rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user

