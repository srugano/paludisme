from django.conf.urls import url
from stock.views import StockProductListView


urlpatterns = [
    url(r'^$', StockProductListView.as_view(), name='stock-debut-journnee-list'),
]
