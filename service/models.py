from django.db import models


class Service(models.Model):
    
    name = models.CharField(verbose_name='Nome', max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'