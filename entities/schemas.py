from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class EntityBase(BaseModel):
    type: constr(max_length=100)
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None

    model_config = {"from_attributes": True}

class EntityCreate(EntityBase):
    pass

class EntityUpdate(BaseModel):
    type: Optional[constr(max_length=100)] = None
    name: Optional[constr(max_length=255)] = None
    description: Optional[str] = None

    model_config = {"from_attributes": True}

class EntityOut(EntityBase):
    id: int
    created_at: datetime