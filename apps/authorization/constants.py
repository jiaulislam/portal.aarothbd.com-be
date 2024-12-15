from enum import Enum


class ExcludePermissionModelsList(str, Enum):
    LOG = "logentry"
    CONTENT_TYPE = "contenttype"
    SESSION = "session"
    REVISION = "revision"
    VERSION = "version"
    TOKEN = "token"
    TOKEN_PROXY = "tokenproxy"
    TRANSACTION_NOTIFICATION_LOG = "transactionnotificationlog"
    GROUP = "group"
    PERMISSIONS = "permission"
    BLACK_LIST_TOKEN = "blacklistedtoken"
    OUTSTANDING_TOKEN = "outstandingtoken"
