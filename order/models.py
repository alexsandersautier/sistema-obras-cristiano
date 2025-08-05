from django.db import models
from collections import defaultdict
from django.core.exceptions import ValidationError
from building.models import Building
from service.models import ServicePrice
from team.models import Team

class Order(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='order_building', verbose_name='Obra')
    start_date = models.DateField(verbose_name='Início da obra')

    def clean(self):
        super().clean()
        # Agrupar quantidades por serviço
        service_quantities = defaultdict(float)

        for item in self.orderitem_order.all():  # usa o related_name
            service = item.service_price.service
            service_quantities[service] += item.quantity

        # Validar se ultrapassa o limite
        for service, total_quantity in service_quantities.items():
            if total_quantity > service.max_quantity:
                raise ValidationError(
                    f"A quantidade total do serviço '{service.name}' ({total_quantity}) excede o máximo permitido ({service.max_quantity})."
                )

    def __str__(self):
        return f'Ordem de serviço referente a obra {self.building} iniciada em {self.start_date.strftime('%d/%m/%Y')}'
    
    class Meta:
        verbose_name = 'Ordem de serviço'
        verbose_name_plural = 'Ordens de serviço'    


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem_order', verbose_name='Ordem de serviço')
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='orderitem_service', verbose_name='Serviço')
    quantity = models.FloatField(verbose_name='Quantidade')
    service_data = models.DateField(verbose_name='Data do serviço', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='orderitem_team', verbose_name='Equipe', null=True, blank=True)
    service_data = models.DateField(verbose_name='Data do serviço', null=True, blank=True)
        
    def __str__(self):
        return f'{self.service_price} da ordem de serviço {self.order}'
    
    class Meta:
        verbose_name = 'Item da ordem de serviço'
        verbose_name_plural = 'Itens da orden de serviço' 