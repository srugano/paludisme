# -*- coding: utf-8 -*-
from rest_framework import serializers
from stock.models import StockProduct, StockOutReport, Product, Report, CasesPaluProv, CasesPaluDis, CasesPaluCDS, StockProductProv, StockProductDis, StockProductCDS


class StockProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    dosage = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = StockProduct
        fields = ('product', 'dosage', 'quantity',  'reporting_date', 'category')

    def get_product(self, obj):
        return obj.product.designation

    def get_dosage(self, obj):
        return obj.dosage.dosage

    def get_category(self, obj):
        return obj.report.category


class StockProductProvSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = StockProductProv
        fields = ('id', 'product', 'quantity_sf',  'year', 'week', 'quantity_sd', 'quantity_sr', 'province')

    def get_province(self, obj):
        return obj.province.name

    def get_id(self, obj):
        return obj.province.id


class StockProductDisSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    class Meta:
        model = StockProductDis
        fields = ('id', 'product', 'quantity_sf',  'year', 'week', 'quantity_sd', 'quantity_sr', 'province', 'district')

    def get_district(self, obj):
        return obj.district.name

    def get_id(self, obj):
        return obj.district.id

    def get_province(self, obj):
        return obj.district.province.name


class StockProductCDSSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    cds = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()

    class Meta:
        model = StockProductCDS
        fields = ('id', 'product', 'quantity_sf',  'year', 'week', 'quantity_sd', 'quantity_sr', 'province', 'district', 'cds')

    def get_cds(self, obj):
        return obj.cds.name

    def get_id(self, obj):
        return obj.cds.id

    def get_district(self, obj):
        return obj.cds.district.name

    def get_province(self, obj):
        return obj.cds.district.province.name


class StockOutProductSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    cds = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = StockOutReport
        fields = ('id', 'province', 'district', 'cds', 'product', 'reporting_date', 'remaining')

    def get_province(self, obj):
        return obj.report.facility.district.province.name

    def get_district(self, obj):
        return obj.report.facility.district.name

    def get_cds(self, obj):
        return obj.report.facility.name

    def get_product(self, obj):
        return obj.product.designation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'designation', 'code')


class CasesPaluSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    simple = serializers.IntegerField()
    acute = serializers.IntegerField()
    pregnant_women = serializers.IntegerField()
    decease = serializers.IntegerField()
    year = serializers.IntegerField()

    class Meta:
        fields = ('simple', 'acute', 'pregnant_women', 'decease', 'week', 'year')


class CasesPaluProvSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = CasesPaluProv
        fields = ('id', 'simple', 'acute', 'pregnant_women', 'decease', 'ge', 'tdr', 'province', 'year', 'week')

    def get_province(self, obj):
        return obj.province.name

    def get_id(self, obj):
        return obj.province.id


class CasesPaluDisSerializer(CasesPaluProvSerializer):
    district = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = CasesPaluDis
        fields = ('id', 'simple', 'acute', 'pregnant_women', 'decease', 'ge', 'tdr', 'district', 'week', 'year', 'province')

    def get_district(self, obj):
        return obj.district.name

    def get_province(self, obj):
        return obj.district.province.name

    def get_id(self, obj):
        return obj.district.id


class CasesPaluCdsSerializer(CasesPaluDisSerializer):
    cds = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = CasesPaluCDS
        fields = ('id', 'simple', 'acute', 'pregnant_women', 'decease', 'ge', 'tdr', 'province', 'week', 'district', 'cds', 'year')

    def get_province(self, obj):
        return obj.cds.district.province.name

    def get_district(self, obj):
        return obj.cds.district.name

    def get_cds(self, obj):
        return obj.cds.name

    def get_id(self, obj):
        return obj.cds.id


class RateSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    week = serializers.IntegerField()
    nombre = serializers.IntegerField()
    expected = serializers.SerializerMethodField()

    def get_expected(self, obj):
        return self.context['nombre_cds']


class ReportSerializer(serializers.ModelSerializer):
    cds = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ('id', 'reporting_date', 'province', 'district', 'cds', 'text', 'category')

    def get_province(self, obj):
        return obj.facility.district.province.name

    def get_district(self, obj):
        return obj.facility.district.name

    def get_cds(self, obj):
        return obj.facility.name
