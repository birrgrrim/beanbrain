def test_create_taster(client):
    resp = client.post("/tasters/", json={"name": "Alex"})
    assert resp.status_code == 201
    assert resp.json()["name"] == "Alex"


def test_create_duplicate_taster(client):
    client.post("/tasters/", json={"name": "Alex"})
    resp = client.post("/tasters/", json={"name": "Alex"})
    assert resp.status_code == 409


def test_list_tasters(client):
    client.post("/tasters/", json={"name": "Alex"})
    client.post("/tasters/", json={"name": "Kate"})
    resp = client.get("/tasters/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_delete_taster(client):
    create = client.post("/tasters/", json={"name": "ToDelete"})
    taster_id = create.json()["id"]
    resp = client.delete(f"/tasters/{taster_id}")
    assert resp.status_code == 204

    resp = client.get("/tasters/")
    assert len(resp.json()) == 0


def test_list_grinders(client):
    resp = client.get("/grinders/")
    assert resp.status_code == 200
    grinders = resp.json()
    assert len(grinders) == 1
    assert grinders[0]["name"] == "Default Grinder"
    assert grinders[0]["is_default"] is True


def test_list_brew_setups(client):
    resp = client.get("/brew-setups/")
    assert resp.status_code == 200
    setups = resp.json()
    assert len(setups) == 1
    assert setups[0]["method_type"] == "espresso"


def test_list_brew_method_types(client):
    resp = client.get("/brew-method-types")
    assert resp.status_code == 200
    types = resp.json()
    assert len(types) == 6
    keys = [t["key"] for t in types]
    assert "espresso" in keys and "pourover" in keys
