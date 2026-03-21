def test_create_grinder(client):
    resp = client.post("/grinders/", json={
        "manufacturer": "Niche Zero",
        "model": "NZ",
        "kind": "auto",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["manufacturer"] == "Niche Zero"
    assert data["kind"] == "auto"


def test_create_manual_grinder(client):
    resp = client.post("/grinders/", json={
        "manufacturer": "1Zpresso K-Max",
        "kind": "manual",
    })
    assert resp.status_code == 201
    assert resp.json()["kind"] == "manual"



def test_update_grinder(client):
    client.post("/grinders/", json={"manufacturer": "Original"})
    grinders = client.get("/grinders/").json()
    gid = grinders[0]["id"]

    resp = client.put(f"/grinders/{gid}", json={"manufacturer": "Renamed"})
    assert resp.status_code == 200
    assert resp.json()["manufacturer"] == "Renamed"



def test_update_grinder_not_found(client):
    resp = client.put("/grinders/999", json={"manufacturer": "Ghost"})
    assert resp.status_code == 404


def test_delete_grinder(client):
    create = client.post("/grinders/", json={"manufacturer": "Temporary"})
    gid = create.json()["id"]

    resp = client.delete(f"/grinders/{gid}")
    assert resp.status_code == 204

    grinders = client.get("/grinders/").json()
    assert not any(g["id"] == gid for g in grinders)


def test_delete_grinder_not_found(client):
    resp = client.delete("/grinders/999")
    assert resp.status_code == 404
