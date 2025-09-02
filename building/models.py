from django.db import models
from team.models import Team
from service.models import ServicePrice

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
    
    class Meta:
        verbose_name = 'Equipe da obra'
        verbose_name_plural = 'Equipes da obra'
        
class BuildingService(models.Model):
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='buildingservice_building', verbose_name='Obra')
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='buildingservice_service', verbose_name='Serviço')
    quantity = models.FloatField(verbose_name='Quantidade')
    
    def __str__(self):
        return f'Serviço {self.service_price.service.name} para a obra {self.building.name} na quantidade de {self.quantity}'
    
    class Meta:
        verbose_name = 'Serviço da obra'
        verbose_name_plural = 'Serviços da obra'


class Template(models.Model):
    
    name = models.CharField(verbose_name='Nome', max_length=20)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

class TemplateBuildingService(models.Model):
    
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='templatebuildingservice_template', verbose_name='Template', null=True, blank=True)
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='templatebuildingservice_service', verbose_name='Serviço')
    quantity = models.FloatField(verbose_name='Quantidade')
    
    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'