from django.db import models
from django.contrib.auth.models import User


class ResourceType(models.Model):
    name = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.name


class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.SET_NULL, null=True, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title