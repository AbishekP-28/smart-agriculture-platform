from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app import models, schemas, recommendation
from app.database import get_db

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/farms/{farm_id}/health", response_model=schemas.FarmHealthReport)
def farm_health_report(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    
    fields_summary = []
    critical_count = 0
    total_health = 0.0
    
    for field in farm.fields:
        latest, status, action, _ = recommendation.get_recommendation_for_field(db, field)
        if latest:
            avg_soil = db.query(func.avg(models.SensorReading.soil_moisture)).filter(
                models.SensorReading.field_id == field.id
            ).scalar() or 0.0
            avg_temp = db.query(func.avg(models.SensorReading.temperature)).filter(
                models.SensorReading.field_id == field.id
            ).scalar() or 0.0
            avg_hum = db.query(func.avg(models.SensorReading.humidity)).filter(
                models.SensorReading.field_id == field.id
            ).scalar() or 0.0
            
            since = datetime.utcnow() - timedelta(hours=24)
            rainfall_sum = db.query(func.sum(models.SensorReading.rainfall)).filter(
                models.SensorReading.field_id == field.id,
                models.SensorReading.timestamp >= since
            ).scalar() or 0.0
            
            fields_summary.append(schemas.FieldHealth(
                field_id=field.id,
                field_name=field.name,
                avg_soil_moisture=round(avg_soil, 1),
                avg_temperature=round(avg_temp, 1),
                avg_humidity=round(avg_hum, 1),
                total_rainfall_last_24h=round(rainfall_sum, 1),
                latest_recommendation=action
            ))
            
            if status in ("Critical", "Dry"):
                critical_count += 1
            soil_score = min(100, max(0, (avg_soil / 70) * 100 if avg_soil <= 70 else 100 - (avg_soil - 70)/0.3))
            total_health += soil_score
    
    overall_health = total_health / len(fields_summary) if fields_summary else 0
    
    return schemas.FarmHealthReport(
        farm_id=farm.id,
        farm_name=farm.name,
        overall_health_score=round(overall_health, 1),
        fields_summary=fields_summary,
        critical_irrigation_needed=critical_count
    )