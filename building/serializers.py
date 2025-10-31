from decimal import Decimal
from rest_framework import serializers
from . import models

class BuildingSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Building
        fields = ['id', 'name', 'total']
    
    def get_total(self, obj):
        """
        Calcula o total da obra somando (service_price * quantity) 
        de todos os BuildingService relacionados
        """
        building_services = models.BuildingService.objects.filter(building=obj)
        
        total = sum(
            bs.service_price.price * Decimal(str(bs.quantity))
            for bs in building_services
        )
        
        return total


class BuildingTeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='team.name', read_only=True)
    class Meta:
        model = models.BuildingTeam
        fields = ['id', 'building', 'team', 'name']


class BuildingServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='service_price.service.name', read_only=True)
    class Meta:
        model = models.BuildingService
        fields = ['id', 'building', 'service_price', 'name']

# class ServicePriceSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='unit.name', read_only=True)
#     class Meta:
#         model = models.ServicePrice
#         fields = ['id', 'price', 'service', 'unit', 'name']