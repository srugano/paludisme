from django.conf.urls import url, include
from stock.views import StockProductViewsets, show_reports_sf, show_reports_sr, StockOutProductViewsets, show_reports_rp, StockProductSFViewsets, StockProductSRViewsets
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'productreports', StockProductViewsets)
router.register(r'productreportssf', StockProductSFViewsets)
router.register(r'productreportssr', StockProductSRViewsets)
router.register(r'productoutreports', StockOutProductViewsets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^show_reports_sf/$', show_reports_sf, name='show_reports_sf'),
    url(r'^show_reports_sr/$', show_reports_sr, name='show_reports_sr'),
    url(r'^show_reports_rp/$', show_reports_rp, name='show_reports_rp'),
]
