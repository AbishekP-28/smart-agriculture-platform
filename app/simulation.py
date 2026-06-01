import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Field, SensorReading

def get_last_reading(db: Session, field_id: int):
    return db.query(SensorReading).filter(
        SensorReading.field_id == field_id
    ).order_by(SensorReading.timestamp.desc()).first()

def generate_reading_for_field(db: Session, field: Field) -> SensorReading:
    last = get_last_reading(db, field.id)
    
    if last:
        soil_moisture = last.soil_moisture
        humidity = last.humidity
        temperature = last.temperature
        rainfall = last.rainfall
    else:
        soil_moisture = random.uniform(40, 70)
        humidity = random.uniform(40, 80)
        temperature = random.uniform(15, 30)
        rainfall = 0.0
    
    # Simulate changes
    evap = random.uniform(0, 2.5)
    soil_moisture -= evap
    
    temperature += random.uniform(-1.5, 1.5)
    temperature = max(0, min(50, temperature))
    
    humidity += random.uniform(-5, 5)
    humidity = max(20, min(95, humidity))
    
    rainfall = 0.0
    if random.random() < 0.2:
        rainfall = random.uniform(0.5, 12.0)
        soil_moisture += rainfall * 1.2
    
    soil_moisture = max(0, min(100, soil_moisture))
    
    new_reading = SensorReading(
        field_id=field.id,
        soil_moisture=round(soil_moisture, 1),
        humidity=round(humidity, 1),
        temperature=round(temperature, 1),
        rainfall=round(rainfall, 1),
        timestamp=datetime.utcnow()
    )
    return new_reading

def simulate_all_fields(db: Session):
    fields = db.query(Field).all()
    new_readings = []
    for field in fields:
        reading = generate_reading_for_field(db, field)
        db.add(reading)
        new_readings.append(reading)
    db.commit()
    return new_readings