from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import Testimonial


class TestimonialSerializer(s.ModelSerializer):
    class Meta:
        model = Testimonial
        exclude = AUDIT_COLUMNS
