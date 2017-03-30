from stock.models import StockProduct, Product
from rest_framework import viewsets
import django_filters
from stock.serializers import StockProductSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class StockProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(name="report", lookup_expr='category')

    class Meta:
        model = StockProduct
        fields = ['dosage', 'product', 'report', 'category']


class StockProductViewsets(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = StockProductFilter


@login_required
def show_reports_sf(request):
    return render(request, "stock/sf.html")


@login_required
def show_reports_sr(request):
    return render(request, "stock/sr.html")


def create_stockproduct(report=None, product=None):
    products = [m.code for m in Product.objects.all().distinct()]
    message = ""
    if product.code in products:
        values = report.text.split(" ")[3:]
        dosages = product.dosages.all()
        for dose in dosages:
            sp = StockProduct.objects.create(product=product, report=report, dosage=dose, quantity=values[dose.rank])
            sp.save()
            message += sp.quantity + " (" + dose.dosage + "), "
    return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)


def update_stockproduct(report=None, product=None):
    values = report.text.split(" ")[3:]
    dosages = product.dosages.all()
    message = ""
    for dose in dosages:
        sp, created = StockProduct.objects.get_or_create(product=product, report=report, dosage=dose)
        sp.quantity = values[dose.rank]
        sp.save()
        message += sp.quantity + " (" + dose.dosage + "), "

    return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)
