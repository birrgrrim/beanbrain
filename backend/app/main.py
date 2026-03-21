import os
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .database import SessionLocal
from .routers import coffees, descriptors, reviews, grinder_settings, tasters, scrape, grinders, brew_setups, origins, roasteries
from .seed import seed_database, seed_origins


def _run_migrations() -> None:
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.environ.get("TESTING"):
        _run_migrations()
        db = SessionLocal()
        try:
            seed_database(db)
            seed_origins(db)
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
