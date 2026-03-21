"""drop is_default from grinders and brew_setups

Revision ID: 34823d51c675
Revises: 1692efa4dbc4
Create Date: 2026-03-22 00:14:37.277638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34823d51c675'
down_revision: Union[str, Sequence[str], None] = '1692efa4dbc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove is_default column from grinders and brew_setups."""
    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.drop_column('is_default')

    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.drop_column('is_default')


def downgrade() -> None:
    """Re-add is_default column."""
    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_default', sa.Boolean(), server_default='0'))

    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_default', sa.Boolean(), server_default='0'))
