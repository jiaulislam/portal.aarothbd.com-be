from core.services import BaseModelService

from ..models import Blog


class BlogService(BaseModelService):
    model_class = Blog
