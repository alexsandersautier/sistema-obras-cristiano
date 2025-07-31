from django.db import models


class Employee(models.Model):
    
    name = models.CharField(verbose_name='Nome', max_length=255)
    document_number = models.CharField(verbose_name='CPF/CNPJ', max_length=20)
    phone_number = models.CharField(verbose_name='Telefone', max_length=11)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'