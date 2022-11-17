from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Room, Amenity
from wishlists.models import Wishlist
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
    is_owner = serializers.SerializerMethodField()
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
            "is_owner",
            "photos",
        )
        
    def get_rating(self, room):
        return room.average_rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):
    
    owner = TinyUserSerializer(read_only=True) # owner FK를 확장할 때 이 serializer를 사용해라
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)
    in_my_wishlist = serializers.SerializerMethodField() # wishlist에 포함된 상태임을 나타내는 필드
    
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
    
    def get_in_my_wishlist(self, room):
        request = self.context['request']
        return Wishlist.objects.filter(
            user=request.user, 
            rooms__pk=room.pk,
        ).exists() # 요청 보낸 유저의 wishlists 중 해당 room을 포함하는 wishlist의 존재 여부
        

