from rest_framework.serializers import ModelSerializer
from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

class PerkSerializer(ModelSerializer):
    class Meta():
        model = Perk
        fields = "__all__"
        
        
class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "address",
            "description",
        )
        
        
class ExperienceDetailSerializer(ModelSerializer):
    
    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Experience
        fields = "__all__"