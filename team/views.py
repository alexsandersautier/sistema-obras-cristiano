from rest_framework import permissions, viewsets
from .models import Team, TeamEmployee
from .serializers import TeamSerializer, TeamEmployeeSerializer, TeamEmployeerSaveSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by("name")
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamEmployeeSaveViewSet(viewsets.ModelViewSet):
    queryset = TeamEmployee.objects.all()
    serializer_class = TeamEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]        

class TeamEmployeeViewSet(viewsets.ModelViewSet):
    queryset = TeamEmployee.objects.all()
    serializer_class = TeamEmployeerSaveSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.request.query_params.get('team', None)
        
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        
        return queryset
    