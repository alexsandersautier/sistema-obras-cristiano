from django.contrib import admin
from django.utils.formats import localize
from .models import Service, ServicePrice

class ServicoPriceInline(admin.TabularInline):
    model = ServicePrice
    extra = 1 

class ServicoAdmin(admin.ModelAdmin):
    inlines = [ServicoPriceInline]
    list_display = ("id", "name", "max_quantity", "listar_unit", "listar_prices")

    def listar_prices(self, obj):
        return ", ".join([localize(p.price) for p in obj.serviceprice_service.all()])
    listar_prices.short_description = "Preços"

    def listar_unit(self, obj):
        return ", ".join([str(p.unit) for p in obj.serviceprice_service.all()])
    listar_unit.short_description = "Unid."

admin.site.register(Service, ServicoAdmin)
