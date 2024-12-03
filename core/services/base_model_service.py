from typing import Generic

from django.utils.text import slugify
from rest_framework.generics import get_object_or_404

from ..types import DjangoModel, ValidatedDataType
from .core_service import CoreService


class BaseModelService(Generic[DjangoModel]):
    model_class: DjangoModel = None  # type: ignore

    def __init__(self) -> None:
        self.core_service = CoreService()

    def prepare_data(self, validated_data: ValidatedDataType, *args, **kwargs):
        """prepares the validated data as per model requirements"""
        return validated_data

    def get_model_class(self) -> DjangoModel:
        assert self.model_class is not None, (
            "%s should include model_class attribute or override get_model_class() method" % self.__class__.__name__
        )
        return self.model_class

    def get(self, **kwargs) -> DjangoModel:
        """get the single model object with dynamic key"""
        model_class = self.get_model_class()
        instance = get_object_or_404(model_class, **kwargs)
        return instance

    def all(self, **kwargs):
        """get all the model instances by filtering with kwargs argument"""
        model_class = self.get_model_class()
        instances = model_class.objects.filter(**kwargs)
        return instances

    def get_slug_or_raise_exception(self, field_value: str) -> str:
        """make a slug value and get a slugified value for given field_value"""
        model_class = self.get_model_class()
        slug = slugify(field_value)
        if model_class.objects.filter(slug=slug).exists():
            # TODO: Handle with Generic Exception Class
            raise Exception("Already Exists !")
        return slug

    def create(self, validated_data: ValidatedDataType, **kwargs) -> DjangoModel:
        """create an model instance with the given validated data"""
        # TODO: the user tagging can be handled by decorator pattern.
        validated_data = self.prepare_data(validated_data)
        model_class = self.get_model_class()
        request = kwargs.get("request")
        user = self.core_service.get_user(request)
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        instance = model_class.objects.create(**validated_data)
        return instance

    def update(self, instance: DjangoModel, validated_data: ValidatedDataType, **kwargs) -> DjangoModel:
        """update an instance model with the given validated data"""
        request = kwargs.get("request")
        user = self.core_service.get_user(request)
        validated_data["updated_by"] = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
