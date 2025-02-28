from core.services import BaseModelService

from ..models import Blog


class BlogService(BaseModelService[Blog]):
    model_class = Blog
