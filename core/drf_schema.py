from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema as SpectacularAutoSchema


class AutoSchema(SpectacularAutoSchema):
    def get_operation_id(self) -> str:
        """Get an operation ID that includes the version number.

        This prevents conflicts on auto-generated operation IDs.
        """
        operation_id = super().get_operation_id()
        version, _ = self.view.determine_version(self.view.request, **self.view.kwargs)
        return f"{version}_{operation_id}"


class SecureCookieAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "core.authentication.SecureCookieAuthentication"
    name = "SecureCookieAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "SecureCookieAuthentication",
            "description": "<h4>Clients will get authenticated automatically by getting cookies value once login.</h4>",
        }
