# -*- coding: utf-8 -*-
from rest_framework import serializers
from stock.models import StockProduct, StockOutReport, Product


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


class RateSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    week = serializers.IntegerField()
    nombre = serializers.IntegerField()
    expected = serializers.SerializerMethodField()

    def get_expected(self, obj):
        return self.context['nombre_cds']
