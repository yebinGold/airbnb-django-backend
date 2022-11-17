from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound

from .models import Wishlist
from .serializers import WishlistSerializer

from rooms.models import Room


class Wishlists(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)
    

class WishlistDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            return Response(WishlistSerializer(updated_wishlist).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)
  

class WishlistRoomToggle(APIView):
    
    """ wishlist의 rooms 리스트에 room을 추가하고, 이미 해당 room이 존재하면 삭제하는 view """
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_list(self, pk, user):
        
        """  room을 추가/삭제할 wishlist를 찾는 메소드 """
        
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
    
    def get_room(self, pk):
        
        """ wishlist에 추가/삭제할 room을 찾는 메소드 """
        
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)