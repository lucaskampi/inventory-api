from typing import Dict, Any
from django.db import transaction
from .models import Entity

def list_entities(name: str = None, description: str = None, type: str = None):
    qs = Entity.objects.all()
    if name:
        qs = qs.filter(name__icontains=name)
    if description:
        qs = qs.filter(description__icontains=description)
    if type:
        qs = qs.filter(type__icontains=type)
    return qs.order_by("-created_at")

def get_entity(entity_id: int) -> Entity:
    return Entity.objects.get(pk=entity_id)

def create_entity(data: Dict[str, Any]) -> Entity:
    with transaction.atomic():
        return Entity.objects.create(**data)

def update_entity(entity_id: int, data: Dict[str, Any]) -> Entity:
    with transaction.atomic():
        obj = Entity.objects.get(pk=entity_id)
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return obj

def delete_entity(entity_id: int) -> None:
    obj = Entity.objects.get(pk=entity_id)
    obj.delete()