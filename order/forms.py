from django import forms
from .models import Order, OrderTemplateItem

class OrderAdminForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'


class OrderTemplateItemForm(forms.ModelForm):
    class Meta:
        model = OrderTemplateItem
        fields = "__all__"

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        service_price = self.cleaned_data.get('service_price')

        if service_price:
            max_quantity = service_price.service.max_quantity
            if quantity > max_quantity:
                raise forms.ValidationError(
                    f"A quantidade máxima permitida para este serviço é {max_quantity}."
                )
        return quantity