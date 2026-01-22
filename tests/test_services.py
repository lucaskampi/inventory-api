import pytest

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_create_entity():
    data = {"type": "widget", "name": "w1", "description": "desc"}
    obj = services.create_entity(data)
    assert isinstance(obj, Entity)
    assert obj.id is not None
    assert obj.type == "widget"


@pytest.mark.django_db
def test_list_entities():
    services.create_entity({"type": "a"})
    services.create_entity({"type": "b"})
    qs = services.list_entities()
    assert qs.count() >= 2


@pytest.mark.django_db
def test_get_update_delete_entity():
    created = services.create_entity({"type": "tmp", "name": "n"})
    got = services.get_entity(created.id)
    assert got.id == created.id

    updated = services.update_entity(created.id, {"name": "new"})
    assert updated.name == "new"

    services.delete_entity(created.id)
    with pytest.raises(Entity.DoesNotExist):
        services.get_entity(created.id)
