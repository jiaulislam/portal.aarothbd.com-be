from django.urls import path

from .views import TestimonialListAPIView

urlpatterns = [
    path(r"testimonials/", TestimonialListAPIView.as_view(), name="testimonial-list-view"),
]
