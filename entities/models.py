from django.db import models

class Entity(models.Model):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.name or self.pk}"