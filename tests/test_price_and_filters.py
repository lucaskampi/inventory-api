import pytest
from decimal import Decimal

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_truncation_and_sum():
    e1 = services.create_entity({"type": "fruit", "unit_price": "1.864"})
    e2 = services.create_entity({"type": "fruit", "unit_price": "1.134"})

    assert isinstance(e1, Entity)
    assert isinstance(e2, Entity)

    assert e1.price_cents_truncated() == 186
    assert e2.price_cents_truncated() == 113

    total_cents = e1.price_cents_truncated() + e2.price_cents_truncated()
    assert total_cents == 299
    assert total_cents / 100 == 2.99


@pytest.mark.django_db
def test_create_accepts_comma_and_dot():
    a = services.create_entity({"type": "veh", "unit_price": "50,99"})
    b = services.create_entity({"type": "veh", "unit_price": 50.99})

    assert a.unit_price == Decimal("50.9900")
    assert b.unit_price == Decimal("50.9900")


@pytest.mark.django_db
def test_update_sets_unit_price():
    obj = services.create_entity({"type": "t"})
    updated = services.update_entity(obj.id, {"unit_price": "10,12345"})
    # quantized to 4 decimals with ROUND_DOWN -> 10.1234
    assert updated.unit_price == Decimal("10.1234")


@pytest.mark.django_db
def test_list_entities_operators():
    # create sample data
    services.create_entity({"type": "tool", "name": "hammer", "description": "heavy tool"})
    services.create_entity({"type": "toolbox", "name": "box", "description": "container"})
    services.create_entity({"type": "widget", "name": "w1", "description": "blue widget"})

    # contains (default)
    res = services.list_entities(name="amm")
    assert any(r.name == "hammer" for r in res)

    # startswith
    res2 = services.list_entities(name="ham", name_op="startswith")
    assert any(r.name == "hammer" for r in res2)

    # equals on type
    res3 = services.list_entities(type="tool", type_op="equals")
    assert all(r.type == "tool" for r in res3)

    # endswith on description
    res4 = services.list_entities(description="widget", description_op="endswith")
    assert any(r.description.endswith("widget") for r in res4)

    # notcontains exclude names with 'box'
    res5 = services.list_entities(name="box", name_op="notcontains")
    assert all("box" not in (r.name or "") for r in res5)
