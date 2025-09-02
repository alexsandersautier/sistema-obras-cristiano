from django.http import JsonResponse
from building.models import BuildingService
from .models import ServicePrice
from django.shortcuts import get_object_or_404

def get_service_details(request, service_price_id):
    service_price = get_object_or_404(ServicePrice, pk=service_price_id)
    data = {
        'max_quantity': service_price.service.max_quantity,
        'unit_price': float(service_price.price)
    }
    return JsonResponse(data)

def get_services_by_building(request, building_id):
    services = BuildingService.objects.filter(building_id=building_id).select_related("service_price")
    data = [
        {"id": bs.service_price.id, "text": str(bs.service_price)}
        for bs in services
    ]
    return JsonResponse(data, safe=False)


def get_info_service(request, service_id):
    ...