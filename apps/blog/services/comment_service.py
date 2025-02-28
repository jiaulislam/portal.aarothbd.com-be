from core.services import BaseModelService

from ..models import Comment


class CommentService(BaseModelService[Comment]):
    model_class = Comment
