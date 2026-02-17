from rest_framework import serializers

from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    hashtag_list = serializers.SlugRelatedField(
        source="hashtags",
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_username",
            "content",
            "media",
            "likes_count",
            "is_liked",
            "hashtag_list",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "author_username", "hashtag_list", "created_at", "updated_at")

    def get_likes_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.liked_by.filter(id=request.user.id).exists()


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "author_username", "content", "created_at", "updated_at")
        read_only_fields = ("id", "author", "author_username", "created_at", "updated_at")
