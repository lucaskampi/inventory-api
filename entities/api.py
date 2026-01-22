from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import transaction

from .models import Entity
from .schemas import EntityCreate, EntityOut, EntityUpdate
from . import services

router = Router()

@router.get("/entities", response=List[EntityOut])
def list_entities(request):
    qs = services.list_entities()
    return list(qs)

@router.get("/entities/{entity_id}", response=EntityOut)
def get_entity(request, entity_id: int):
    try:
        obj = services.get_entity(entity_id)
    except Entity.DoesNotExist:
        raise Http404("Entity not found")
    return obj

@router.post("/entities", response={201: EntityOut})
def create_entity(request, payload: EntityCreate):
    obj = services.create_entity(payload.model_dump())
    return 201, obj

@router.put("/entities/{entity_id}", response=EntityOut)
def update_entity(request, entity_id: int, payload: EntityUpdate):
    try:
        data = payload.model_dump(exclude_none=True)
        obj = services.update_entity(entity_id, data)
    except Entity.DoesNotExist:
        raise Http404("Entity not found")
    return obj

@router.delete("/entities/{entity_id}", response={204: None})
def delete_entity(request, entity_id: int):
    try:
        services.delete_entity(entity_id)
    except Entity.DoesNotExist:
        raise Http404("Entity not found")
    return 204, None