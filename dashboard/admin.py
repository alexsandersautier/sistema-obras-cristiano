from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import FakeModel

from django.shortcuts import redirect
from django.urls import reverse

@admin.register(FakeModel)
class CustomDashboardAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_site.admin_view(self.dashboard_view),
                name="custom-dashboard",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        # Redireciona para a URL custom ao invés da lista padrão do model
        return redirect(reverse("admin:custom-dashboard"))

    def dashboard_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="Dashboard de Cálculos",
            resultado={"soma": 123, "media": 456},
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
