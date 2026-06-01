from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app import models, schemas
from app.database import get_db
from app.recommendation import get_recommendation_text

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard-summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    total_farms = db.query(models.Farm).count()
    total_fields = db.query(models.Field).count()
    
    avg_moisture = db.query(func.avg(models.SensorReading.soil_moisture)).scalar() or 0.0
    avg_temp = db.query(func.avg(models.SensorReading.temperature)).scalar() or 0.0
    
    fields_need = 0
    fields = db.query(models.Field).all()
    for field in fields:
        latest = db.query(models.SensorReading).filter(
            models.SensorReading.field_id == field.id
        ).order_by(models.SensorReading.timestamp.desc()).first()
        if latest:
            status, _, _ = get_recommendation_text(latest.soil_moisture, 0)
            if status in ("Critical", "Dry"):
                fields_need += 1
    
    return schemas.DashboardSummary(
        total_farms=total_farms,
        total_fields=total_fields,
        average_soil_moisture=round(avg_moisture, 1),
        average_temperature=round(avg_temp, 1),
        fields_needing_irrigation=fields_need
    )

@router.get("/field-trend/{field_id}", response_model=list[schemas.TrendPoint])
def field_trend(field_id: int, days: int = Query(7, ge=1, le=30), db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    since = datetime.utcnow() - timedelta(days=days)
    readings = db.query(models.SensorReading).filter(
        models.SensorReading.field_id == field_id,
        models.SensorReading.timestamp >= since
    ).order_by(models.SensorReading.timestamp.asc()).all()
    
    return [schemas.TrendPoint(
        timestamp=r.timestamp,
        soil_moisture=r.soil_moisture,
        temperature=r.temperature,
        rainfall=r.rainfall
    ) for r in readings]