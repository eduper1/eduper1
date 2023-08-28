from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# handle posts
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)