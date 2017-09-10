from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from stock.models import Product, Report, Reporter, Dosage, StockProduct, Temporary, StockOutReport, PotentialCases, PotentialDeceased, Tests, CasesPalu, CasesPaluProv


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("designation", "code",)
    search_fields = ("designation", "dosages", "code",)
    list_filter = ('designation',)


@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
    list_display = ("facility", "reporting_date", "text", "category")
    search_fields = ("facility", "text", "category")
    list_filter = ("category",)
    date_hierarchy = ("reporting_date")


@admin.register(Reporter)
class ReporterAdmin(ImportExportModelAdmin):
    list_display = ("facility", "phone_number", "supervisor_phone_number", )
    search_fields = ("facility__name", "phone_number", "supervisor_phone_number", )
    list_filter = ("facility", "phone_number", "supervisor_phone_number", )


@admin.register(Dosage)
class DosageAdmin(ImportExportModelAdmin):
    pass


@admin.register(StockProduct)
class StockProductAdmin(ImportExportModelAdmin):
    list_display = ("report", "product", "dosage", "quantity", "reporting_date" )
    search_fields = ("report__text",)
    list_filter = ("report__category", "product", )
    date_hierarchy = ("reporting_date")



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


@admin.register(CasesPaluProv)
class CasesPaluProvAdmin(ImportExportModelAdmin):
    pass


@admin.register(PotentialDeceased)
class PotentialDeceasedAdmin(ImportExportModelAdmin):
    pass


@admin.register(PotentialCases)
class PotentialCasesAdmin(ImportExportModelAdmin):
    pass
