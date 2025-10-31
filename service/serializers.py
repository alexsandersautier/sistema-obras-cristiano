from rest_framework import serializers
from . import models

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'

class ServicePriceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='unit.name', read_only=True)
    class Meta:
        model = models.ServicePrice
        fields = ['id', 'price', 'service', 'unit', 'name']