from django.contrib.admin import AdminSite
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import logout

class MyAdminSite(AdminSite):
    site_header = 'SGO'
    site_title = 'SGO Admin'
    index_title = 'Bem-vindo ao painel'

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)
        if request.method == "POST" and request.user.is_authenticated:
            return redirect('/admin/dashboard/fakemodel/dashboard/')  # ou a URL desejada
        return response

    def logout(self, request, extra_context = ...):
        logout(request)
        return redirect('/admin/')
    
custom_admin_site = MyAdminSite(name='custom_admin')

for model, model_admin in admin.site._registry.items():
    custom_admin_site.register(model, model_admin.__class__)
