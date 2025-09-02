from django.db import models
from building.models import Building
from service.models import ServicePrice
from team.models import Team
from django.core.exceptions import ValidationError

class Order(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='order_building', verbose_name='Obra')
    start_date = models.DateField(verbose_name='Início da obra')

    def __str__(self):
        return f"Ordem de serviço referente a obra {self.building} iniciada em {self.start_date.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = 'Ordem de serviço'
        verbose_name_plural = 'Ordens de serviço'    


class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem_order', verbose_name='Ordem de serviço')
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='orderitem_service', verbose_name='Serviço')
    quantity = models.FloatField(verbose_name='Quantidade')
    service_data = models.DateField(verbose_name='Data do serviço', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='orderitem_team', verbose_name='Equipe', null=True, blank=True)
        
    def __str__(self):
        return f'{self.service_price} da ordem de serviço {self.order}'
    
    def clean(self):
        super().clean()
        if self.service_data and self.order and self.order.start_date:
            if self.service_data < self.order.start_date:
                raise ValidationError({
                    'service_data': f'A data do serviço ({self.service_data.strftime("%d/%m/%Y")}) não pode ser anterior à data de início da obra ({self.order.start_date.strftime("%d/%m/%Y")}).'
                })
    class Meta:
        verbose_name = 'Item da ordem de serviço'
        verbose_name_plural = 'Itens da orden de serviço' 

class OrderTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do Template")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Template de Ordem"
        verbose_name_plural = "Templates de Ordem"
        
class OrderTemplateItem(models.Model):
    template = models.ForeignKey(OrderTemplate, on_delete=models.CASCADE, related_name="items")
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.service_price} ({self.quantity})"

    class Meta:
        verbose_name = "Serviço do Template"
        verbose_name_plural = "Serviços do Template"
        
