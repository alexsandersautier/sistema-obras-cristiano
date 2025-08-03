from django.urls import path
from django.conf.urls.i18n import set_language
from .admin import custom_admin_site as admin_site
from dashboard import views

urlpatterns = [
    path("admin/custom-dashboard/", views.calculos_dashboard, name="custom-dashboard"),
    path('admin/', admin_site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
]


