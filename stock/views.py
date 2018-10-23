import datetime
from django.shortcuts import render
from django.conf import settings
import django_filters
from django.db.models.functions import Extract
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from stock.models import StockProduct, Dosage, StockOutReport, CasesPalu, Report
from rest_framework import viewsets
from stock.serializers import (
    StockProductSerializer,
    StockOutProductSerializer,
    ProductSerializer,
    CasesPaluSerializer,
    RateSerializer,
    CasesPaluProvSerializer,
    CasesPaluDisSerializer,
    CasesPaluCdsSerializer,
    StockProductCDSSerializer,
    StockProductDisSerializer,
    StockProductProvSerializer,
    ReportSerializer,
)
from bdiadmin.models import CDS, District, Province
from django.http import JsonResponse
from django.contrib import messages
from stock.tasks import export_cases_palu, export_stock_product
from django.views.decorators.csrf import csrf_exempt

GROUPS = getattr(settings, "RUPTURE_GROUPS", "")


class StockProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(name="report", lookup_expr="category")

    class Meta:
        model = StockProduct
        fields = ["dosage", "product", "report", "category"]


class StockProductSFViewsets(viewsets.ModelViewSet):
    queryset = StockProduct.objects.filter(report__category="SF")
    serializer_class = StockProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = (
        "report__facility__district__province",
        "report__facility__district",
        "report__facility",
    )

    def get_queryset(self):
        startdate = self.request.GET.get("startdate", "")
        enddate = self.request.GET.get("enddate", "")
        if startdate and startdate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__gte=datetime.datetime.strptime(
                    startdate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        if enddate and enddate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__lte=datetime.datetime.strptime(
                    enddate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        list_of_ids = []
        for i in CDS.objects.all():
            raba = Report.objects.filter(category="SF", facility=i)
            if raba:
                list_of_ids.append(raba.latest("reporting_date").id)
        return self.queryset.filter(report__id__in=list_of_ids)


class StockProductProvViewsets(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = StockProductProvSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class StockProductDisViewsets(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = StockProductDisSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class StockProductCDSViewsets(viewsets.ModelViewSet):
    queryset = CDS.objects.all()
    serializer_class = StockProductCDSSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class StockProductSRViewsets(StockProductSFViewsets):
    queryset = StockProduct.objects.filter(report__category="SR")


class StockOutProductViewsets(viewsets.ModelViewSet):
    queryset = StockOutReport.objects.all()
    serializer_class = StockOutProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = (
        "report__facility__district__province",
        "report__facility__district",
        "report__facility",
    )


class ProductViewsets(viewsets.ModelViewSet):
    queryset = Dosage.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("dosage", "id")


class CasesPaluViewsets(viewsets.ModelViewSet):
    queryset = (
        CasesPalu.objects.annotate(
            year=Extract("reporting_date", "year"),
            week=Extract("reporting_date", "week"),
        )
        .values("year", "week")
        .annotate(simple=Sum("simple"))
        .annotate(acute=Sum("acute"))
        .annotate(pregnant_women=Sum("pregnant_women"))
        .annotate(decease=Sum("decease"))
        .order_by("year", "week")
    )
    serializer_class = CasesPaluSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = (
        "report__facility__district__province",
        "report__facility__district",
        "report__facility",
    )

    def get_queryset(self):
        startdate = self.request.GET.get("startdate", "")
        enddate = self.request.GET.get("enddate", "")
        if startdate and startdate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__gte=datetime.datetime.strptime(
                    startdate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        if enddate and enddate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__lte=datetime.datetime.strptime(
                    enddate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        return self.queryset


class CasesPaluProvViewsets(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = CasesPaluProvSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class CasesPaluDisViewsets(CasesPaluProvViewsets):
    queryset = District.objects.all()
    serializer_class = CasesPaluDisSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class CasesPaluCdsViewsets(viewsets.ModelViewSet):
    queryset = CDS.objects.all()
    serializer_class = CasesPaluCdsSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("id", "code")


class RateViewsets(viewsets.ModelViewSet):
    queryset = (
        Report.objects.filter(category__in=["SF", "CA", "TS"])
        .annotate(
            year=Extract("reporting_date", "year"),
            week=Extract("reporting_date", "week"),
        )
        .values("year", "week")
        .annotate(nombre=Count("pk"))
        .order_by("week")
    )
    serializer_class = RateSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("facility__district__province", "facility__district", "facility")

    def get_queryset(self):
        startdate = self.request.GET.get("startdate", "")
        enddate = self.request.GET.get("enddate", "")
        if startdate and startdate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__gte=datetime.datetime.strptime(
                    startdate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        if enddate and enddate != "undefined":
            self.queryset = self.queryset.filter(
                reporting_date__week__lte=datetime.datetime.strptime(
                    enddate, "%Y-%m-%d"
                ).isocalendar()[1]
            )
        return self.queryset


class ReportCAViewsets(viewsets.ModelViewSet):
    queryset = Report.objects.filter(category__in=["CA", "TS"])
    serializer_class = ReportSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ("facility__district__province", "facility__district", "facility")


class ReportSTViewsets(ReportCAViewsets):
    queryset = Report.objects.filter(category__in=["SR", "SF", "SD"])


@login_required
def cas_palu(request):
    return render(request, "stock/cas_palu.html")


@login_required
def situation_stock(request):
    return render(request, "stock/situation_stock.html")


@login_required
def show_reports_rp(request):
    return render(request, "stock/situation_stock.html")


@login_required
@csrf_exempt
def CasesPaluExport(request):
    export_cases_palu.delay(user_id=request.user.id)
    return JsonResponse(
        {
            "Ok": "Export started. When the exportation is finished, we will e-mail you the link to download the Excel file. Thanks."
        },
        safe=False,
    )


@csrf_exempt
@login_required
def StockProductExport(request):
    export_stock_product.delay(user_id=request.user.id)
    return JsonResponse(
        {
            "Ok": "Export started. When the exportation is finished, we will e-mail you the link to download the Excel file. Thanks."
        },
        safe=False,
    )
