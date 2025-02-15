from django.urls import path

from .views.blog_views_v1 import BlogListAPIView, BlogRetrieveAPIView

urlpatterns = [
    path(r"ecomm/blogs/", BlogListAPIView.as_view(), name="blog-list-view"),
    path(r"ecomm/blogs/<str:slug>/", BlogRetrieveAPIView.as_view(), name="blog-retrieve-view"),
]
