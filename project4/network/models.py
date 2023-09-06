from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# handle posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    # dislikes = models.ManyToManyField(User, related_name="disliked_posts", blank=True)
    def count_likes(self):
        return self.likes.count()