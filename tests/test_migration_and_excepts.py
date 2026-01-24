import importlib
from decimal import Decimal

import pytest

from entities import services
from entities.models import Entity


@pytest.mark.django_db
def test_create_entity_forced_decimal_invalid_monkeypatch(monkeypatch):
    # Force Decimal(...) to raise for the specific string so except branch is used
    orig_D = services.Decimal

    def fake_D(x):
        # raise InvalidOperation when called with that exact string
        if isinstance(x, str) and x == "50.99":
            raise services.InvalidOperation
        return orig_D(x)

    monkeypatch.setattr(services, 'Decimal', fake_D)

    obj = services.create_entity({"type": "x", "unit_price": "50.99"})
    # despite fake raising on first call, float conversion path should succeed
    assert obj.unit_price == Decimal('50.9900')


@pytest.mark.django_db
def test_update_entity_forced_decimal_invalid(monkeypatch):
    orig_D = services.Decimal

    def fake_D(x):
        if isinstance(x, str) and x == "10.12345":
            raise services.InvalidOperation
        return orig_D(x)

    obj = services.create_entity({"type": "u"})
    monkeypatch.setattr(services, 'Decimal', fake_D)
    updated = services.update_entity(obj.id, {"unit_price": "10.12345"})
    assert updated.unit_price == Decimal('10.1234')


def _make_fake_objs(vals, attr_name):
    class Obj:
        def __init__(self, v):
            setattr(self, attr_name, v)

        def save(self, update_fields=None):
            # pretend to save
            pass

    return [Obj(v) for v in vals]


def test_migration_runpython_forwards_and_backwards():
    mod = importlib.import_module('entities.migrations.0003_entity_unit_price')

    class FakeManager:
        def __init__(self, objs):
            self._objs = objs

        def all(self):
            return list(self._objs)

    class FakeModel:
        def __init__(self, objs):
            self.objects = FakeManager(objs)

    class Apps:
        def __init__(self, model):
            self._model = model

        def get_model(self, app, name):
            return self._model

    # create fake objects with various price_cents
    objs = _make_fake_objs([100, '200', None, 'bad'], 'price_cents')
    fake_model = FakeModel(objs)
    apps = Apps(fake_model)

    # forwards should run and skip problematic rows
    mod.forwards(apps, None)

    # now test backwards with unit_price values
    objs2 = _make_fake_objs([Decimal('1.23'), '4.56', None, 'bad'], 'unit_price')
    fake_model2 = FakeModel(objs2)
    apps2 = Apps(fake_model2)

    mod.backwards(apps2, None)


@pytest.mark.django_db
def test_model_unit_price_decimal_variants():
    e = services.create_entity({"type": "p", "unit_price": "3.1415"})
    assert e.unit_price_decimal == Decimal('3.1415')

    # force string stored in DB (simulate weird value)
    e.unit_price = '2.5'
    assert e.unit_price_decimal == Decimal('2.5')

    e.unit_price = None
    assert e.unit_price_decimal == Decimal('0')
