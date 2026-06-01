def test_dashboard_summary(client):
    response = client.get("/analytics/dashboard-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_farms" in data
    assert "total_fields" in data
    assert "average_soil_moisture" in data