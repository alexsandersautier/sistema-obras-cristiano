from django.contrib import admin
from .models import Building, BuildingTeam
# Register your models here.

class BuildingTeamInline(admin.TabularInline):
    model = BuildingTeam
    extra = 1

class BuildingAdmin(admin.ModelAdmin):
    inlines = [BuildingTeamInline]


admin.site.register(Building, BuildingAdmin)
