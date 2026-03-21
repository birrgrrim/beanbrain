"""rename equipment fields manufacturer model

Revision ID: 5f94067f351a
Revises: 5708f4e75ba9
Create Date: 2026-03-21 17:41:55.022406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f94067f351a'
down_revision: Union[str, Sequence[str], None] = '5708f4e75ba9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename grinder.name -> manufacturer, brew_setup.name -> manufacturer + add model."""
    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.alter_column('name', new_column_name='manufacturer')

    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.alter_column('name', new_column_name='manufacturer')
        batch_op.add_column(sa.Column('model', sa.String(), nullable=True))


def downgrade() -> None:
    """Revert: manufacturer -> name, drop brew_setup.model."""
    with op.batch_alter_table('brew_setups', schema=None) as batch_op:
        batch_op.drop_column('model')
        batch_op.alter_column('manufacturer', new_column_name='name')

    with op.batch_alter_table('grinders', schema=None) as batch_op:
        batch_op.alter_column('manufacturer', new_column_name='name')
