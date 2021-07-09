from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from diary.func import set_message
from post.models import Post
from post.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
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

    def post(self, request):
        user = self.request.user
        data = request.data

        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data)
