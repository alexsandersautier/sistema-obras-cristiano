from rest_framework import serializers
from .models import Team, TeamEmployee
from employee.serializers import EmployeeSerializer

class TeamEmployeerSaveSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='employee.name', read_only=True)
    class Meta:
        model = TeamEmployee
        fields = ['id', 'name',]

class TeamEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEmployee
        fields = ["id", "employee", "team"]


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ["id", "name"]