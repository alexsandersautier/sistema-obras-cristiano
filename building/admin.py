from django.contrib import admin
from django.utils.formats import localize
from .models import Building, BuildingTeam, BuildingService, TemplateBuildingService, Template
from .forms import BuildingFormAdmin
from decimal import Decimal


from django.contrib import admin
from django.utils.formats import localize
from .models import TemplateBuildingService
from decimal import Decimal

class TemplateItem(admin.TabularInline):
    model = TemplateBuildingService
    extra = 0
    # Keep these fields in readonly_fields
    readonly_fields = ['display_max_quantity', 'display_unit_price', 'display_total']
    
    # And include them in the fields list to be displayed
    fields = ['service_price', 'quantity', 'display_max_quantity', 'display_unit_price', 'display_total']

    class Media:
        js = ('js/template.js', ) # Assuming your JS file handles the dynamic update

    def display_max_quantity(self, obj):
        # Your method logic remains the same
        if obj.service_price and obj.service_price.service and obj.service_price.service.max_quantity is not None:
            value = f"{obj.service_price.service.max_quantity:.2f}"
            return value.replace('.', ',')
        return "-"
    
    display_max_quantity.short_description = "Quantidade Máxima"

    def display_unit_price(self, obj):
        # Your method logic remains the same
        if obj.service_price and obj.service_price.price is not None:
            return f"{localize(obj.service_price.price)}"
        return "-"
    
    display_unit_price.short_description = 'Preço Unitário'

    def display_total(self, obj):
        if obj.quantity is None or obj.service_price is None or obj.service_price.price is None:
            return "-"
        try:
            total = Decimal(obj.quantity) * obj.service_price.price
            return f"{localize(total)}"
        except (TypeError, ValueError):
            return "-"
    
    display_total.short_description = "Total"

class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateItem]
    readonly_fields = ['total_price_summary']
    fields = ['name', 'total_price_summary']

    def total_price_summary(self, obj):
        if obj:
            total = sum(Decimal(item.quantity) * item.service_price.price for item in obj.templatebuildingservice_template.all() if item.quantity and item.service_price)
            return f"{localize(total)}"
        return "0,00"
    total_price_summary.short_description = "Total do Template"

admin.site.register(Template, TemplateAdmin)

class BuildingTeamInline(admin.TabularInline):
    model = BuildingTeam
    extra = 0

class BuildingServiceInline(admin.TabularInline):
    model = BuildingService
    extra = 0
    fields = ('service_price', 'quantity', 'display_unit_price', 'display_total')
    readonly_fields = ('display_unit_price', 'display_total')
    
    class Media:
        js = ('js/template.js', )

    def display_unit_price(self, obj):
        # Your method logic remains the same
        if obj.service_price and obj.service_price.price is not None:
            return f"{localize(obj.service_price.price)}"
        return "-"
    
    display_unit_price.short_description = 'Preço Unitário'

    def display_total(self, obj):
        if obj.quantity is None or obj.service_price is None or obj.service_price.price is None:
            return "-"
        try:
            total = Decimal(obj.quantity) * obj.service_price.price
            return f"{localize(total)}"
        except (TypeError, ValueError):
            return "-"
    
    display_total.short_description = "Total"

class BuildingAdmin(admin.ModelAdmin):
    inlines = [BuildingTeamInline, BuildingServiceInline]
    form = BuildingFormAdmin
    
    readonly_fields = ['total_price_summary']
    list_display = ('name', 'total_price_summary')
    fields = ['name', 'template', 'total_price_summary']
    ordering = ('name',)

    def total_price_summary(self, obj):
        if obj:
            total = sum(Decimal(item.quantity) * item.service_price.price for item in obj.buildingservice_building.all() if item.quantity and item.service_price)
            return f"{localize(total)}"
        return "0,00"
    
    total_price_summary.short_description = "Total da Obra"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        template = form.cleaned_data.get('template')
        if template and not change:  # Só popula ao criar, não ao editar
            print(template)
            for item in template.templatebuildingservice_template.all():
                BuildingService.objects.create(
                    building=obj,
                    service_price=item.service_price,
                    quantity=item.quantity
                )

admin.site.register(Building, BuildingAdmin)
