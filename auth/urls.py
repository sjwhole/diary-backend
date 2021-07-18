from django.urls import path

from .views import MyLoginView, MyRegisterView, kakao

urlpatterns = [
    path("login/", MyLoginView.as_view()),
    path("kakao/login/", kakao),
    path("registration/", MyRegisterView.as_view()),
]
