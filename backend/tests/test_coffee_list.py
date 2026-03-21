"""Tests for computed fields in coffee list: avg_rating, person_rating, default_grind, descriptor filter."""


def _setup(client):
    """Create a roastery + coffee, return (roastery_id, coffee_id, default_setup_id)."""
    rid = client.post("/roasteries/", json={"name": "Test Roastery"}).json()["id"]
    cid = client.post("/coffees/", json={"name": "Test Coffee", "roastery_id": rid}).json()["id"]
    setups = client.get("/brew-setups/").json()
    sid = setups[0]["id"] if setups else client.post("/brew-setups/", json={"method_type": "espresso", "manufacturer": "Test"}).json()["id"]
    return rid, cid, sid


def test_avg_rating_single_review(client):
    _, cid, sid = _setup(client)
    tid = client.post("/tasters/", json={"name": "Alex"}).json()["id"]
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": tid, "brew_setup_id": sid, "rating": 8})

    coffees = client.get("/coffees/", params={"brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["avg_rating"] == 8.0


def test_avg_rating_multiple_reviews(client):
    _, cid, sid = _setup(client)
    t1 = client.post("/tasters/", json={"name": "Alex"}).json()["id"]
    t2 = client.post("/tasters/", json={"name": "Kate"}).json()["id"]
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t1, "brew_setup_id": sid, "rating": 7})
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t2, "brew_setup_id": sid, "rating": 9})

    coffees = client.get("/coffees/", params={"brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["avg_rating"] == 8.0


def test_avg_rating_rounds_to_one_decimal(client):
    _, cid, sid = _setup(client)
    t1 = client.post("/tasters/", json={"name": "Alex"}).json()["id"]
    t2 = client.post("/tasters/", json={"name": "Kate"}).json()["id"]
    t3 = client.post("/tasters/", json={"name": "Sam"}).json()["id"]
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t1, "brew_setup_id": sid, "rating": 7})
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t2, "brew_setup_id": sid, "rating": 8})
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t3, "brew_setup_id": sid, "rating": 9})

    coffees = client.get("/coffees/", params={"brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["avg_rating"] == 8.0  # (7+8+9)/3 = 8.0


def test_avg_rating_none_without_reviews(client):
    _, cid, sid = _setup(client)
    coffees = client.get("/coffees/", params={"brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["avg_rating"] is None


def test_person_rating(client):
    _, cid, sid = _setup(client)
    t1 = client.post("/tasters/", json={"name": "Alex"}).json()["id"]
    t2 = client.post("/tasters/", json={"name": "Kate"}).json()["id"]
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t1, "brew_setup_id": sid, "rating": 7})
    client.put(f"/coffees/{cid}/reviews/", json={"taster_id": t2, "brew_setup_id": sid, "rating": 9})

    coffees = client.get("/coffees/", params={"taster_id": t1, "brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["person_rating"] == 7


def test_person_rating_none_without_review(client):
    _, cid, sid = _setup(client)
    t1 = client.post("/tasters/", json={"name": "Alex"}).json()["id"]

    coffees = client.get("/coffees/", params={"taster_id": t1, "brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["person_rating"] is None


def test_default_grind(client):
    _, cid, sid = _setup(client)
    grinders = client.get("/grinders/").json()
    grinder_id = grinders[0]["id"] if grinders else client.post("/grinders/", json={"manufacturer": "Test"}).json()["id"]
    setups2 = client.get("/brew-setups/").json()
    setup_id = setups2[0]["id"] if setups2 else client.post("/brew-setups/", json={"method_type": "espresso", "manufacturer": "Test"}).json()["id"]

    client.post(f"/coffees/{cid}/settings/", json={
        "grinder_id": grinder_id,
        "brew_setup_id": setup_id,
        "setting": 14.5,
    })

    coffees = client.get("/coffees/", params={"grinder_id": grinder_id, "brew_setup_id": setup_id}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["default_grind"] == 14.5


def test_default_grind_none_without_setting(client):
    _, cid, sid = _setup(client)
    coffees = client.get("/coffees/", params={"brew_setup_id": sid}).json()
    coffee = next(c for c in coffees if c["id"] == cid)
    assert coffee["default_grind"] is None


def test_filter_by_descriptor(client):
    rid = client.post("/roasteries/", json={"name": "R"}).json()["id"]
    descriptors = client.get("/descriptors").json()
    choc_id = next(d["id"] for d in descriptors if d["name"] == "Chocolate")
    berry_id = next(d["id"] for d in descriptors if d["name"] == "Berry")

    # Coffee with chocolate
    client.post("/coffees/", json={
        "name": "Choco Coffee",
        "roastery_id": rid,
        "roastery_descriptor_ids": [choc_id],
    })
    # Coffee with berry
    client.post("/coffees/", json={
        "name": "Berry Coffee",
        "roastery_id": rid,
        "roastery_descriptor_ids": [berry_id],
    })

    resp = client.get("/coffees/", params={"descriptor_id": choc_id})
    coffees = resp.json()
    assert len(coffees) == 1
    assert coffees[0]["name"] == "Choco Coffee"
