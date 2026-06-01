def test_create_farm(client):
    response = client.post("/farms/", json={"name": "Green Valley", "location": "California"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Green Valley"
    assert "id" in data

def test_list_farms(client):
    client.post("/farms/", json={"name": "Sunny Farm", "location": "Texas"})
    response = client.get("/farms/")
    assert response.status_code == 200
    assert len(response.json()) >= 1