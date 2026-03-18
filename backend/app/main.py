from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import inspect, text

from .database import Base, SessionLocal, engine
from .models import BrewSetup, Grinder
from .routers import coffees, descriptors, reviews, grinder_settings, tasters, scrape, grinders, brew_setups
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


def _migrate_equipment_to_grinders_and_setups(db):
    """One-time migration: convert old Equipment/BrewMethod/BasketSize to Grinder/BrewSetup."""
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    # Add kind column to grinders if missing
    if "grinders" in table_names:
        grinder_cols = {col["name"] for col in inspector.get_columns("grinders")}
        if "kind" not in grinder_cols:
            db.execute(text("ALTER TABLE grinders ADD COLUMN kind VARCHAR DEFAULT 'auto'"))
            db.commit()

    # Rebuild grinder_settings table if it still has old columns
    if "grinder_settings" in table_names:
        gs_columns = {col["name"] for col in inspector.get_columns("grinder_settings")}
        if "equipment_id" in gs_columns:
            # Add new columns if missing (needed before rebuild to copy data)
            if "grinder_id" not in gs_columns:
                db.execute(text("ALTER TABLE grinder_settings ADD COLUMN grinder_id INTEGER REFERENCES grinders(id)"))
            if "brew_setup_id" not in gs_columns:
                db.execute(text("ALTER TABLE grinder_settings ADD COLUMN brew_setup_id INTEGER REFERENCES brew_setups(id)"))
            db.commit()

            # Rebuild table with new schema (drops old NOT NULL columns)
            db.execute(text("ALTER TABLE grinder_settings RENAME TO _gs_old"))
            db.execute(text("""
                CREATE TABLE grinder_settings (
                    id INTEGER PRIMARY KEY,
                    coffee_id INTEGER NOT NULL REFERENCES coffees(id) ON DELETE CASCADE,
                    grinder_id INTEGER NOT NULL REFERENCES grinders(id),
                    brew_setup_id INTEGER NOT NULL REFERENCES brew_setups(id),
                    setting FLOAT NOT NULL,
                    notes VARCHAR
                )
            """))
            db.execute(text("CREATE INDEX ix_grinder_settings_id ON grinder_settings (id)"))
            db.execute(text("""
                INSERT INTO grinder_settings (id, coffee_id, grinder_id, brew_setup_id, setting, notes)
                SELECT id, coffee_id, grinder_id, brew_setup_id, setting, notes
                FROM _gs_old
                WHERE grinder_id IS NOT NULL AND brew_setup_id IS NOT NULL
            """))
            db.execute(text("DROP TABLE _gs_old"))
            db.commit()

    # Only migrate data if old tables exist and new tables are empty
    if "equipment" not in table_names:
        return
    if db.query(Grinder).first() is not None:
        return

    # Migrate grinders from equipment
    old_grinders = db.execute(text(
        "SELECT id, name, model, is_default FROM equipment WHERE type = 'grinder' AND is_active = 1"
    )).fetchall()
    grinder_id_map = {}
    for og in old_grinders:
        g = Grinder(name=og.name, model=og.model, is_default=bool(og.is_default))
        db.add(g)
        db.flush()
        grinder_id_map[og.id] = g.id

    # Migrate brew setups from brew methods + machines + baskets
    old_methods = db.execute(text("SELECT id, name, is_default FROM brew_methods")).fetchall()
    old_machines = db.execute(text(
        "SELECT id, name, is_default FROM equipment WHERE type = 'machine' AND is_active = 1"
    )).fetchall()
    old_baskets = db.execute(text("SELECT id, size_grams, label, is_default FROM basket_sizes")).fetchall()

    brew_setup_map = {}  # (old_method_id, old_basket_id or None) -> new brew_setup_id

    for method in old_methods:
        method_name_lower = method.name.lower()
        if method_name_lower == "espresso":
            # Create one BrewSetup per machine+basket combo
            for machine in old_machines:
                for basket in old_baskets:
                    name = f"{machine.name}, {basket.label}"
                    is_def = bool(method.is_default and machine.is_default and basket.is_default)
                    bs = BrewSetup(
                        method_type="espresso", name=name,
                        basket_grams=basket.size_grams, is_default=is_def,
                    )
                    db.add(bs)
                    db.flush()
                    brew_setup_map[(method.id, basket.id)] = bs.id
            if not old_machines:
                # No machines — create per basket
                for basket in old_baskets:
                    bs = BrewSetup(
                        method_type="espresso", name=f"Espresso, {basket.label}",
                        basket_grams=basket.size_grams, is_default=bool(method.is_default and basket.is_default),
                    )
                    db.add(bs)
                    db.flush()
                    brew_setup_map[(method.id, basket.id)] = bs.id
        else:
            # Non-espresso: one BrewSetup per method
            method_type = method_name_lower.replace(" ", "")
            # Map to known keys if possible
            type_map = {"pourover": "pourover", "aeropress": "aeropress",
                        "frenchpress": "frenchpress", "moka": "moka", "cezve": "cezve"}
            mt = type_map.get(method_type, "pourover")
            bs = BrewSetup(
                method_type=mt, name=method.name,
                is_default=bool(method.is_default),
            )
            db.add(bs)
            db.flush()
            brew_setup_map[(method.id, None)] = bs.id

    # Rewire grinder_settings
    old_settings = db.execute(text(
        "SELECT id, equipment_id, brew_method_id, basket_size_id FROM grinder_settings"
    )).fetchall()
    for os in old_settings:
        new_grinder_id = grinder_id_map.get(os.equipment_id)
        if not new_grinder_id:
            continue
        new_setup_id = brew_setup_map.get((os.brew_method_id, os.basket_size_id))
        if not new_setup_id:
            new_setup_id = brew_setup_map.get((os.brew_method_id, None))
        if not new_setup_id:
            continue
        db.execute(text(
            "UPDATE grinder_settings SET grinder_id = :gid, brew_setup_id = :sid WHERE id = :id"
        ), {"gid": new_grinder_id, "sid": new_setup_id, "id": os.id})

    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        _migrate_metrics_to_int(db)
        _migrate_equipment_to_grinders_and_setups(db)
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
app.include_router(tasters.router)
app.include_router(scrape.router)


@app.get("/health")
def health():
    return {"status": "ok"}
