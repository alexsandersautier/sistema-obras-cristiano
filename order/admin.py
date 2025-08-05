from django.contrib import admin
from .models import Order,OrderItem
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from collections import defaultdict

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
    
admin.site.register(Order, OrderAdmin)