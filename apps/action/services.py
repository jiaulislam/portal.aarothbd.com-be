import os

from django.apps import apps
from django.core.management import call_command

from core.exceptions.common import CustomException
from core.services import BaseModelService
from core.services.sentry_service import capture_exception_sentry

from .models import Action


class ActionService(BaseModelService[Action]):
    model_class = Action

    def get_actions_data(self, app_name: str = "data_migration"):
        mapped_data = []
        try:
            app_config = apps.get_app_config(app_name)
            commands_dir = os.path.join(app_config.path, "management", "commands")
            if os.path.exists(commands_dir):
                commands = [
                    os.path.splitext(f)[0] for f in os.listdir(commands_dir) if f.endswith(".py") and f != "__init__.py"
                ]
                for command in commands:
                    _segments = command.split("_")
                    title = " ".join([segment.title() for segment in _segments])
                    _data = {}
                    _data["codename"] = command
                    _data["name"] = title
                    mapped_data.append(_data)
                return mapped_data
            else:
                return []
        except LookupError as exc:
            capture_exception_sentry(exc)
            raise CustomException(detail="Unable to lookup for actions !", code="server_error")

    def call_action(self, action_name: str) -> None:
        try:
            call_command(action_name)
        except Exception as exc:
            capture_exception_sentry(exc)
            raise CustomException(detail=str(exc), code="server_error")
