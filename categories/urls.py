from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryViewSet.as_view({
        'get': 'list', # get 요청을 받으면 list 메소드 실행
        'post': 'create', # post 요청 받으면 create 메소드 실행
    })),
    path("<int:pk>", views.CategoryViewSet.as_view({
        'get': 'retrieve', # 객체 하나만 찾아서 반환
        'put': 'partial_update',
        'delete': 'destroy',
    })),
]
