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


def test_list_basket_sizes(client):
    resp = client.get("/basket-sizes")
    assert resp.status_code == 200
    sizes = resp.json()
    assert len(sizes) == 3
    grams = [s["size_grams"] for s in sizes]
    assert 14 in grams and 18 in grams and 25 in grams
