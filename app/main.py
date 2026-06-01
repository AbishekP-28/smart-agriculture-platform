from fastapi import FastAPI
from app.database import engine, Base
from app.routes import farms, fields, readings, recommendations, reports, analytics, simulate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Agriculture Monitoring Platform")

app.include_router(farms.router)
app.include_router(fields.router)
app.include_router(readings.router)
app.include_router(recommendations.router)
app.include_router(reports.router)
app.include_router(analytics.router)
app.include_router(simulate.router)

@app.get("/")
def root():
    return {"message": "Smart Agriculture API is running"}