
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.handlePost, name="handlePost"),
    path("post/<int:postId>", views.handleLikes, name="handleLikes"),
    path("editPost/<int:editId", views.editPost, name="editPost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
