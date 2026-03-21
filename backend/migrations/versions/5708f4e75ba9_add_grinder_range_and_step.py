"""add grinder range and step

Revision ID: 5708f4e75ba9
Revises: 3817fe24fdf7
Create Date: 2026-03-21 16:24:10.779592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5708f4e75ba9'
down_revision: Union[str, Sequence[str], None] = '3817fe24fdf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add range_min, range_max, step columns to grinders."""
    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('range_min', sa.Float(), server_default='0'))
        batch_op.add_column(sa.Column('range_max', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('step', sa.Float(), server_default='1'))


def downgrade() -> None:
    """Remove range_min, range_max, step columns from grinders."""
    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.drop_column('step')
        batch_op.drop_column('range_max')
        batch_op.drop_column('range_min')
