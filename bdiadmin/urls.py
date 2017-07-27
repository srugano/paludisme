from django.conf.urls import url, include
from bdiadmin.views import DistrictViewSet, ProvinceViewSet, ProfileUserListView, CDSViewSet, ProfileUserCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'province', ProvinceViewSet)
router.register(r'district', DistrictViewSet)
router.register(r'cds', CDSViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^profile/$', ProfileUserListView.as_view(), name='profile'),
    url(r'^profile/create/$', ProfileUserCreateView.as_view(), name='profile_create'),
]