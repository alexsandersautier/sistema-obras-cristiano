from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', set_language, name='set_language'),
]
