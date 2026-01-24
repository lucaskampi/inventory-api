from typing import Dict, Any
from django.db import transaction
from .models import Entity
from decimal import Decimal, InvalidOperation, ROUND_DOWN

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
        if value is None:
            return qs
        # treat empty string as no-filter
        if isinstance(value, str) and value.strip() == "":
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
    # accept `unit_price` (e.g. 50.99) and store as Decimal with 4 decimal places
    unit = data.pop('unit_price', None)
    if unit is not None:
        # accept both 50.99 and '50,99' by normalizing comma to dot
        unit_str = str(unit).replace(',', '.').strip()
        # treat empty string as no-value
        if unit_str == "":
            unit = None
        else:
            try:
                d = Decimal(unit_str)
            except (InvalidOperation, ValueError):
                d = Decimal(float(unit_str))
            # store with 4 decimal places to preserve measurement precision, truncate (ROUND_DOWN)
            data['unit_price'] = d.quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
    with transaction.atomic():
        return Entity.objects.create(**data)

def update_entity(entity_id: int, data: Dict[str, Any]) -> Entity:
    with transaction.atomic():
        # support updating via `unit_price` as well
        unit = data.pop('unit_price', None)
        if unit is not None:
            unit_str = str(unit).replace(',', '.').strip()
            if unit_str == "":
                unit = None
            else:
                try:
                    d = Decimal(unit_str)
                except (InvalidOperation, ValueError):
                    d = Decimal(float(unit_str))
                data['unit_price'] = d.quantize(Decimal('0.0001'), rounding=ROUND_DOWN)

        obj = Entity.objects.get(pk=entity_id)
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return obj

def delete_entity(entity_id: int) -> None:
    obj = Entity.objects.get(pk=entity_id)
    obj.delete()