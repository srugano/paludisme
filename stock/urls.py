from django.conf.urls import url, include
from stock.views import StockProductSFViewsets, cas_palu, situation_stock, StockOutProductViewsets, show_reports_rp, ProductViewsets, CasesPaluViewsets, RateViewsets, CasesPaluProvViewsets, CasesPaluDisViewsets, CasesPaluCdsViewsets, StockProductProvViewsets, StockProductDisViewsets, StockProductCDSViewsets, ReportCAViewsets, ReportSTViewsets, CasesPaluExport, StockProductExport
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'reportsCA', ReportCAViewsets)
router.register(r'reportsST', ReportSTViewsets)
router.register(r'stockfinal', StockProductSFViewsets)
router.register(r'stockfinalprov', StockProductProvViewsets)
router.register(r'stockfinaldis', StockProductDisViewsets)
router.register(r'stockfinalcds', StockProductCDSViewsets)
router.register(r'productoutreports', StockOutProductViewsets)
router.register(r'products', ProductViewsets)
router.register(r'casespalusProv', CasesPaluProvViewsets)
router.register(r'casespalusDis', CasesPaluDisViewsets)
router.register(r'casespalusCds', CasesPaluCdsViewsets)
router.register(r'casespalus', CasesPaluViewsets)
router.register(r'rates', RateViewsets)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^cas_palu/$', cas_palu, name='cas_palu'),
    url(r'^situation_stock/$', situation_stock, name='situation_stock'),
    url(r'^show_reports_rp/$', show_reports_rp, name='show_reports_rp'),
    url(r'^casepaluexport/$', CasesPaluExport.as_view(), name='casepaluexport'),
    url(r'^stockproductexport/$', StockProductExport.as_view(), name='stockproductexport'),
]
