import pytest
import json
from django.test import Client


@pytest.mark.django_db
def test_get_not_found():
    client = Client()
    assert client.get("/api/entities/999999").status_code == 404


@pytest.mark.django_db
def test_create_invalid_payload():
    client = Client()
    resp = client.post(
        "/api/entities", json.dumps({"name": "x"}), content_type="application/json"
    )
    assert resp.status_code in (400, 422)


@pytest.mark.django_db
def test_delete_nonexistent_returns_404():
    client = Client()
    resp = client.delete("/api/entities/999999")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_list_empty_returns_empty_list():
    client = Client()
    resp = client.get("/api/entities")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.django_db
def test_update_not_found_returns_404():
    client = Client()
    resp = client.put(
        "/api/entities/999999",
        data=json.dumps({"name": "nope"}),
        content_type="application/json",
    )
    assert resp.status_code == 404
