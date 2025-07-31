from django.contrib import admin
from .models import Service, ServicePrice
    
class ServicoPriceInline(admin.TabularInline):
    model = ServicePrice
    extra = 1 

class ServicoAdmin(admin.ModelAdmin):
    inlines = [ServicoPriceInline]

admin.site.register(Service, ServicoAdmin)
