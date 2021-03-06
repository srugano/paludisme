from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from paludisme.views import (
    password,
    add_report,
    add_reporter,
    confirm_reporter,
    add_stockout,
    home,
    landing,
)
from stock.utils import export_to_excel
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^stock/", include("stock.urls")),
    url(r"^add_report/", add_report, name="add-report"),
    url(r"^add_reporter/", add_reporter, name="add-reporter"),
    url(r"^add_stockoutr/", add_stockout, name="add-stockout"),
    url(r"^confirm_reporter/", confirm_reporter, name="confirm_reporter"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r"^explorer/", include("explorer.urls")),
    url(r"^bdiadmin/", include("bdiadmin.urls")),
    url(r"^login/$", auth_views.login, name="login"),
    url(r"^logout/$", auth_views.logout, {"next_page": "/"}, name="logout"),
    url(r"^oauth/", include("social_django.urls", namespace="social")),
    url(r"^settings/password/$", password, name="password"),
    url(r"^export/xlsx/$", export_to_excel, name="export_to_excel"),
    url(r"^home/$", home, name="home"),
    url(r"^$", landing, name="landing"),
)
