# -*- coding: utf-8 -*-
from rest_framework import serializers
from stock.models import StockProduct


class StockProductSerializer(serializers.ModelSerializer):
    province = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    cds = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    dosage = serializers.SerializerMethodField()

    class Meta:
        model = StockProduct
        fields = ('id', 'province', 'district', 'product', 'dosage', 'quantity', 'cds',)

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

