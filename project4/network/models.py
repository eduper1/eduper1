from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='userProfile', on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.user.userProfile.followers.count()

# handle posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    # dislikes = models.ManyToManyField(User, related_name="disliked_posts", blank=True)
    def count_likes(self):
        return self.likes.count()