from app import __version__
from app.models import SchemaVersion


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_schema_version_table_exists(client):
    """Schema version table is created and can store a version."""
    from app.database import get_db
    from app.main import app

    db = next(app.dependency_overrides[get_db]())
    db.add(SchemaVersion(version=__version__))
    db.commit()
    row = db.query(SchemaVersion).first()
    assert row.version == __version__
    assert row.applied_at is not None
