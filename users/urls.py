from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("me/reviews", views.MyReviews.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("@<str:username>", views.PublicUser.as_view()), # /me url path와 user 'me'를 구분하기 위한 @
]
