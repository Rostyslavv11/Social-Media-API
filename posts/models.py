import re

from django.conf import settings
from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    content = models.TextField()
    media = models.ImageField(upload_to="post_media/", blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_id}: {self.content[:30]}"

    @staticmethod
    def extract_hashtags(content: str) -> set[str]:
        tags = re.findall(r"#([A-Za-z0-9_]+)", content or "")
        return {tag.lower() for tag in tags}

    def sync_hashtags(self) -> None:
        tag_names = self.extract_hashtags(self.content)
        tag_objects = [Hashtag.objects.get_or_create(name=name)[0] for name in tag_names]
        self.hashtags.set(tag_objects)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_hashtags()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_id}: {self.content[:30]}"
