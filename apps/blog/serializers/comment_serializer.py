from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from ..models import Comment

__all__ = ["CommentSerializer"]


class CommentSerializer(s.ModelSerializer):
    class Meta:
        model = Comment
        exclude = AUDIT_COLUMNS
