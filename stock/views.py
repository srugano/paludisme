from django.views.generic import ListView
from stock.models import StockProduct
from rest_framework import viewsets
from stock.serializers import StockProductSerializer


class StockProductViewsets(viewsets.ModelViewSet):
    queryset = StockProduct.objects.all()
    serializer_class = StockProductSerializer


class StockProductListView(ListView):
    model = StockProduct
    paginate_by = 25
    context_object_name = 'produits'

