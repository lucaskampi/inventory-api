import pytest
from django.http import Http404

from entities import api, services
from entities.schemas import EntityCreate, EntityUpdate
from entities.models import Entity


@pytest.mark.django_db
def test_list_entities_direct_empty_then_nonempty():
    # ensure DB empty for entities
    for e in services.list_entities():
        e.delete()

    res = api.list_entities(None)
    assert isinstance(res, list)
    assert res == []

    # create one and verify
    obj = services.create_entity({"type": "t"})
    res2 = api.list_entities(None)
    assert any(isinstance(x, Entity) for x in res2)


@pytest.mark.django_db
def test_get_entity_direct_404_and_success():
    with pytest.raises(Http404):
        api.get_entity(None, 999999)

    obj = services.create_entity({"type": "g"})
    got = api.get_entity(None, obj.id)
    assert got.id == obj.id


@pytest.mark.django_db
def test_create_entity_direct():
    payload = EntityCreate(type="x", name="n")
    status, obj = api.create_entity(None, payload)
    assert status == 201
    assert isinstance(obj, Entity)


@pytest.mark.django_db
def test_update_entity_direct_404_and_partial():
    payload = EntityUpdate(name="updated")
    with pytest.raises(Http404):
        api.update_entity(None, 999999, payload)

    obj = services.create_entity({"type": "t", "name": "old", "description": "d"})
    updated = api.update_entity(None, obj.id, payload)
    assert updated.name == "updated"
    assert updated.type == "t"


@pytest.mark.django_db
def test_delete_entity_direct_404_and_success():
    with pytest.raises(Http404):
        api.delete_entity(None, 999999)

    obj = services.create_entity({"type": "t"})
    status, body = api.delete_entity(None, obj.id)
    assert status == 204
    with pytest.raises(Entity.DoesNotExist):
        services.get_entity(obj.id)
