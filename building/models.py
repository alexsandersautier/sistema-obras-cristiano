from django.db import models
from team.models import Team

# Create your models here.
class Building(models.Model):

    name = models.CharField(verbose_name='Nome', max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'


class BuildingTeam(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='buildingteam_building', verbose_name='Obra')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='buildingteam_team', verbose_name='Equipe')
    
    def __str__(self):
        return f'Equipe {self.team} da obra {self.building}'