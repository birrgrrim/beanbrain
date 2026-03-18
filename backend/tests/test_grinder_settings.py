def _create_coffee(client):
    resp = client.post("/coffees/", json={"name": "Test Coffee", "roastery": "R"})
    return resp.json()["id"]


def _get_defaults(client):
    grinders = client.get("/grinders/").json()
    setups = client.get("/brew-setups/").json()
    grinder_id = next(g["id"] for g in grinders if g["is_default"])
    setup_id = next(s["id"] for s in setups if s["is_default"])
    return grinder_id, setup_id


def test_create_grinder_setting(client):
    coffee_id = _create_coffee(client)
    grinder_id, setup_id = _get_defaults(client)

    resp = client.post(f"/coffees/{coffee_id}/settings/", json={
        "grinder_id": grinder_id,
        "brew_setup_id": setup_id,
        "setting": 12.5,
        "notes": "Good for medium extraction",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["setting"] == 12.5
    assert data["grinder"]["name"] == "Default Grinder"
    assert data["brew_setup"]["method_type"] == "espresso"


def test_create_setting_without_notes(client):
    coffee_id = _create_coffee(client)
    grinder_id, setup_id = _get_defaults(client)

    resp = client.post(f"/coffees/{coffee_id}/settings/", json={
        "grinder_id": grinder_id,
        "brew_setup_id": setup_id,
        "setting": 10,
    })
    assert resp.status_code == 201
    assert resp.json()["notes"] is None


def test_list_grinder_settings(client):
    coffee_id = _create_coffee(client)
    grinder_id, setup_id = _get_defaults(client)

    client.post(f"/coffees/{coffee_id}/settings/", json={
        "grinder_id": grinder_id, "brew_setup_id": setup_id, "setting": 10,
    })

    resp = client.get(f"/coffees/{coffee_id}/settings/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_delete_grinder_setting(client):
    coffee_id = _create_coffee(client)
    grinder_id, setup_id = _get_defaults(client)

    create = client.post(f"/coffees/{coffee_id}/settings/", json={
        "grinder_id": grinder_id, "brew_setup_id": setup_id, "setting": 10,
    })
    setting_id = create.json()["id"]

    resp = client.delete(f"/coffees/{coffee_id}/settings/{setting_id}")
    assert resp.status_code == 204

    resp = client.get(f"/coffees/{coffee_id}/settings/")
    assert len(resp.json()) == 0


def test_setting_for_nonexistent_coffee(client):
    resp = client.get("/coffees/999/settings/")
    assert resp.status_code == 404
