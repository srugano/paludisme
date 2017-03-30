from django.views.generic import ListView
from stock.models import StockProduct, Product
from rest_framework import viewsets
from stock.serializers import StockProductSerializer


class StockProductViewsets(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockProductSerializer


class StockProductListView(ListView):
    model = StockProduct
    paginate_by = 25
    context_object_name = 'produits'


def create_stockproduct(report=None, product=None):
    products = [m.code for m in Product.objects.all().distinct()]
    if product.code in products:
        values = report.text.split(" ")[3:]
        dosages = product.dosages.all()
        for dose in dosages:
            sp = StockProduct.objects.create(product=product, report=report, dosage=dose, quantity=values[dose.rank])
            sp.save()


def update_stockproduct(report=None, product=None):
    values = report.text.split(" ")[3:]
    dosages = product.dosages.all()
    for dose in dosages:
        sp = StockProduct.objects.get(product=product, report=report, dosage=dose)
        sp.quantity = values[dose.rank]
        sp.save()
