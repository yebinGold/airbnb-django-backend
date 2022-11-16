from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Room, Amenity
from categories.models import Category
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from reviews.serializers import ReviewSerializer

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
    
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.is_authenticated:    
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
        else:
            raise NotAuthenticated
        
    
class RoomDetail(APIView):
    
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
        if not request.user.is_authenticated:
            raise NotAuthenticated
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
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class RoomReviews(APIView):
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all(), many=True)
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