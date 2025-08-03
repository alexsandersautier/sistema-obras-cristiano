from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@admin.site.admin_view
def calculos_dashboard(request):
    resultado = {"soma": 123, "media": 456}
    return render(request, "admin/custom_dashboard.html", {
        "resultado": resultado,
        "title": "Relatórios"
    })