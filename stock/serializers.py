# -*- coding: utf-8 -*-
from rest_framework import serializers
from stock.models import StockProduct, StockOutReport, Product, CasesPalu, Tests
from django.db.models import Sum
from bdiadmin.models import CDS


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


class CasesPalu2Serializer(serializers.ModelSerializer):
    ge = serializers.SerializerMethodField()
    tdr = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()

    class Meta:
        model = CasesPalu
        fields = ('simple', 'acute', 'pregnant_women', 'decease', 'ge', 'tdr', 'province')

    def get_ge(self, obj):
        return Tests.objects.filter(reporting_date=obj['reporting_date'], report__facility__district__province=obj['report__facility__district__province']).aggregate(ges=Sum('ge'))['ges']

    def get_tdr(self, obj):
        return Tests.objects.filter(reporting_date=obj['reporting_date'], report__facility__district__province=obj['report__facility__district__province']).aggregate(tdrs=Sum('tdr'))['tdrs']

    def get_province(self, obj):
        return CDS.objects.filter(district__province=obj['report__facility__district__province']).first().district.province.name


class RateSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    week = serializers.IntegerField()
    nombre = serializers.IntegerField()
    expected = serializers.SerializerMethodField()

    def get_expected(self, obj):
        return self.context['nombre_cds']
