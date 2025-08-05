from django.contrib import admin
from .models import Order,OrderItem, OrderTemplate, OrderTemplateItem
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from collections import defaultdict
from .forms import OrderAdminForm, OrderTemplateItemForm

class OrderTemplateItemInline(admin.TabularInline):
    model = OrderTemplateItem
    extra = 1
    form = OrderTemplateItemForm

@admin.register(OrderTemplate)
class OrderTemplateAdmin(admin.ModelAdmin):
    inlines = [OrderTemplateItemInline]
    list_display = ['name']

class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        service_totals = defaultdict(float)

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                service_price = form.cleaned_data['service_price']
                quantity = form.cleaned_data['quantity']
                service = service_price.service
                service_totals[service] += quantity

        for service, total in service_totals.items():
            if total > service.max_quantity:
                raise ValidationError(
                    f"A quantidade total do serviço '{service.name}' ({total}) excede o máximo permitido ({service.max_quantity})."
                )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    formset = OrderItemInlineFormSet


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    form = OrderAdminForm
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        template = form.cleaned_data.get('template')
        if template and not change:  # Só popula ao criar, não ao editar

            for item in template.items.all():
                OrderItem.objects.create(
                    order=obj,
                    service_price=item.service_price,
                    quantity=item.quantity
                )
    
admin.site.register(Order, OrderAdmin)