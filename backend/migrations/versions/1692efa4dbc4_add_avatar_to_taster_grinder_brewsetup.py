"""add avatar to taster grinder brewsetup

Revision ID: 1692efa4dbc4
Revises: b597de861e84
Create Date: 2026-03-21 20:39:24.207763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1692efa4dbc4'
down_revision: Union[str, Sequence[str], None] = 'b597de861e84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add avatar column to tasters, grinders, and brew_setups."""
    with op.batch_alter_table('tasters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))

    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))

    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove avatar columns."""
    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    with op.batch_alter_table('tasters', schema=None) as batch_op:
        batch_op.drop_column('avatar')
