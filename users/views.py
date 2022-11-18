from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from .serializers import PrivateUserSerializer, PublicUserSerializer
from .models import User

class Me(APIView):
    
    """ My Profile """
    
    permission_classes = [IsAuthenticated] # 내 프로필 정보를 보고 수정 -> 나만 가능(private url)
    
    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)
    
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(PrivateUserSerializer(updated_user).data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    
    """ Create User Account """

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Check your password.")
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    
    """ Get Other User's public profile """
    
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound    
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        old_password = request.data.get('old-password')
        new_password = request.data.get('new-password')
        if not old_password or not new_password: # 데이터 없으면
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

