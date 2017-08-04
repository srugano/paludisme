from django.conf.urls import url, include
from stock.views import StockProductViewsets, cas_palu, situation_stock, StockOutProductViewsets, show_reports_rp, ProductViewsets, CasesPaluViewsets, RateViewsets
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'productreportss', StockProductViewsets)
router.register(r'productoutreports', StockOutProductViewsets)
router.register(r'products', ProductViewsets)
router.register(r'casespalus', CasesPaluViewsets)
router.register(r'rates', RateViewsets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^cas_palu/$', cas_palu, name='cas_palu'),
    url(r'^situation_stock/$', situation_stock, name='situation_stock'),
    url(r'^show_reports_rp/$', show_reports_rp, name='show_reports_rp'),
]
