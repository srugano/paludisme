# -*- coding: utf-8 -*-
from rest_framework import serializers
from stock.models import StockProduct, StockOutReport, Product, CasesPalu


class StockProductSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    cds = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    dosage = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = StockProduct
        fields = ('id', 'province', 'district', 'cds', 'product', 'dosage', 'quantity', 'cds', 'reporting_date', 'category')

    def get_province(self, obj):
        return obj.report.facility.district.province.name

    def get_district(self, obj):
        return obj.report.facility.district.name

    def get_cds(self, obj):
        return obj.report.facility.name

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


class StockProductSerializer2(serializers.Serializer):
    act_14ans_et_plus = serializers.IntegerField()
    act_1_5ans = serializers.IntegerField()
    act_2_11_mois = serializers.IntegerField()
    act_6_13ans = serializers.IntegerField()
    art = serializers.IntegerField()
    qui_100mg = serializers.IntegerField()
    qui_300mg = serializers.IntegerField()
    qui_500mg = serializers.IntegerField()
    sp = serializers.IntegerField()
    tdr = serializers.IntegerField()

    class Meta:
        fields = ('act_14ans_et_plus', 'act_1_5ans', 'act_2_11_mois', 'act_6_13ans', 'art', 'qui_100mg', 'qui_300mg', 'qui_500mg', 'sp', 'tdr', )
