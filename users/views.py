from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
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
        