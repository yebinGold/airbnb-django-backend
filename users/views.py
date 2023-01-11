import jwt
import requests

from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from .serializers import PrivateUserSerializer, PublicUserSerializer
from .models import User

from reviews.serializers import UserReviewListSerializer
from wishlists.serializers import WishlistSerializer
from bookings.serializers import PublicBookingSerializer
from bookings.models import Booking


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyReviews(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        my_reviews = user.reviews.all()
        serializer = UserReviewListSerializer(my_reviews, many=True)
        return Response(serializer.data)


class MyWishlists(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        wishlists = user.wishlists.all()
        serializer = WishlistSerializer(wishlists, many=True, context={'request':request})
        return Response(serializer.data)


class MyBookings(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        room_bookings = user.bookings.filter(kind=Booking.BookingKindChoices.ROOM)
        experience_bookings = user.bookings.filter(kind=Booking.BookingKindChoices.EXPERIENCE)
        rb_serializer = PublicBookingSerializer(room_bookings, many=True)
        exb_serializer = PublicBookingSerializer(experience_bookings, many=True)
        return Response({
            "forRooms": rb_serializer.data,
            "forExperiences": exb_serializer.data
        })


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        

class LogIn(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, 
                            username=username, 
                            password=password
        ) # 해당 정보에 맞는 user가 있다면 찾아옴
        if user:
            login(request, user) # user를 로그인 시키고 세션 생성, 사용자에게 cookie를 보내줌
            return Response({"ok": "welcome!"})
        else:
            return Response({"error": "일치하는 유저가 없습니다."})


class LogOut(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
    


class JWTLogIn(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, 
                            username=username, 
                            password=password
        ) # 해당 정보에 맞는 user가 있다면 찾아옴
        if user:
            # sign the token
            token = jwt.encode({"pk":user.pk}, 
                               settings.SECRET_KEY, # 장고가 제공하는 secret key로 토큰에 서명
                               algorithm="HS256", # 업계 표준 토큰 암호화 알고리즘
            )
            return Response({"token": token})
        else:
            return Response({"error": "일치하는 유저가 없습니다."})
        

class GithubLogIn(APIView):
    
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=dd7325ccd13b98e589f2&client_secret={settings.GH_SECRET}",
                headers={
                    "Accept": "application/json" # json response를 요청
                },
                )
            access_token = access_token.json()['access_token']
            user_data = requests.get(
                "https://api.github.com/user", 
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_email = requests.get(
                "https://api.github.com/user/emails", 
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_email = user_email.json()
            try:
                user = User.objects.get(email=user_email[0]['email']) # github에서 받은 이메일로 유처 찾기
                login(request, user) # 유저 찾았으면 로그인 시켜주기
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get('login'),
                    email=user_email[0]['email'],
                    name=user_data.get('name'),
                    profile_photo=user_data.get('avatar_url'),
                )
                user.set_unusable_password() # password를 사용해서 로그인 불가 only by social networks
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            #print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)