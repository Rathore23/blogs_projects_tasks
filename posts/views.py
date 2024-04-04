from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from accounts.permissions import IsOwnerOrReadOnly
from posts.models import Post, PostPhoto
from posts.serializers import PostSerializer, PostPhotoSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(
        like_count=Count('liked_by')
    ).order_by('-like_count')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = (
        "user__is_staff", "user__is_active",
        "category__title", "category", "user",
    )
    search_fields = (
        "category__title", "user__username", "title", "content",
    )

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated,])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked = False
        else:
            post.liked_by.add(user)
            liked = True

        post.save()
        return Response({'liked': liked})


class PostPhotosViewSet(viewsets.ModelViewSet):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    related_model = Post
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
