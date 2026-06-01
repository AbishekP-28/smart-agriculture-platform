from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Field, SensorReading

def get_recommendation_text(soil_moisture: float, recent_rainfall_mm: float = 0):
    if soil_moisture < 20:
        return ("Critical", "Irrigate Immediately", f"Soil moisture {soil_moisture}% is very low. Water now.")
    elif soil_moisture < 40:
        if recent_rainfall_mm > 5:
            return ("Dry but rain expected", "Wait & Monitor", f"Rainfall {recent_rainfall_mm}mm recently. Delay irrigation.")
        return ("Dry", "Schedule Irrigation", f"Soil moisture {soil_moisture}% is below ideal. Plan to water within 24h.")
    elif soil_moisture <= 70:
        return ("Adequate", "No Action Needed", "Soil moisture is optimal. Maintain monitoring.")
    else:
        return ("Excessive", "Reduce Irrigation", f"Soil moisture {soil_moisture}% is too high. Avoid watering.")

def get_recent_rainfall(db: Session, field_id: int, hours=24) -> float:
    since = datetime.utcnow() - timedelta(hours=hours)
    readings = db.query(SensorReading).filter(
        SensorReading.field_id == field_id,
        SensorReading.timestamp >= since
    ).all()
    return sum(r.rainfall for r in readings)

def get_recommendation_for_field(db: Session, field: Field):
    latest = db.query(SensorReading).filter(
        SensorReading.field_id == field.id
    ).order_by(SensorReading.timestamp.desc()).first()
    if not latest:
        return None, None, None, None
    rainfall_24h = get_recent_rainfall(db, field.id, 24)
    status, action, message = get_recommendation_text(latest.soil_moisture, rainfall_24h)
    return latest, status, action, message