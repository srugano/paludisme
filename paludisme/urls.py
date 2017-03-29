from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from paludisme.views import home, settings, password, add_report


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^stock/', include('stock.urls')),
    url(r'^add/', add_report, name="add-report"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', settings, name='settings'),
    url(r'^settings/password/$', password, name='password'),
]
