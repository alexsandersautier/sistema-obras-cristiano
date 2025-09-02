from django.http import JsonResponse
from building.models import BuildingService

def get_services_by_building(request, building_id):
    services = BuildingService.objects.filter(building_id=building_id).select_related("service_price")
    data = [
        {"id": bs.service_price.id, "text": str(bs.service_price)}
        for bs in services
    ]
    return JsonResponse(data, safe=False)