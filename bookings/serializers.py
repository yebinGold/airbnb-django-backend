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


class CreateExperienceBookingSerializer(ModelSerializer):
    
    # field overriding -> as required
    experience_time = serializers.DateTimeField()
    
    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests"
        ) # 유저에게 직접 받아와야 하는 값들
        
    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now()).date()
        start = self.context['experience'].start # 체험 시작 시간
        end = self.context['experience'].end # 체험 끝 시간
        date = value.date() # 예약 날짜
        time = value.time() # 예약 시간
        
        if now > date:
            raise serializers.ValidationError("Can't book in the past.")
        if start > time or time > end:
            raise serializers.ValidationError("No experience at that time!")
        if Booking.objects.filter(experience_time=value).exists():
            raise serializers.ValidationError("That schedule is already booked!")
        return value
        

class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
        