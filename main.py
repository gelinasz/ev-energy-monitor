from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy.orm import Session

from datetime import datetime

from database import get_db
from models import Sensor as SensorModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SensorCreate(BaseModel):
    name: str
    voltage: float = Field(ge=0)
    current: float = Field(ge=0)
    power_kw: float = Field(ge=0)
    temperature: float
    status: str


class SensorOut(BaseModel):
    id: int
    name: str
    voltage: float
    current: float
    power_kw: float
    temperature: float
    status: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def root():
    return {"message": "EV energy monitoring system online"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "system": "ev-energy-monitor",
        "version": "0.2.0"
    }


@app.post("/sensors", response_model=SensorOut)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    new_sensor = SensorModel(**sensor.model_dump())
    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)
    return new_sensor


@app.get("/sensors", response_model=list[SensorOut])
def get_sensors(db: Session = Depends(get_db)):
    return db.query(SensorModel).all()
CHARGER_PRIORITIES = {
    "Charger-01": 1,
    "Charger-02": 2
}
SITE_POWER_LIMIT_KW = 150
STALE_THRESHOLD_SECONDS = 15

@app.get("/site/power")
def get_site_power(db: Session = Depends(get_db)):
    chargers = db.query(SensorModel).all()

    latest_readings = {}

    for charger in chargers:
        latest_readings[charger.name] = charger

    total_power = sum(
        charger.power_kw
        for charger in latest_readings.values()
    )

    return {
        "site_power_limit_kw": SITE_POWER_LIMIT_KW,
        "current_power_kw": round(total_power, 2),
        "available_power_kw": round(
            SITE_POWER_LIMIT_KW - total_power, 2
        ),
        "over_limit": total_power > SITE_POWER_LIMIT_KW
    }


@app.get("/site/power/recommendation")
def get_power_recommendation(db: Session = Depends(get_db)):
    chargers = db.query(SensorModel).all()

    latest_readings = {}

    for charger in chargers:
        latest_readings[charger.name] = charger

    total_power = sum(
        charger.power_kw
        for charger in latest_readings.values()
    )

    if total_power <= SITE_POWER_LIMIT_KW:
        return {
            "status": "normal",
            "action": "none",
            "power_to_reduce_kw": 0
        }

    power_to_reduce = total_power - SITE_POWER_LIMIT_KW

    # Find the lowest-priority charger that is currently charging
    candidates = [
        charger
        for charger in latest_readings.values()
        if charger.status == "charging"
    ]

    candidates.sort(
        key=lambda charger: CHARGER_PRIORITIES.get(
            charger.name, 999
        ),
        reverse=True
    )

    if not candidates:
        return {
            "status": "over_limit",
            "action": "reduce_charging",
            "power_to_reduce_kw": round(power_to_reduce, 2),
            "target_charger": None
        }

    target = candidates[0]

    return {
        "status": "over_limit",
        "action": "reduce_charging",
        "power_to_reduce_kw": round(power_to_reduce, 2),
        "target_charger": target.name,
        "target_charger_power_kw": round(target.power_kw, 2),
        "target_priority": CHARGER_PRIORITIES.get(
            target.name, 999
        )
    }
@app.get("/site/health")
def get_site_health(db: Session = Depends(get_db)):
    chargers = db.query(SensorModel).all()

    latest_readings = {}

    for charger in chargers:
        latest_readings[charger.name] = charger

    now = datetime.utcnow()

    results = []

    for charger in latest_readings.values():
        age_seconds = (now - charger.timestamp).total_seconds()

        results.append({
    "charger": charger.name,
    "last_seen": charger.timestamp,
    "age_seconds": round(age_seconds, 1),
    "status": "stale" if age_seconds > STALE_THRESHOLD_SECONDS else "fresh",
    "action": "check_connection" if age_seconds > STALE_THRESHOLD_SECONDS else "none"
})

    return {
        "chargers": results
    }