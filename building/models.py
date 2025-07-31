from django.db import models
from team.models import Team

# Create your models here.
class Building(models.Model):

    name = models.CharField(verbose_name='Nome', max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='building_team', verbose_name='Equipe')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
