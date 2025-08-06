from django.contrib import admin
from .models import Order,OrderItem
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from collections import defaultdict
from .forms import OrderAdminForm

class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        from collections import defaultdict
        from django.core.exceptions import ValidationError
        from django.forms.utils import ErrorList
        from django.db.models import Sum
        from building.models import BuildingService

        current_order = self.instance
        building = current_order.building

        # Agrupar novas quantidades por service_price
        service_quantities = defaultdict(float)
        form_map = {}

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                service_price = form.cleaned_data['service_price']
                quantity = form.cleaned_data['quantity']

                service_quantities[service_price] += quantity
                # Guardar referência para mostrar erro no formulário correto
                form_map[service_price] = form

        for service_price, new_quantity in service_quantities.items():
            # Soma das quantidades anteriores (de outras ordens da mesma obra)
            total_existing = (
                OrderItem.objects.filter(
                    order__building=building,
                    service_price=service_price
                )
                .exclude(order=current_order)  # Exclui a ordem atual (em caso de edição)
                .aggregate(Sum('quantity'))['quantity__sum'] or 0
            )

            # Soma total com os dados do formulário atual
            total_after_save = total_existing + new_quantity

            # Verifica se há quantidade prevista para esse serviço na obra
            try:
                building_service = BuildingService.objects.get(building=building, service_price=service_price)
                max_quantity = building_service.quantity

                if total_after_save > max_quantity:
                    form = form_map[service_price]
                    form.add_error(
                        'quantity',
                        ValidationError(
                            f"A quantidade total para o serviço '{service_price}' excede o permitido na obra "
                            f"({total_after_save} > {max_quantity})."
                        )
                    )
            except BuildingService.DoesNotExist:
                # Se não estiver vinculado na obra, não valida — como você pediu
                pass

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    formset = OrderItemInlineFormSet


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    form = OrderAdminForm
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        building = form.cleaned_data.get('building')
        if building and not change:  # Só popula ao criar, não ao editar
            print(building)
            for item in building.buildingservice_building.all():
                OrderItem.objects.create(
                    order=obj,
                    service_price=item.service_price,
                    quantity=0
                )
    
admin.site.register(Order, OrderAdmin)