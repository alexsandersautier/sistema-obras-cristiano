from django.db import models

class FakeModel(models.Model):
    class Meta:
        managed = False
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"
        app_label = "dashboard"