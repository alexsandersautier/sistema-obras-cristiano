from rest_framework import permissions, viewsets
from .models import Service, ServicePrice
from .serializers import ServiceSerializer, ServicePriceSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by("name")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServicePriceViewSet(viewsets.ModelViewSet):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service',]
