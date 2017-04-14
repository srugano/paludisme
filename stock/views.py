from stock.models import StockProduct, Product, StockOutReport
from rest_framework import viewsets
import django_filters
from stock.serializers import StockProductSerializer, StockOutProductSerializer
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


class StockOutProductViewsets(viewsets.ModelViewSet):
    queryset = StockOutReport.objects.all()
    serializer_class = StockOutProductSerializer


@login_required
def show_reports_sf(request):
    return render(request, "stock/sf.html")


@login_required
def show_reports_sr(request):
    return render(request, "stock/sr.html")


@login_required
def show_reports_rp(request):
    return render(request, "stock/rp.html")


def create_stockproduct(report=None, product=None, *args, **kwargs):
    products = [m.code for m in Product.objects.all().distinct()]
    if product.code in products:
        values = report.text.split(" ")[3:]
        if report.text.split(" ")[0] in ["RP"]:
            st = StockOutReport.objects.create(product=product, report=report, remaining=values[0])
            st.save()  
            return "Kuri {0}, handitswe ko hasigaye {1}, za {2} kw'itariki {3}. Murakoze".format(report.facility, values[0], product.designation, st.reporting_date)
        else:
            message = ""
            dosages = product.dosages.all()
            for dose in dosages:
                sp = StockProduct.objects.create(product=product, report=report, dosage=dose, quantity=values[dose.rank])
                sp.save()
                message += sp.quantity + " (" + dose.dosage + "), "
            return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)


def update_stockproduct(report=None, product=None, *args, **kwargs):
    values = report.text.split(" ")[3:]
    if report.text.split(" ")[0] in ["RP"]:
            st, created = StockOutReport.objects.get_or_create(product=product, report=report)
            st.remaining = values[0]
            st.save()
            return "Kuri {0}, handitswe ko hasigaye {1} za {2} kw'itariki {3}. Murakoze.".format(report.facility, values[0], product.designation, st.reporting_date)
    else:
        dosages = product.dosages.all()
        message = ""
        for dose in dosages:
            sp, created = StockProduct.objects.get_or_create(product=product, report=report, dosage=dose)
            sp.quantity = values[dose.rank]
            sp.save()
            message += sp.quantity + " (" + dose.dosage + "), "

        return "Kuri {0}, handitswe kuri {2}, {1} murakoze".format(report.facility, message, product.designation)
