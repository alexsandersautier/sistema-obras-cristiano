from django.db import models
from building.models import Building
from service.models import ServicePrice

# Create your models here.
class Order(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='order_building', verbose_name='Obra')
    start_date = models.DateField(verbose_name='Início da obra')
    
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
    
    def __str__(self):
        return f'{self.service_price} da ordem de serviço {self.order}'
    
    class Meta:
        verbose_name = 'Item da ordem de serviço'
        verbose_name_plural = 'Itens da orden de serviço' 