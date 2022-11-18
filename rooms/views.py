from django.conf import settings
from django.utils import timezone
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Room, Amenity
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer

from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.serializers import PublicBookingSerializer
from bookings.models import Booking


class Amenities(APIView):
    
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return serializer.errors
    

class AmenityDetail(APIView):
    
    def get_object(self, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
            return amenity
        except Amenity.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)
    
    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request":request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category") # (required) -> 새로운 객체 생성 전에 찾아와서 넘겨줌
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    new_room = serializer.save(owner=request.user, category=category)
                    amenities = request.data.get("amenities") # (not required) -> 새로운 객체 생성 후에 추가 작업
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        new_room.amenities.add(amenity) # manytomany에 값 추가
                    return Response(RoomDetailSerializer(new_room).data)
            except Exception: # 어떤 에러가 발생하든지
                raise ParseError("Amenity not found") # 사용자에게 에러 메시지 표시
            
        else:
            return Response(serializer.errors)
    
    
class RoomDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request":request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        
        if request.data.get("category"):
            try:
                category_pk = request.data.get("category")
                new_category = Category.objects.get(pk=category_pk)
                if new_category.kind != Category.CategoryKindChoices.ROOMS:
                    category = room.category
                    raise ParseError("Category kind should be 'room'")
                else: 
                    category = new_category
            except Category.DoesNotExist:
                raise ParseError("Category not found")
        else:
            category = room.category
        
        if serializer.is_valid():
            try:
                with transaction.atomic(): 
                    updated_room = serializer.save(category=category)
                    
                    if request.data.get("amenities"):
                        new_amenities = request.data.get("amenities")
                        updated_room.amenities.clear()
                        for amenity_pk in new_amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)
                    return Response(RoomDetailSerializer(updated_room).data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
   
    
class RoomReviews(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        try:
            page = int(request.query_params.get('page', 1))
            print(page)
        except ValueError:
            page = 1
            
        page_size = settings.PAGE_SIZE # 한 번에 3개씩
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)
        
    def post(self, request, pk):
        room = self.get_object(pk)  
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=room)
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)
   
    
class RoomAmenities(APIView):
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        try:
            page = int(request.query_params.get('page', 1))
            print(page)
        except ValueError:
            page = 1
            
        page_size = settings.PAGE_SIZE # 한 번에 3개씩
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True)
        return Response(serializer.data)
   
        
class RoomPhotos(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def post(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room) # 해당 room에 사진 추가
            return Response(PhotoSerializer(photo).data)
        else: 
            return Response(serializer.errors)


class RoomBookings(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room, 
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now, # 현재 날짜보다 뒤의 예약만 보여줌
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
        

"""
{
"name":"hello",
"country":"Korea",
"city":"Seoul",
"price":2500,
"rooms":3,
"toilets":1,
"desc":"welcome",
"address":"Imun 123",
"category":1,
"amenities":[1,2,3],
"kind":"private_room"
}
"""