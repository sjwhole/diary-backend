from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from diary.utils import set_message
from post.models import Post
from post.serializers import PostSerializer
from .permissions import IsOwner


class PostCreateViewSet(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsOwner]


class PostSharedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(share=True)
    serializer_class = PostSerializer


class MyPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        year = request.GET.get("year")
        month = request.GET.get("month")

        if not year or not month:
            content = set_message("조회할 기간 입력하세요.")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.filter(user=user, created_at__year=year, created_at__month=month)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
