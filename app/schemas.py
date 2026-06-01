from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# Farm schemas
class FarmBase(BaseModel):
    name: str
    location: Optional[str] = None

class FarmCreate(FarmBase):
    pass

class FarmResponse(FarmBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Field schemas
class FieldBase(BaseModel):
    name: str
    area_ha: Optional[float] = 0.0
    crop_type: Optional[str] = None

class FieldCreate(FieldBase):
    pass

class FieldResponse(FieldBase):
    id: int
    farm_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# SensorReading schemas
class SensorReadingBase(BaseModel):
    soil_moisture: float = Field(..., ge=0, le=100)
    humidity: float = Field(..., ge=0, le=100)
    temperature: float = Field(..., ge=-10, le=60)
    rainfall: float = Field(..., ge=0)

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingResponse(SensorReadingBase):
    id: int
    field_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Recommendation response
class RecommendationResponse(BaseModel):
    field_id: int
    field_name: str
    latest_reading: SensorReadingResponse
    soil_moisture_status: str
    action: str
    message: str
    timestamp: datetime

# Farm health report
class FieldHealth(BaseModel):
    field_id: int
    field_name: str
    avg_soil_moisture: float
    avg_temperature: float
    avg_humidity: float
    total_rainfall_last_24h: float
    latest_recommendation: str

class FarmHealthReport(BaseModel):
    farm_id: int
    farm_name: str
    overall_health_score: float
    fields_summary: List[FieldHealth]
    critical_irrigation_needed: int

# Analytics
class DashboardSummary(BaseModel):
    total_farms: int
    total_fields: int
    average_soil_moisture: float
    average_temperature: float
    fields_needing_irrigation: int

class TrendPoint(BaseModel):
    timestamp: datetime
    soil_moisture: float
    temperature: float
    rainfall: float