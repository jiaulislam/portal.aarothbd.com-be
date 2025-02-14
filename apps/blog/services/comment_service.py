from core.services import BaseModelService

from ..models import Comment


class CommentService(BaseModelService):
    model_class = Comment
