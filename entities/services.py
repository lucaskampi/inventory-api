from typing import Dict, Any
from django.db import transaction
from .models import Entity

def list_entities(
    name: str = None,
    name_op: str = "contains",
    description: str = None,
    description_op: str = "contains",
    type: str = None,
    type_op: str = "contains",
):
    qs = Entity.objects.all()
    op_map = {
        "equals": "exact",
        "contains": "icontains",
        "startswith": "istartswith",
        "endswith": "iendswith",
    }

    def apply(qs, field, value, op):
        if not value:
            return qs
        if op == "notcontains":
            return qs.exclude(**{f"{field}__icontains": value})
        lookup = op_map.get(op, "icontains")
        return qs.filter(**{f"{field}__{lookup}": value})

    qs = apply(qs, "name", name, name_op)
    qs = apply(qs, "description", description, description_op)
    qs = apply(qs, "type", type, type_op)
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