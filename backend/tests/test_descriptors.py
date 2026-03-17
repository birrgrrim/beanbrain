def test_list_descriptors(client):
    resp = client.get("/descriptors")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 50
    assert all("name" in d and "category" in d for d in data)


def test_descriptors_have_categories(client):
    resp = client.get("/descriptors")
    categories = {d["category"] for d in resp.json()}
    assert "Fruity" in categories
    assert "Sweet" in categories
    assert "Nutty" in categories
