def test_list_origins(client):
    resp = client.get("/origins/")
    assert resp.status_code == 200
    origins = resp.json()
    assert len(origins) > 30


def test_origins_have_bilingual_names(client):
    origins = client.get("/origins/").json()
    ethiopia = next(o for o in origins if o["name_en"] == "Ethiopia")
    assert ethiopia["name_uk"] == "Ефіопія"
    assert ethiopia["flag"] == "🇪🇹"


def test_origins_sorted_by_english_name(client):
    origins = client.get("/origins/").json()
    names = [o["name_en"] for o in origins]
    assert names == sorted(names)
