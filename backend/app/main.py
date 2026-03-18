from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import coffees, descriptors, reviews, grinder_settings, tasters, scrape, grinders, brew_setups, origins, roasteries
from .seed import seed_database, seed_origins


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        seed_origins(db)
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
app.include_router(grinders.router)
app.include_router(brew_setups.router)
app.include_router(origins.router)
app.include_router(roasteries.router)
app.include_router(tasters.router)
app.include_router(scrape.router)


@app.get("/health")
def health():
    return {"status": "ok"}
