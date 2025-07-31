from django.db import models


class Unit(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=255)
    acronym = models.CharField(verbose_name='Sigla', max_length=3)

    def __str__(self):
        return f'{self.name} - {self.acronym}'
    
    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
