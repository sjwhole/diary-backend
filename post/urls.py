from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostCreateViewSet, PostReadUpdateDeleteView, PostSharedViewSet, MyPostView

router = DefaultRouter()
router.register("", PostSharedViewSet)

urlpatterns = [
    path("my/", MyPostView.as_view()),
    path("<int:pk>/", PostReadUpdateDeleteView.as_view()),
    path("", PostCreateViewSet.as_view()),
    path("share/", include(router.urls)),
]
