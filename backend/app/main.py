import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .database import Base, SessionLocal, engine
from .models import SchemaVersion
from .routers import coffees, descriptors, reviews, grinder_settings, tasters, scrape, grinders, brew_setups, origins, roasteries
from .seed import seed_database, seed_origins


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        seed_origins(db)
        # Stamp current version
        row = db.query(SchemaVersion).first()
        if row:
            row.version = __version__
        else:
            db.add(SchemaVersion(version=__version__))
        db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title="BeanBrain", version=__version__, lifespan=lifespan)

cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coffees.router)
app.include_router(reviews.router)
app.include_router(grinder_settings.router)
app.include_router(descriptors.router)
app.include_router(grinders.router)
app.include_router(brew_setups.router)
app.include_router(origins.router)
app.include_router(roasteries.router)
app.include_router(tasters.router)
app.include_router(scrape.router)


@app.get("/health")
def health():
    return {"status": "ok"}
