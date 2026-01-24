import pytest
from decimal import Decimal

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_model_helpers_direct_access():
    obj = services.create_entity({"type": "test", "unit_price": "1.864"})
    # access Decimal property
    dec = obj.unit_price_decimal
    assert isinstance(dec, Decimal)
    # access float helper
    f = obj.unit_price_float
    assert isinstance(f, float)
    # truncated cents
    cents = obj.price_cents_truncated()
    assert isinstance(cents, int)
    assert cents == 186


@pytest.mark.django_db
def test_services_create_update_variants_cover_branches():
    # integers and floats
    e1 = services.create_entity({"type": "v", "unit_price": 50})
    e2 = services.create_entity({"type": "v", "unit_price": 50.0})
    e3 = services.create_entity({"type": "v", "unit_price": "50.50"})
    e4 = services.create_entity({"type": "v", "unit_price": "50,50"})

    assert e1.unit_price == Decimal("50.0000")
    assert e2.unit_price == Decimal("50.0000")
    assert e3.unit_price == Decimal("50.5000")
    assert e4.unit_price == Decimal("50.5000")

    # update with different forms
    updated = services.update_entity(e1.id, {"unit_price": "10,12345"})
    assert updated.unit_price == Decimal("10.1234")

    # update with empty string should not change
    before = e2.unit_price
    updated2 = services.update_entity(e2.id, {"unit_price": ""})
    assert updated2.unit_price == before

    # update with None should not change
    updated3 = services.update_entity(e3.id, {"unit_price": None})
    assert updated3.unit_price == e3.unit_price


@pytest.mark.django_db
def test_list_entities_all_ops_exercised():
    # prepare data
    for e in list(services.list_entities()):
        e.delete()

    services.create_entity({"type": "tool", "name": "hammer", "description": "heavy tool"})
    services.create_entity({"type": "toolbox", "name": "box", "description": "container"})
    services.create_entity({"type": "widget", "name": "w1", "description": "blue widget"})

    # contains (default)
    r1 = services.list_entities(name="amm")
    assert any(getattr(x, 'name', '') == 'hammer' for x in r1)

    # startswith
    r2 = services.list_entities(name="ham", name_op="startswith")
    assert any(getattr(x, 'name', '') == 'hammer' for x in r2)

    # equals on type
    r3 = services.list_entities(type="tool", type_op="equals")
    assert all(x.type == "tool" for x in r3)

    # endswith on description
    r4 = services.list_entities(description="widget", description_op="endswith")
    assert any((x.description or '').endswith("widget") for x in r4)

    # notcontains
    r5 = services.list_entities(name="box", name_op="notcontains")
    assert all((x.name is None) or ("box" not in x.name) for x in r5)

    # empty string and None filters
    all_none = services.list_entities(name=None)
    all_empty = services.list_entities(name="")
    assert all_none.count() == all_empty.count()
