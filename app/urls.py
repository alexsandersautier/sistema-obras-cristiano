from django.urls import path, include
from django.conf.urls.i18n import set_language
from .admin import custom_admin_site as admin_site
from dashboard import views
from django.views.generic import RedirectView
from building import views as v
from rest_framework import routers

from unit import views as unit_views
from . import views as user_views

router = routers.DefaultRouter()
router.register(r"units", unit_views.UnitViewSet)
router.register(r"users", user_views.UserInfoViewSet, basename="user-info")

urlpatterns = [
    path("admin/custom-dashboard/", views.calculos_dashboard, name="custom-dashboard"),
    path('admin/', admin_site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    path('', RedirectView.as_view(url='/admin/dashboard/fakemodel/dashboard/', permanent=False)),
    path("get-services/<int:building_id>/", v.get_services_by_building, name="get_services_by_building"),
    path('get_service_details/<int:service_price_id>/', v.get_service_details, name='get_service_details'),
    path('', include(router.urls))
]


