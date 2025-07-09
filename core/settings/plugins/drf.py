REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_VERSION": "v1",
    "VERSION_PARAM": "version",
    "ALLOWED_VERSIONS": None,  # Allowed all for fixed use ["v1", "v2"]
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.SecureCookieAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "core.drf_schema.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}
