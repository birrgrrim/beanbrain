def _create_coffee(client):
    rid = client.post("/roasteries/", json={"name": "Test Roastery"}).json()["id"]
    resp = client.post("/coffees/", json={"name": "Test Coffee", "roastery_id": rid})
    return resp.json()["id"]


def _create_taster(client, name="Alex"):
    resp = client.post("/tasters/", json={"name": name})
    return resp.json()["id"]


def _default_brew_setup_id(client):
    setups = client.get("/brew-setups/").json()
    return next(s["id"] for s in setups if s["is_default"])


def test_create_review(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)
    setup_id = _default_brew_setup_id(client)

    resp = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id,
        "brew_setup_id": setup_id,
        "rating": 8,
        "comment": "Very smooth, great crema",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["taster"]["name"] == "Alex"
    assert data["rating"] == 8
    assert data["brew_setup_id"] == setup_id


def test_upsert_review(client):
    """Same person + brew setup updating their review should overwrite, not create new."""
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)
    setup_id = _default_brew_setup_id(client)

    client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 6, "comment": "Ok",
    })
    resp = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 9, "comment": "Actually great!",
    })
    assert resp.json()["rating"] == 9
    assert resp.json()["comment"] == "Actually great!"

    # Should still be only one review
    reviews = client.get(f"/coffees/{coffee_id}/reviews/").json()
    assert len(reviews) == 1


def test_review_with_descriptors(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client, "Kate")
    setup_id = _default_brew_setup_id(client)
    descriptors = client.get("/descriptors").json()
    chocolate_id = next(d["id"] for d in descriptors if d["name"] == "Chocolate")

    resp = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id,
        "brew_setup_id": setup_id,
        "rating": 7,
        "descriptor_ids": [chocolate_id],
    })
    assert resp.status_code == 200
    assert any(d["name"] == "Chocolate" for d in resp.json()["descriptors"])


def test_review_rating_validation(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)
    setup_id = _default_brew_setup_id(client)

    resp = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 0,
    })
    assert resp.status_code == 422

    resp = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 11,
    })
    assert resp.status_code == 422


def test_per_method_reviews(client):
    """Same person can review same coffee for different brew methods."""
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)

    # Create a second brew setup
    s2 = client.post("/brew-setups/", json={
        "method_type": "pourover", "manufacturer": "Hario", "model": "V60",
    }).json()

    setup1 = _default_brew_setup_id(client)
    setup2 = s2["id"]

    client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup1, "rating": 9,
    })
    client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup2, "rating": 5,
    })

    reviews = client.get(f"/coffees/{coffee_id}/reviews/").json()
    assert len(reviews) == 2
    ratings = {r["brew_setup_id"]: r["rating"] for r in reviews}
    assert ratings[setup1] == 9
    assert ratings[setup2] == 5


def test_list_reviews(client):
    coffee_id = _create_coffee(client)
    t1 = _create_taster(client, "Alex")
    t2 = _create_taster(client, "Kate")
    setup_id = _default_brew_setup_id(client)
    client.put(f"/coffees/{coffee_id}/reviews/", json={"taster_id": t1, "brew_setup_id": setup_id, "rating": 8})
    client.put(f"/coffees/{coffee_id}/reviews/", json={"taster_id": t2, "brew_setup_id": setup_id, "rating": 6})

    resp = client.get(f"/coffees/{coffee_id}/reviews/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_delete_review(client):
    coffee_id = _create_coffee(client)
    taster_id = _create_taster(client)
    setup_id = _default_brew_setup_id(client)
    create = client.put(f"/coffees/{coffee_id}/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 5,
    })
    review_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}/reviews/{review_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}/reviews/")
    assert len(resp.json()) == 0


def test_review_for_nonexistent_coffee(client):
    taster_id = _create_taster(client)
    setup_id = _default_brew_setup_id(client)
    resp = client.put("/coffees/999/reviews/", json={
        "taster_id": taster_id, "brew_setup_id": setup_id, "rating": 5,
    })
    assert resp.status_code == 404


def test_coffee_stock_and_store(client):
    rid = client.post("/roasteries/", json={"name": "R"}).json()["id"]
    resp = client.post("/coffees/", json={"name": "Coffee", "roastery_id": rid})
    data = resp.json()
    assert data["in_stock"] is False
    assert data["in_store"] is True

    coffee_id = data["id"]
    resp = client.put(f"/coffees/{coffee_id}", json={"in_stock": True})
    assert resp.json()["in_stock"] is True

    resp = client.put(f"/coffees/{coffee_id}", json={"in_store": False})
    assert resp.json()["in_store"] is False


def test_coffees_sorted_by_stock(client):
    rid = client.post("/roasteries/", json={"name": "R"}).json()["id"]
    c1 = client.post("/coffees/", json={"name": "Archive", "roastery_id": rid}).json()
    c2 = client.post("/coffees/", json={"name": "AtHome", "roastery_id": rid}).json()
    client.put(f"/coffees/{c1['id']}", json={"in_store": False})
    client.put(f"/coffees/{c2['id']}", json={"in_stock": True})

    coffees = client.get("/coffees/").json()
    assert coffees[0]["name"] == "AtHome"  # in_stock first
    assert coffees[1]["name"] == "Archive"  # archive last
