from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import UserProfile
from posts.models import Comment, Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_queryset(self):
        queryset = Post.objects.select_related("author").prefetch_related("hashtags")

        hashtag = self.request.query_params.get("hashtag")
        author = self.request.query_params.get("author")
        user_id = self.request.query_params.get("user_id")
        search = self.request.query_params.get("search")
        created_from = self.request.query_params.get("created_from")
        created_to = self.request.query_params.get("created_to")

        if hashtag:
            queryset = queryset.filter(hashtags__name__iexact=hashtag.lstrip("#").lower())
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if user_id:
            queryset = queryset.filter(author_id=user_id)
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search)
                | Q(author__username__icontains=search)
                | Q(hashtags__name__icontains=search.lstrip("#").lower())
            )
        if created_from:
            queryset = queryset.filter(created_at__date__gte=created_from)
        if created_to:
            queryset = queryset.filter(created_at__date__lte=created_to)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        post.liked_by.add(request.user)
        return Response({"detail": "Post liked.", "likes_count": post.liked_by.count()})

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.liked_by.remove(request.user)
        return Response({"detail": "Post unliked.", "likes_count": post.liked_by.count()})

    @action(detail=False, methods=["get"], url_path="my")
    def my_posts(self, request):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="feed")
    def feed(self, request):
        try:
            following_ids = request.user.userprofile.following.values_list("id", flat=True)
        except UserProfile.DoesNotExist:
            following_ids = []

        queryset = self.get_queryset().filter(Q(author=request.user) | Q(author_id__in=following_ids))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        queryset = Comment.objects.select_related("author", "post")
        post_id = self.request.query_params.get("post_id")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
