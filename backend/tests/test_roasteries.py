def test_create_roastery(client):
    resp = client.post("/roasteries/", json={
        "name": "MadHeads",
        "website": "https://madheads.coffee",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "MadHeads"
    assert data["website"] == "https://madheads.coffee"
    assert data["is_active"] is True


def test_create_roastery_minimal(client):
    resp = client.post("/roasteries/", json={"name": "Local"})
    assert resp.status_code == 201
    assert resp.json()["website"] is None
    assert resp.json()["logo_url"] is None


def test_list_roasteries(client):
    client.post("/roasteries/", json={"name": "Roastery A"})
    client.post("/roasteries/", json={"name": "Roastery B"})

    resp = client.get("/roasteries/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_roasteries_sorted_by_name(client):
    client.post("/roasteries/", json={"name": "Zebra Beans"})
    client.post("/roasteries/", json={"name": "Alpha Roast"})

    names = [r["name"] for r in client.get("/roasteries/").json()]
    assert names == ["Alpha Roast", "Zebra Beans"]


def test_update_roastery(client):
    create = client.post("/roasteries/", json={"name": "Old Name"})
    rid = create.json()["id"]

    resp = client.put(f"/roasteries/{rid}", json={"name": "New Name"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"


def test_update_roastery_not_found(client):
    resp = client.put("/roasteries/999", json={"name": "Ghost"})
    assert resp.status_code == 404


def test_delete_roastery_soft_delete(client):
    """Delete should soft-delete (set is_active=False), not hard-delete."""
    create = client.post("/roasteries/", json={"name": "To Deactivate"})
    rid = create.json()["id"]

    resp = client.delete(f"/roasteries/{rid}")
    assert resp.status_code == 204

    # Should not appear in list (filtered by is_active)
    roasteries = client.get("/roasteries/").json()
    assert not any(r["id"] == rid for r in roasteries)


def test_delete_roastery_not_found(client):
    resp = client.delete("/roasteries/999")
    assert resp.status_code == 404
