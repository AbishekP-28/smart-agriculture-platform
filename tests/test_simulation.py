from app.simulation import generate_reading_for_field
from app.models import Farm, Field

def test_generate_reading(db_session):
    farm = Farm(name="Sim Farm")
    db_session.add(farm)
    db_session.commit()
    field = Field(name="Test Field", farm_id=farm.id)
    db_session.add(field)
    db_session.commit()
    
    reading = generate_reading_for_field(db_session, field)
    assert 0 <= reading.soil_moisture <= 100
    assert 0 <= reading.humidity <= 100
    assert reading.rainfall >= 0