from django.conf.urls import url, include
from stock.views import StockProductListView, StockProductViewsets
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'reports', StockProductViewsets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^stock-debut-journnee/$', StockProductListView.as_view(), name='stock-debut-journnee-list'),
]
