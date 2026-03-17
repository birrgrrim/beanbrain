def test_create_coffee(client):
    resp = client.post("/coffees/", json={
        "name": "Ethiopia Yirgacheffe",
        "roastery": "Local Roasters",
        "origin": "Ethiopia",
        "process": "Washed",
        "roast_level": "Light",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Ethiopia Yirgacheffe"
    assert data["roastery"] == "Local Roasters"
    assert data["id"] is not None


def test_create_coffee_with_descriptors(client):
    descriptors = client.get("/descriptors").json()
    chocolate = next(d for d in descriptors if d["name"] == "Chocolate")
    berry = next(d for d in descriptors if d["name"] == "Berry")

    resp = client.post("/coffees/", json={
        "name": "Colombia Supremo",
        "roastery": "Bean Co",
        "roastery_descriptor_ids": [chocolate["id"], berry["id"]],
    })
    assert resp.status_code == 201
    data = resp.json()
    names = {d["name"] for d in data["roastery_descriptors"]}
    assert "Chocolate" in names
    assert "Berry" in names


def test_list_coffees(client):
    client.post("/coffees/", json={"name": "Coffee A", "roastery": "R1"})
    client.post("/coffees/", json={"name": "Coffee B", "roastery": "R2"})

    resp = client.get("/coffees/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_search_coffees(client):
    client.post("/coffees/", json={"name": "Kenya AA", "roastery": "Roaster One"})
    client.post("/coffees/", json={"name": "Brazil Santos", "roastery": "Roaster Two"})

    resp = client.get("/coffees/", params={"search": "kenya"})
    assert len(resp.json()) == 1
    assert resp.json()[0]["name"] == "Kenya AA"


def test_get_coffee(client):
    create = client.post("/coffees/", json={"name": "Test", "roastery": "R"})
    coffee_id = create.json()["id"]

    resp = client.get(f"/coffees/{coffee_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test"


def test_get_coffee_not_found(client):
    resp = client.get("/coffees/999")
    assert resp.status_code == 404


def test_update_coffee(client):
    create = client.post("/coffees/", json={"name": "Old", "roastery": "R"})
    coffee_id = create.json()["id"]

    resp = client.put(f"/coffees/{coffee_id}", json={"name": "New"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"
    assert resp.json()["roastery"] == "R"


def test_delete_coffee(client):
    create = client.post("/coffees/", json={"name": "Delete Me", "roastery": "R"})
    coffee_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}")
    assert resp.status_code == 404
