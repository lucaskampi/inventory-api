import pytest
import json
from django.test import Client


@pytest.mark.django_db
def test_api_crud_flow():
    client = Client()

    # create
    resp = client.post(
        "/api/entities",
        data=json.dumps({"type": "widget", "name": "w1", "description": "desc"}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    body = resp.json()
    entity_id = body["id"] if isinstance(body, list) else body.get("id")

    # get
    resp = client.get(f"/api/entities/{entity_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == entity_id

    # update
    resp = client.put(
        f"/api/entities/{entity_id}",
        data=json.dumps({"name": "updated"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "updated"

    # delete
    resp = client.delete(f"/api/entities/{entity_id}")
    assert resp.status_code in (200, 204)
