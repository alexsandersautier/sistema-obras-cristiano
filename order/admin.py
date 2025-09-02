from .models import Order,OrderItem
from .forms import OrderAdminForm
from django.contrib import admin
from .models import Order, OrderItem
from building.models import BuildingService, Building
from service.models import ServicePrice
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Sum

class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        from collections import defaultdict
        
        current_order = self.instance
        building = current_order.building

        service_quantities = defaultdict(float)
        form_map = {}

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                service_price = form.cleaned_data['service_price']
                quantity = form.cleaned_data['quantity']

                service_quantities[service_price] += quantity
                form_map[service_price] = form

        for service_price, new_quantity in service_quantities.items():
            qs = OrderItem.objects.filter(
                order__building=building,
                service_price=service_price
            )

            if current_order.pk:
                qs = qs.exclude(order=current_order)

            total_existing = qs.aggregate(Sum('quantity'))['quantity__sum'] or 0
            total_after_save = total_existing + new_quantity

            try:
                building_service = BuildingService.objects.get(
                    building=building, service_price=service_price
                )
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
                pass


# The problem is here in the inline and admin classes. Let's fix it.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    formset = OrderItemInlineFormSet

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "service_price":
            parent_order = getattr(request, "_parent_object_", None)

            if parent_order and parent_order.building:
                kwargs["queryset"] = ServicePrice.objects.filter(
                    buildingservice_service__building=parent_order.building
                ).distinct()
            else:
                kwargs["queryset"] = ServicePrice.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    form = OrderAdminForm

    class Media:
        js = ("js/order.js",)

    def get_form(self, request, obj=None, **kwargs):
        request._parent_object_ = obj
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        building = form.cleaned_data.get('building')
        if building and not change:
            for item in building.buildingservice_building.all():
                OrderItem.objects.create(
                    order=obj,
                    service_price=item.service_price,
                    quantity=0
                )

admin.site.register(Order, OrderAdmin)