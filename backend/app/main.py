from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import coffees, descriptors, equipment, tastings, grinder_settings
from .seed import seed_database

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeanBrain", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


app.include_router(coffees.router)
app.include_router(tastings.router)
app.include_router(grinder_settings.router)
app.include_router(descriptors.router)
app.include_router(equipment.router)


@app.get("/health")
def health():
    return {"status": "ok"}
