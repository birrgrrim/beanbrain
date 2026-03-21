"""add brew_setup_id to reviews

Revision ID: b597de861e84
Revises: 5f94067f351a
Create Date: 2026-03-21 18:45:19.318968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b597de861e84'
down_revision: Union[str, Sequence[str], None] = '5f94067f351a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add brew_setup_id to reviews, backfill with default brew setup."""
    # 1. Add column as nullable first
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brew_setup_id', sa.Integer(), nullable=True))

    # 2. Backfill: assign all existing reviews to the default brew setup
    conn = op.get_bind()
    default_setup = conn.execute(
        sa.text("SELECT id FROM brew_setups WHERE is_default = 1 LIMIT 1")
    ).scalar()

    if default_setup is None:
        # Fallback: use the first brew setup
        default_setup = conn.execute(
            sa.text("SELECT id FROM brew_setups ORDER BY id LIMIT 1")
        ).scalar()

    if default_setup is not None:
        conn.execute(
            sa.text("UPDATE reviews SET brew_setup_id = :sid WHERE brew_setup_id IS NULL"),
            {"sid": default_setup},
        )

    # 3. Recreate table with NOT NULL constraint, FK, and new unique constraint
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.alter_column('brew_setup_id', nullable=False)
        batch_op.create_foreign_key(
            'fk_review_brew_setup', 'brew_setups', ['brew_setup_id'], ['id']
        )
        batch_op.drop_constraint('uq_review_coffee_taster', type_='unique')
        batch_op.create_unique_constraint(
            'uq_review_coffee_taster_setup', ['coffee_id', 'taster_id', 'brew_setup_id']
        )


def downgrade() -> None:
    """Remove brew_setup_id from reviews, restore old unique constraint."""
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint('uq_review_coffee_taster_setup', type_='unique')
        batch_op.drop_constraint('fk_review_brew_setup', type_='foreignkey')
        batch_op.drop_column('brew_setup_id')
        batch_op.create_unique_constraint(
            'uq_review_coffee_taster', ['coffee_id', 'taster_id']
        )
