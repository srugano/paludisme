from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from stock.models import Product, Report, Reporter, Dosage, StockProduct, Temporary


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
    pass


@admin.register(Reporter)
class ReporterAdmin(ImportExportModelAdmin):
    pass


@admin.register(Dosage)
class DosageAdmin(ImportExportModelAdmin):
    pass


@admin.register(StockProduct)
class StockProductAdmin(ImportExportModelAdmin):
    pass


@admin.register(Temporary)
class TemporaryAdmin(ImportExportModelAdmin):
    pass