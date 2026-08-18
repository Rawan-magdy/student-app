from django.contrib import admin
from .models import ResourceType, Resource


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'resource_type', 'created_at')
    list_filter = ('resource_type',)
    search_fields = ('title', 'description')