def _create_roastery(client, name="Test Roastery"):
    resp = client.post("/roasteries/", json={"name": name})
    return resp.json()["id"]


def test_create_coffee(client):
    rid = _create_roastery(client, "Local Roasters")
    resp = client.post("/coffees/", json={
        "name": "Ethiopia Yirgacheffe",
        "roastery_id": rid,
        "process": "Washed",
        "roast_level": "Light",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Ethiopia Yirgacheffe"
    assert data["roastery_ref"]["name"] == "Local Roasters"
    assert data["id"] is not None


def test_create_coffee_with_descriptors(client):
    rid = _create_roastery(client, "Bean Co")
    descriptors = client.get("/descriptors").json()
    chocolate = next(d for d in descriptors if d["name"] == "Chocolate")
    berry = next(d for d in descriptors if d["name"] == "Berry")

    resp = client.post("/coffees/", json={
        "name": "Colombia Supremo",
        "roastery_id": rid,
        "roastery_descriptor_ids": [chocolate["id"], berry["id"]],
    })
    assert resp.status_code == 201
    data = resp.json()
    names = {d["name"] for d in data["roastery_descriptors"]}
    assert "Chocolate" in names
    assert "Berry" in names


def test_create_coffee_with_origin(client):
    rid = _create_roastery(client)
    origins = client.get("/origins/").json()
    ethiopia = next(o for o in origins if o["name_en"] == "Ethiopia")

    resp = client.post("/coffees/", json={
        "name": "Sidamo",
        "roastery_id": rid,
        "origin_id": ethiopia["id"],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["origin_ref"]["name_en"] == "Ethiopia"
    assert data["origin_ref"]["flag"] == "🇪🇹"


def test_list_coffees(client):
    rid = _create_roastery(client)
    client.post("/coffees/", json={"name": "Coffee A", "roastery_id": rid})
    client.post("/coffees/", json={"name": "Coffee B", "roastery_id": rid})

    resp = client.get("/coffees/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_coffees(client):
    rid = _create_roastery(client)
    client.post("/coffees/", json={"name": "Kenya AA", "roastery_id": rid})
    client.post("/coffees/", json={"name": "Brazil Santos", "roastery_id": rid})

    resp = client.get("/coffees/", params={"search": "kenya"})
    assert len(resp.json()) == 1
    assert resp.json()[0]["name"] == "Kenya AA"


def test_get_coffee(client):
    rid = _create_roastery(client)
    create = client.post("/coffees/", json={"name": "Test", "roastery_id": rid})
    coffee_id = create.json()["id"]

    resp = client.get(f"/coffees/{coffee_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test"


def test_get_coffee_not_found(client):
    resp = client.get("/coffees/999")
    assert resp.status_code == 404


def test_update_coffee(client):
    rid = _create_roastery(client)
    create = client.post("/coffees/", json={"name": "Old", "roastery_id": rid})
    coffee_id = create.json()["id"]

    resp = client.put(f"/coffees/{coffee_id}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"


def test_delete_coffee(client):
    rid = _create_roastery(client)
    create = client.post("/coffees/", json={"name": "Delete Me", "roastery_id": rid})
    coffee_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}")
    assert resp.status_code == 404
