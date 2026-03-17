def _create_coffee(client):
    resp = client.post("/coffees/", json={"name": "Test Coffee", "roastery": "R"})
    return resp.json()["id"]


def _get_defaults(client):
    equipment = client.get("/equipment").json()
    methods = client.get("/brew-methods").json()
    baskets = client.get("/basket-sizes").json()
    grinder_id = next(e["id"] for e in equipment if e["type"] == "grinder")
    espresso_id = next(m["id"] for m in methods if m["name"] == "Espresso")
    basket_18 = next(b["id"] for b in baskets if b["size_grams"] == 18)
    return grinder_id, espresso_id, basket_18


def test_create_grinder_setting(client):
    coffee_id = _create_coffee(client)
    grinder_id, espresso_id, basket_18 = _get_defaults(client)

    resp = client.post(f"/coffees/{coffee_id}/settings/", json={
        "equipment_id": grinder_id,
        "brew_method_id": espresso_id,
        "basket_size_id": basket_18,
        "setting": 12.5,
        "notes": "Good for medium extraction",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["setting"] == 12.5
    assert data["equipment"]["type"] == "grinder"
    assert data["brew_method"]["name"] == "Espresso"
    assert data["basket_size"]["size_grams"] == 18


def test_create_setting_without_basket(client):
    coffee_id = _create_coffee(client)
    grinder_id, espresso_id, _ = _get_defaults(client)

    resp = client.post(f"/coffees/{coffee_id}/settings/", json={
        "equipment_id": grinder_id,
        "brew_method_id": espresso_id,
        "setting": 10,
    })
    assert resp.status_code == 201
    assert resp.json()["basket_size"] is None


def test_list_grinder_settings(client):
    coffee_id = _create_coffee(client)
    grinder_id, espresso_id, basket_18 = _get_defaults(client)

    client.post(f"/coffees/{coffee_id}/settings/", json={
        "equipment_id": grinder_id, "brew_method_id": espresso_id,
        "basket_size_id": basket_18, "setting": 10,
    })

    resp = client.get(f"/coffees/{coffee_id}/settings/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_delete_grinder_setting(client):
    coffee_id = _create_coffee(client)
    grinder_id, espresso_id, _ = _get_defaults(client)

    create = client.post(f"/coffees/{coffee_id}/settings/", json={
        "equipment_id": grinder_id, "brew_method_id": espresso_id, "setting": 10,
    })
    setting_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}/settings/{setting_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}/settings/")
    assert len(resp.json()) == 0


def test_setting_for_nonexistent_coffee(client):
    resp = client.get("/coffees/999/settings/")
    assert resp.status_code == 404
