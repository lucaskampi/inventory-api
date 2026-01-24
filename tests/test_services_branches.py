import pytest
from decimal import Decimal

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_create_without_unit_price_defaults_to_zero():
    obj = services.create_entity({"type": "no_price"})
    assert isinstance(obj, Entity)
    assert obj.unit_price == Decimal("0.0000")


@pytest.mark.django_db
def test_create_accepts_int_float_and_strings():
    a = services.create_entity({"type": "a", "unit_price": 50})
    b = services.create_entity({"type": "b", "unit_price": 50.0})
    c = services.create_entity({"type": "c", "unit_price": "50.99"})
    d = services.create_entity({"type": "d", "unit_price": "50,99"})

    assert a.unit_price == Decimal("50.0000")
    assert b.unit_price == Decimal("50.0000")
    assert c.unit_price == Decimal("50.9900")
    assert d.unit_price == Decimal("50.9900")


@pytest.mark.django_db
def test_update_with_none_or_empty_does_not_change():
    obj = services.create_entity({"type": "u", "unit_price": "10.50"})
    before = obj.unit_price
    updated = services.update_entity(obj.id, {"unit_price": None})
    assert updated.unit_price == before

    updated2 = services.update_entity(obj.id, {"unit_price": ""})
    assert updated2.unit_price == before


@pytest.mark.django_db
def test_list_entities_none_and_empty_and_notcontains():
    # ensure clean state
    for e in list(services.list_entities()):
        e.delete()

    services.create_entity({"type": "tool", "name": "hammer", "description": "heavy tool"})
    services.create_entity({"type": "toolbox", "name": "box", "description": "container"})

    # None should behave like no filter
    all1 = services.list_entities(name=None)
    all2 = services.list_entities()
    assert all1.count() == all2.count()

    # empty string should behave like no filter
    all3 = services.list_entities(name="")
    assert all3.count() == all2.count()

    # notcontains should exclude
    res = services.list_entities(name="box", name_op="notcontains")
    assert all((r.name is None or "box" not in r.name) for r in res)
