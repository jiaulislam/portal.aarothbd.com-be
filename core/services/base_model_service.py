from typing import Generic, Type

from django.utils.text import slugify
from rest_framework.generics import get_object_or_404

from core.exceptions import SlugAlreadyExistException

from ..types import _T, BaseSerializerValidatedDataType
from .core_service import CoreService


class BaseModelService(Generic[_T]):
    model_class: Type[_T] = None  # type: ignore

    def __init__(self) -> None:
        self.core_service = CoreService()

    def prepare_data(self, validated_data: BaseSerializerValidatedDataType, *args, **kwargs):
        """prepares the validated data as per model requirements"""
        return validated_data

    def get_model_class(self) -> Type[_T]:
        assert self.model_class is not None, (
            "%s should include model_class attribute or override get_model_class() method" % self.__class__.__name__
        )
        return self.model_class

    def get(self, **kwargs) -> _T:
        """get the single model object with dynamic key"""
        select_related = kwargs.pop("select_related", [])
        prefetch_related = kwargs.pop("prefetch_related", [])
        model_class = self.get_model_class()
        queryset = model_class.objects.all()
        if select_related and type(select_related) is list:
            queryset = queryset.select_related(*select_related)
        if prefetch_related and type(prefetch_related) is list:
            queryset = queryset.prefetch_related(*prefetch_related)
        queryset = get_object_or_404(queryset, **kwargs)
        return queryset

    def all(self, **kwargs):
        """get all the model instances by filtering with kwargs argument"""
        select_related = kwargs.pop("select_related", [])
        prefetch_related = kwargs.pop("prefetch_related", [])
        model_class = self.get_model_class()
        queryset = model_class.objects.all()
        if select_related and type(select_related) is list:
            queryset = queryset.select_related(*select_related)
        if prefetch_related and type(prefetch_related) is list:
            queryset = queryset.prefetch_related(*prefetch_related)
        queryset = queryset.filter(**kwargs)
        return queryset

    def get_slug_or_raise_exception(self, field_value: str) -> str:
        """make a slug value and get a slugified value for given field_value"""
        model_class = self.get_model_class()
        slug = slugify(field_value)
        slug_exists = model_class.objects.filter(slug=slug).exists()
        if slug_exists:
            raise SlugAlreadyExistException()
        return slug

    def create(self, validated_data: BaseSerializerValidatedDataType, **kwargs) -> _T:
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

    def update(self, instance: _T, validated_data: BaseSerializerValidatedDataType, **kwargs) -> _T:
        """update an instance model with the given validated data"""
        request = kwargs.get("request")
        user = self.core_service.get_user(request)
        validated_data["updated_by"] = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
