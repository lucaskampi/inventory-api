from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime
from decimal import Decimal

class EntityBase(BaseModel):
    type: constr(max_length=100)
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    # store and accept unit_price with Decimal precision; API accepts float/str and will be parsed
    unit_price: Optional[Decimal] = None

    model_config = {"from_attributes": True}

class EntityCreate(EntityBase):
    pass

class EntityUpdate(BaseModel):
    type: Optional[constr(max_length=100)] = None
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    unit_price: Optional[Decimal] = None

    model_config = {"from_attributes": True}

class EntityOut(EntityBase):
    id: int
    created_at: datetime
    # unit_price returned as Decimal (serialized by Pydantic)
    unit_price: Decimal