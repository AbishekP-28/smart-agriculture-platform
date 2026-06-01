def test_recommendation_endpoint(client):
    farm = client.post("/farms/", json={"name": "Test Farm"}).json()
    field = client.post(f"/fields/?farm_id={farm['id']}", json={"name": "Wheat Field"}).json()
    client.post("/simulate/trigger")
    resp = client.get(f"/recommendations/fields/{field['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert "action" in data
    assert "soil_moisture_status" in data