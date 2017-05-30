from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from stock.models import Product, Report, Reporter, Dosage, StockProduct, Temporary, StockOutReport, PotentialCases, PotentialDeceased, Tests, CasesPalu


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


@admin.register(Tests)
class TestsAdmin(ImportExportModelAdmin):
    pass


@admin.register(StockOutReport)
class StockOutReportAdmin(ImportExportModelAdmin):
    pass


@admin.register(CasesPalu)
class CasesPaluAdmin(ImportExportModelAdmin):
    pass


@admin.register(PotentialDeceased)
class PotentialDeceasedAdmin(ImportExportModelAdmin):
    pass


@admin.register(PotentialCases)
class PotentialCasesAdmin(ImportExportModelAdmin):
    pass
