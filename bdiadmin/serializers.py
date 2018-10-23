from rest_framework import serializers
from bdiadmin.models import Province, District, CDS


class ProvinceSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Province model """

    class Meta:
        model = Province
        fields = ("name", "code", "id")


class DistrictSerializer(serializers.ModelSerializer):
    """ Serializer to represent the District model """

    class Meta:
        model = District
        fields = ("name", "code", "province", "id")


class CDSSerializer(serializers.ModelSerializer):
    """ Serializer to represent the District model """

    class Meta:
        model = CDS
        fields = ("name", "code", "district", "id")
