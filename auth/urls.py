from django.urls import path

from .views import MyLoginView, MyRegisterView

urlpatterns = [
    path("login/", MyLoginView.as_view()),
    path("registration/", MyRegisterView.as_view()),
]
