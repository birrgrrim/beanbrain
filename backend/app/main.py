from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from .database import Base, SessionLocal, engine
from .routers import coffees, descriptors, equipment, reviews, grinder_settings, tasters, scrape
from .seed import seed_database


def _migrate_metrics_to_int(db):
    """One-time migration: convert sweetness/acidity/bitterness from '7/10' strings to integers."""
    rows = db.execute(text(
        "SELECT id, sweetness, acidity, bitterness FROM coffees "
        "WHERE sweetness LIKE '%/%' OR acidity LIKE '%/%' OR bitterness LIKE '%/%'"
    )).fetchall()
    for row in rows:
        updates = {}
        for col in ("sweetness", "acidity", "bitterness"):
            val = getattr(row, col)
            if val and "/" in str(val):
                try:
                    updates[col] = int(str(val).split("/")[0])
                except (ValueError, IndexError):
                    updates[col] = None
        if updates:
            set_clause = ", ".join(f"{k} = :{k}" for k in updates)
            db.execute(text(f"UPDATE coffees SET {set_clause} WHERE id = :id"), {**updates, "id": row.id})
    if rows:
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        _migrate_metrics_to_int(db)
    finally:
        db.close()
    yield


app = FastAPI(title="BeanBrain", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coffees.router)
app.include_router(reviews.router)
app.include_router(grinder_settings.router)
app.include_router(descriptors.router)
app.include_router(equipment.router)
app.include_router(tasters.router)
app.include_router(scrape.router)


@app.get("/health")
def health():
    return {"status": "ok"}
