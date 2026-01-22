import pytest

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_entity_str_representation():
    obj = services.create_entity({"type": "mytype", "name": "myname"})
    s = str(obj)
    assert "mytype" in s
    assert "myname" in s
