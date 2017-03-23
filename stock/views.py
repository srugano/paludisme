from django.views.generic import ListView
from stock.models import StockProduct


class StockProductListView(ListView):
    model = StockProduct
    paginate_by = 25
    context_object_name = 'produits'

