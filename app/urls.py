from django.urls import path
from django.conf.urls.i18n import set_language
from .admin import custom_admin_site as admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
]


