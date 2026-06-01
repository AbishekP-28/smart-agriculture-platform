def test_create_field(client):
    farm = client.post("/farms/", json={"name": "Farm A"}).json()
    response = client.post(f"/fields/?farm_id={farm['id']}", json={"name": "Wheat Field", "area_ha": 10.5})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Wheat Field"
    assert data["farm_id"] == farm["id"]

def test_list_fields(client):
    farm = client.post("/farms/", json={"name": "Farm B"}).json()
    client.post(f"/fields/?farm_id={farm['id']}", json={"name": "Field 1"})
    response = client.get(f"/fields/?farm_id={farm['id']}")
    assert response.status_code == 200
    assert len(response.json()) >= 1