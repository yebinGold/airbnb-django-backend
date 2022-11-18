from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Booking

class CreateRoomBookingerializer(ModelSerializer):
    
    # field overriding -> as required
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    
    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests"
        ) # 유저에게 직접 받아와야 하는 값들

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past.")
        else:
            return value
    
    def validate(self, data):
        if data["check_out"] <= data['check_in']:
            raise serializers.ValidationError("Check in shoud be earlier than Check out.")
        if Booking.objects.filter(check_in__lte=data['check_out'], check_out__gte=data["check_in"]).exists():
            raise serializers.ValidationError("Those dates are already booked.")
        return data


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )