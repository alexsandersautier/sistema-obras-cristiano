from django.db import models
from unit.models import Unit


class Service(models.Model):
    
    name = models.CharField(verbose_name='Nome', max_length=255)
    max_quantity = models.FloatField(default=0)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'


class ServicePrice(models.Model):
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='serviceprice_service', verbose_name='Serviço')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='serviceprice_unit', verbose_name='Unidade')
    price = models.DecimalField(verbose_name='Preço', decimal_places=2, max_digits=6)
    
    def __str__(self):
        return f'{self.service} no valor de {self.price} por {self.unit.acronym}'
    
    class Meta:
        verbose_name = 'Preço de serviços por unidade'
        verbose_name_plural = 'Preços de serviços por unidade'
