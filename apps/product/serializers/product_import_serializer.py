from rest_framework import serializers


class ProductImportFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        # Allow Excel and CSV files (case-insensitive)
        allowed_ext = (".xls", ".xlsx", ".csv")
        filename = value.name.lower()
        if not filename.endswith(allowed_ext):
            raise serializers.ValidationError("Only Excel (.xls, .xlsx) or CSV (.csv) files are allowed.")
        return value
