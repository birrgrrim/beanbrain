def _create_coffee(client):
    resp = client.post("/coffees/", json={"name": "Test Coffee", "roastery": "R"})
    return resp.json()["id"]


def _create_taster(client, name="Alex"):
    resp = client.post("/tasters/", json={"name": name})
    return resp.json()["id"]


def test_create_tasting(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_id": taster_id,
        "rating": 8,
        "comment": "Very smooth, great crema",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["taster"]["name"] == "Alex"
    assert data["rating"] == 8


def test_create_tasting_with_descriptors(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client, "Kate")
    descriptors = client.get("/descriptors").json()
    chocolate_id = next(d["id"] for d in descriptors if d["name"] == "Chocolate")

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_id": taster_id,
        "rating": 7,
        "descriptor_ids": [chocolate_id],
    })
    assert resp.status_code == 201
    assert any(d["name"] == "Chocolate" for d in resp.json()["descriptors"])


def test_tasting_rating_validation(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_id": taster_id,
        "rating": 0,
    })
    assert resp.status_code == 422

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_id": taster_id,
        "rating": 11,
    })
    assert resp.status_code == 422


def test_list_tastings(client):
    coffee_id = _create_coffee(client)
    t1 = _create_taster(client, "Alex")
    t2 = _create_taster(client, "Kate")
    client.post(f"/coffees/{coffee_id}/tastings/", json={"taster_id": t1, "rating": 8})
    client.post(f"/coffees/{coffee_id}/tastings/", json={"taster_id": t2, "rating": 6})

    resp = client.get(f"/coffees/{coffee_id}/tastings/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_delete_tasting(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)
    create = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_id": taster_id, "rating": 5,
    })
    tasting_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}/tastings/{tasting_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}/tastings/")
    assert len(resp.json()) == 0


def test_tasting_for_nonexistent_coffee(client):
    taster_id = _create_taster(client)
    resp = client.post("/coffees/999/tastings/", json={
        "taster_id": taster_id, "rating": 5,
    })
    assert resp.status_code == 404
