from django.contrib import admin
from .models import Team, TeamEmployee

class EmployeeInline(admin.TabularInline):
    model = TeamEmployee
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    inlines = [EmployeeInline]
    
admin.site.register(Team, TeamAdmin)
