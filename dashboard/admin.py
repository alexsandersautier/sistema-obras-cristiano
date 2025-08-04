from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import FakeModel
from django.shortcuts import redirect
from django.urls import reverse

from django.db.models.functions import ExtractYear
from order.models import OrderItem
from building.models import Building
from team.models import Team
from django.db.models import F, FloatField, ExpressionWrapper, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        years = OrderItem.objects.annotate(
            year=ExtractYear('service_data')
        ).values_list(
            'year', flat=True
        ).distinct().order_by('year')

        buildings = Building.objects.filter(
            order_building__orderitem_order__isnull=False
        ).values_list('name', flat=True).distinct().order_by('name')

        teams = Team.objects.all()

        year = request.GET.get('year')  
        month = request.GET.get('month')
        building = request.GET.get('building')
        team = request.GET.get('team')


        orders = OrderItem.objects.select_related('service_price__service')

        # aplicar filtros dinamicamente
        if year and 'Todos' not in year:
            orders = orders.filter(service_data__year=year)
        if month and 'Todos' not in month:
            orders = orders.filter(service_data__month=month)
        if building and 'Todos' not in building:
            orders = orders.filter(order__building__name=building)  # ou .name se você estiver passando o nome
        if team and 'Todos' not in team:
            orders = orders.filter(team__name=team)
        
        orders = orders.annotate(
            total_service=ExpressionWrapper(
                F('service_price__price') * F('quantity'),
                output_field=FloatField()
            )
        )
        
        paginator = Paginator(orders, 10)
        page_number = request.GET.get("page", 1)
        try:
            orders_page = paginator.page(page_number)
        except PageNotAnInteger:
            orders_page = paginator.page(1)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)

        total_geral = sum(item.total_service for item in orders_page)

        MONTHS = [
            ('1', 'Janeiro'),
            ('2', 'Fevereiro'),
            ('3', 'Março'),
            ('4', 'Abril'),
            ('5', 'Maio'),
            ('6', 'Junho'),
            ('7', 'Julho'),
            ('8', 'Agosto'),
            ('9', 'Setembro'),
            ('10', 'Outubro'),
            ('11', 'Novembro'),
            ('12', 'Dezembro'),
        ]

        context = dict(
            self.admin_site.each_context(request),
            title="Dashboard de Cálculos",
            result={
                "buildings": buildings, 
                "orders": orders_page, 
                "years": years, 
                "teams": teams,
            },
            paginator=paginator,
            page_obj=orders_page,
            months=MONTHS,
            total_geral=total_geral,
            selected= {
                "year": year,
                "month": month,
                "building": building,
                "team": team,
            }
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
