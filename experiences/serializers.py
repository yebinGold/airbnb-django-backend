from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Perk, Experience
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer

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
    start = serializers.TimeField()
    end = serializers.TimeField()
    photos = PhotoSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = "__all__"
        
    def validate(self, data):
        experience = Experience.objects.get(pk=self.context["pk"])
        
        start = data['start'] if "start" in data else experience.start
        end = data['end'] if "end" in data else experience.end
        if start >= end:
            raise serializers.ValidationError("start time should be earlier than end time.")
        return data
    
    def get_rating(self, experience):
        return experience.average_rating()