def _create_coffee(client):
    resp = client.post("/coffees/", json={"name": "Test Coffee", "roastery": "R"})
    return resp.json()["id"]


def test_create_tasting(client):
    coffee_id = _create_coffee(client)

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_name": "Alex",
        "rating": 8,
        "comment": "Very smooth, great crema",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["taster_name"] == "Alex"
    assert data["rating"] == 8


def test_create_tasting_with_descriptors(client):
    coffee_id = _create_coffee(client)
    descriptors = client.get("/descriptors").json()
    chocolate_id = next(d["id"] for d in descriptors if d["name"] == "Chocolate")

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_name": "Kate",
        "rating": 7,
        "descriptor_ids": [chocolate_id],
    })
    assert resp.status_code == 201
    assert any(d["name"] == "Chocolate" for d in resp.json()["descriptors"])


def test_tasting_rating_validation(client):
    coffee_id = _create_coffee(client)

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_name": "Alex",
        "rating": 0,
    })
    assert resp.status_code == 422

    resp = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_name": "Alex",
        "rating": 11,
    })
    assert resp.status_code == 422


def test_list_tastings(client):
    coffee_id = _create_coffee(client)
    client.post(f"/coffees/{coffee_id}/tastings/", json={"taster_name": "Alex", "rating": 8})
    client.post(f"/coffees/{coffee_id}/tastings/", json={"taster_name": "Kate", "rating": 6})

    resp = client.get(f"/coffees/{coffee_id}/tastings/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_delete_tasting(client):
    coffee_id = _create_coffee(client)
    create = client.post(f"/coffees/{coffee_id}/tastings/", json={
        "taster_name": "Alex", "rating": 5,
    })
    tasting_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}/tastings/{tasting_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}/tastings/")
    assert len(resp.json()) == 0


def test_tasting_for_nonexistent_coffee(client):
    resp = client.post("/coffees/999/tastings/", json={
        "taster_name": "Alex", "rating": 5,
    })
    assert resp.status_code == 404
