from django.db import models
from building.models import Building

# Create your models here.
class Order(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='order_building', verbose_name='Obra')
    start_date = models.DateField()
    
    def __str__(self):
        return f'Ordem de serviço referente a obra {self.building}'
    
    class Meta:
        verbose_name = 'Ordem de serviço'
        verbose_name_plural = 'Ordens de serviço'    
