from import_export import resources
from .models import CasesPalu, StockProduct, Tests
from import_export import fields
from django.db.models import Sum
import datetime


class CasesPaluResource(resources.ModelResource):
    province = fields.Field()
    district = fields.Field()
    etablissement = fields.Field()
    goute_epaisse = fields.Field()
    tdr = fields.Field()

    class Meta:
        model = CasesPalu
        fields = ('reporting_date', 'province', 'district', 'etablissement', 'simple', 'acute', 'pregnant_women', 'decease', 'goute_epaisse', 'tdr')
        export_order = ('reporting_date', 'province', 'district', 'etablissement', 'simple', 'acute', 'pregnant_women', 'decease', 'goute_epaisse', 'tdr')

    def dehydrate_province(self, book):
        return '%s' % (book.report.facility.district.province.name)

    def dehydrate_district(self, book):
        return '%s' % (book.report.facility.district.name)

    def dehydrate_etablissement(self, book):
        return '%s' % (book.report.facility.name)

    def dehydrate_goute_epaisse(self, book):
        queryset = Tests.objects.filter(report__facility=book.report.facility, reporting_date=book.reporting_date)
        return queryset.aggregate(ges=Sum('ge'))['ges']

    def dehydrate_tdr(self, book):
        queryset = Tests.objects.filter(report__facility=book.report.facility, reporting_date=book.reporting_date)
        return queryset.aggregate(tdrs=Sum('tdr'))['tdrs']


class StockProductResource(resources.ModelResource):
    dosage = fields.Field()
    province = fields.Field()
    district = fields.Field()
    etablissement = fields.Field()

    class Meta:
        model = StockProduct
        fields = ('reporting_date', 'province', 'district', 'etablissement', 'dosage', 'quantity',)
        export_order = ('reporting_date', 'province', 'district', 'etablissement', 'dosage', 'quantity',)

    def dehydrate_dosage(self, book):
        return '%s' % (book.dosage.dosage)

    def dehydrate_province(self, book):
        return '%s' % (book.report.facility.district.province.name)

    def dehydrate_district(self, book):
        return '%s' % (book.report.facility.district.name)

    def dehydrate_etablissement(self, book):
        return '%s' % (book.report.facility.name)
