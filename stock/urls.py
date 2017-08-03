from django.conf.urls import url, include
from stock.views import StockProductViewsets, show_reports_sf, show_reports_sr, StockOutProductViewsets, show_reports_rp, ProductViewsets, CasesPaluViewsets, RateViewsets
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'productreportss', StockProductViewsets)
router.register(r'productoutreports', StockOutProductViewsets)
router.register(r'products', ProductViewsets)
router.register(r'casespalus', CasesPaluViewsets)
router.register(r'rates', RateViewsets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^show_reports_sf/$', show_reports_sf, name='show_reports_sf'),
    url(r'^show_reports_sr/$', show_reports_sr, name='show_reports_sr'),
    url(r'^show_reports_rp/$', show_reports_rp, name='show_reports_rp'),
]
