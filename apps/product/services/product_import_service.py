import pandas as pd
from django.core.files.storage import default_storage

from apps.company.models import Company, CompanyCategory
from apps.product.models import Product, ProductCategory
from apps.uom.models import UoM


class ProductImportService:
    required_file_headers = [
        "supplier",
        "supplier_category",
        "product",
        "product_category",
        "sku_code",
        "uom",
    ]

    @staticmethod
    def get_dataframe(file_full_path):
        file_ext = file_full_path.lower().split(".")[-1]
        if file_ext in ["xls", "xlsx"]:
            return pd.read_excel(file_full_path)
        return pd.read_csv(file_full_path)

    @classmethod
    def import_products(cls, file_full_path):
        df = cls.get_dataframe(file_full_path)
        # Trim all string values
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        products_created = 0
        for _, row in df.iterrows():
            company_category_name = row.get("supplier_category")
            company_name = row.get("supplier")
            product_category_name = row.get("product_category")
            uom_name = row.get("uom")
            if not company_name or not company_category_name or not product_category_name or not uom_name:
                continue
            company_category, _ = CompanyCategory.objects.get_or_create(name=company_category_name)
            company, _ = Company.objects.get_or_create(name=company_name, defaults={"category": company_category})
            product_category, _ = ProductCategory.objects.get_or_create(name=product_category_name)
            uom, _ = UoM.objects.get_or_create(name=uom_name)
            product, created = Product.objects.get_or_create(
                name=row.get("product"),
                defaults={
                    "company": company,
                    "company_category": company_category,
                    "product_category": product_category,
                    "sku_code": row.get("sku_code"),
                    "uom": uom,
                    # Add other fields as needed
                },
            )
            if created:
                products_created += 1
        # Clean up file
        default_storage.delete(file_full_path)
        return products_created

    @classmethod
    def validate_file(cls, file_full_path):
        try:
            df = cls.get_dataframe(file_full_path)
        except Exception as e:
            return {"error": f"Could not read file: {str(e)}"}

        # Validate required headers (case sensitive)
        missing_headers = [h for h in cls.required_file_headers if h not in df.columns]
        if missing_headers:
            return {"error": f"Missing required header(s): {', '.join(missing_headers)}"}

        # Trim all string values in the DataFrame
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Check for missing/empty values in required columns
        missing_cells = []
        for col in cls.required_file_headers:
            missing_rows = df[df[col].isnull() | (df[col].astype(str).str.strip() == "")].index.tolist()
            for row_idx in missing_rows:
                missing_cells.append({"row": row_idx + 2, "column": col})  # +2 for header and 0-index
        if missing_cells:
            return {"error": "Missing value(s) in required columns.", "details": missing_cells}

        return None
