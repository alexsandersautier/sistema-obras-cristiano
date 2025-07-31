from django.db import models
from employee.models import Employee


class Team(models.Model):

    name = models.CharField(verbose_name='Nome', max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'


class TeamEmployee(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='team_employee_employee', verbose_name='Funcionário')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_employee_team', verbose_name='Equipe')
    
    def __str__(self):
        return f'Funcionário {self.employee} da equipe {self.team}'
    
    class Meta:
        verbose_name = 'Funcionário da equipe'
        verbose_name_plural = 'Funcionários da equipe'