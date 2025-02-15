from django.urls import path

from .views.blog_views_v1 import BlogListCreateAPIView, BlogRetrieveAPIView
from .views.comment_view_v1 import CommentBlogCreateAPIView

urlpatterns = [
    path(r"ecomm/blogs/", BlogListCreateAPIView.as_view(), name="blog-list-create-view"),
    path(r"ecomm/blogs/<str:slug>/", BlogRetrieveAPIView.as_view(), name="blog-retrieve-view"),
    path(r"ecomm/comments/", CommentBlogCreateAPIView.as_view(), name="comment-create-view"),
]
