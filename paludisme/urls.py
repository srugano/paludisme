from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from paludisme.views import settings, password, add_report, add_reporter, confirm_reporter, add_stockout, HomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^bdiadmin/', include('bdiadmin.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^stock/', include('stock.urls')),
    url(r'^add_report/', add_report, name="add-report"),
    url(r'^add_reporter/', add_reporter, name="add-reporter"),
    url(r'^add_stockoutr/', add_stockout, name="add-stockout"),
    url(r'^confirm_reporter/', confirm_reporter, name="confirm_reporter"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', settings, name='settings'),
    url(r'^settings/password/$', password, name='password'),
]
