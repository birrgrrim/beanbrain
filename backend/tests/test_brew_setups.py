def test_create_brew_setup(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "pourover",
        "name": "V60",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["method_type"] == "pourover"
    assert data["name"] == "V60"
    assert data["is_default"] is False
    assert data["basket_grams"] is None


def test_create_espresso_with_basket(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "espresso",
        "name": "Gaggia 18g",
        "basket_grams": 18,
    })
    assert resp.status_code == 201
    assert resp.json()["basket_grams"] == 18


def test_create_brew_setup_invalid_method_type(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "invalid_method",
        "name": "Bad Setup",
    })
    assert resp.status_code == 422  # Pydantic Literal validation


def test_create_default_brew_setup_clears_previous(client):
    # Seed has a default espresso setup
    setups = client.get("/brew-setups/").json()
    assert any(s["is_default"] for s in setups)

    resp = client.post("/brew-setups/", json={
        "method_type": "pourover",
        "name": "New Default",
        "is_default": True,
    })
    assert resp.status_code == 201

    setups = client.get("/brew-setups/").json()
    defaults = [s for s in setups if s["is_default"]]
    assert len(defaults) == 1
    assert defaults[0]["name"] == "New Default"


def test_update_brew_setup(client):
    setups = client.get("/brew-setups/").json()
    sid = setups[0]["id"]

    resp = client.put(f"/brew-setups/{sid}", json={"name": "Renamed Setup"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Renamed Setup"


def test_update_brew_setup_set_default(client):
    create = client.post("/brew-setups/", json={
        "method_type": "aeropress",
        "name": "AeroPress",
    })
    sid = create.json()["id"]

    resp = client.put(f"/brew-setups/{sid}", json={"is_default": True})
    assert resp.status_code == 200

    setups = client.get("/brew-setups/").json()
    defaults = [s for s in setups if s["is_default"]]
    assert len(defaults) == 1
    assert defaults[0]["id"] == sid


def test_update_brew_setup_not_found(client):
    resp = client.put("/brew-setups/999", json={"name": "Ghost"})
    assert resp.status_code == 404


def test_delete_brew_setup(client):
    create = client.post("/brew-setups/", json={
        "method_type": "moka",
        "name": "Bialetti",
    })
    sid = create.json()["id"]

    resp = client.delete(f"/brew-setups/{sid}")
    assert resp.status_code == 204

    setups = client.get("/brew-setups/").json()
    assert not any(s["id"] == sid for s in setups)


def test_delete_brew_setup_not_found(client):
    resp = client.delete("/brew-setups/999")
    assert resp.status_code == 404
