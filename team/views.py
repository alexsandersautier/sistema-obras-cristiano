from django.shortcuts import render
from django.views.generic import ListView
from .models import Team

class TeamListView(ListView):
    
    queryset = Team.objects.all()
    template_name = ''