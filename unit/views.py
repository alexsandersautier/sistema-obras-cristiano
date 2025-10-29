from rest_framework import permissions, viewsets
from .models import Unit
from .serializers import UnitSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by("name")
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]