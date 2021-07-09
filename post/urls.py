from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, MyPostView

router = DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path("my/", MyPostView.as_view()),
    path("", include(router.urls)),
]
