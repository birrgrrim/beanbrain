from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import coffees, descriptors, equipment, tastings, grinder_settings, tasters, scrape
from .seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
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
app.include_router(tastings.router)
app.include_router(grinder_settings.router)
app.include_router(descriptors.router)
app.include_router(equipment.router)
app.include_router(tasters.router)
app.include_router(scrape.router)


@app.get("/health")
def health():
    return {"status": "ok"}
