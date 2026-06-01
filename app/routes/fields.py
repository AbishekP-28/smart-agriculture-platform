from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/fields", tags=["Fields"])

@router.post("/", response_model=schemas.FieldResponse)
def create_field(field: schemas.FieldCreate, farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    db_field = models.Field(**field.dict(), farm_id=farm_id)
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field

@router.get("/", response_model=list[schemas.FieldResponse])
def list_fields(farm_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Field)
    if farm_id:
        query = query.filter(models.Field.farm_id == farm_id)
    return query.all()

@router.get("/{field_id}", response_model=schemas.FieldResponse)
def get_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field