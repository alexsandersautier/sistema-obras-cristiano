from django.urls import path
from django.conf.urls.i18n import set_language
from .admin import custom_admin_site as admin_site
from dashboard import views
from django.views.generic import RedirectView
from building import views as v

urlpatterns = [
    path("admin/custom-dashboard/", views.calculos_dashboard, name="custom-dashboard"),
    path('admin/', admin_site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
    path('', RedirectView.as_view(url='/admin/dashboard/fakemodel/dashboard/', permanent=False)),
    path("get-services/<int:building_id>/", v.get_services_by_building, name="get_services_by_building"),
    path('get_service_details/<int:service_price_id>/', v.get_service_details, name='get_service_details'),
]


