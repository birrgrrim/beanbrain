"""baseline schema

Revision ID: 3817fe24fdf7
Revises: 
Create Date: 2026-03-21 15:33:53.424559

"""
from typing import Sequence, Union

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = '3817fe24fdf7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Baseline — no-op. Existing databases already have this schema."""
    pass


def downgrade() -> None:
    """Baseline has no downgrade."""
    pass
