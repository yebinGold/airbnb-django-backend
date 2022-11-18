from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer

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
