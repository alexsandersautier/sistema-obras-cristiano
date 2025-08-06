from django.contrib import admin
from .models import Building, BuildingTeam, BuildingService, TemplateBuildingService, Template
from .forms import BuildingFormAdmin

class TemplateItem(admin.TabularInline):
    model = TemplateBuildingService
    extra = 0
    
class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateItem]

admin.site.register(Template, TemplateAdmin)

class BuildingTeamInline(admin.TabularInline):
    model = BuildingTeam
    extra = 0

class BuildingServiceInline(admin.TabularInline):
    model = BuildingService
    extra = 0
class BuildingAdmin(admin.ModelAdmin):
    inlines = [BuildingTeamInline, BuildingServiceInline]
    form = BuildingFormAdmin
    
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
