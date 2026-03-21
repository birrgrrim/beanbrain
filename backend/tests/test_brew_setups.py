def test_create_brew_setup(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "pourover",
        "manufacturer": "V60",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["method_type"] == "pourover"
    assert data["manufacturer"] == "V60"
    assert data["basket_grams"] is None


def test_create_espresso_with_basket(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "espresso",
        "manufacturer": "Gaggia", "model": "18g",
        "basket_grams": 18,
    })
    assert resp.status_code == 201
    assert resp.json()["basket_grams"] == 18


def test_create_brew_setup_invalid_method_type(client):
    resp = client.post("/brew-setups/", json={
        "method_type": "invalid_method",
        "manufacturer": "Bad Setup",
    })
    assert resp.status_code == 422  # Pydantic Literal validation



def test_update_brew_setup(client):
    client.post("/brew-setups/", json={"method_type": "espresso", "manufacturer": "Original"})
    setups = client.get("/brew-setups/").json()
    sid = setups[0]["id"]

    resp = client.put(f"/brew-setups/{sid}", json={"manufacturer": "Renamed Setup"})
    assert resp.status_code == 200
    assert resp.json()["manufacturer"] == "Renamed Setup"



def test_update_brew_setup_not_found(client):
    resp = client.put("/brew-setups/999", json={"manufacturer": "Ghost"})
    assert resp.status_code == 404


def test_delete_brew_setup(client):
    create = client.post("/brew-setups/", json={
        "method_type": "moka",
        "manufacturer": "Bialetti",
    })
    sid = create.json()["id"]

    resp = client.delete(f"/brew-setups/{sid}")
    assert resp.status_code == 204

    setups = client.get("/brew-setups/").json()
    assert not any(s["id"] == sid for s in setups)


def test_delete_brew_setup_not_found(client):
    resp = client.delete("/brew-setups/999")
    assert resp.status_code == 404
