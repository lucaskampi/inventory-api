from typing import List, Tuple
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Entity
from .schemas import EntityCreate, EntityOut, EntityUpdate, EntityBase

router = Router()

@router.get("/entities", response=List[EntityOut])
def list_entities(request):
    qs = Entity.objects.all().order_by("-created_at")
    return list(qs)

@router.get("/entities/{entity_id}", response=EntityOut)
def get_entity(request, entity_id: int):
    obj = get_object_or_404(Entity, pk=entity_id)
    return obj

@router.post("/entities", response={201: EntityOut})
def create_entity(request, payload: EntityCreate):
    with transaction.atomic():
        obj = Entity.objects.create(**payload.model_dump())
    return 201, obj

@router.put("/entities/{entity_id}", response=EntityOut)
def update_entity(request, entity_id: int, payload: EntityUpdate):
    obj = get_object_or_404(Entity, pk=entity_id)
    data = payload.model_dump(exclude_none=True)
    for field, value in data.items():
        setattr(obj, field, value)
    obj.save()
    return obj

@router.delete("/entities/{entity_id}", response={204: None})
def delete_entity(request, entity_id: int):
    obj = get_object_or_404(Entity, pk=entity_id)
    obj.delete()
    return 204, None