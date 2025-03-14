from core.services import BaseModelService

from ..models import SMSLog


class SMSLogService(BaseModelService[SMSLog]):
    model_class = SMSLog
