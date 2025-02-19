"""create tables

Revision ID: 36cf362a7ae7
Revises:
Create Date: 2025-02-18 20:27:35.152106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36cf362a7ae7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'payment',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('external_id', sa.String(length=120), nullable=False),
        sa.Column('status', sa.String(length=60), nullable=False),
        sa.Column('value', sa.Numeric(10, 2), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_customer')),
        sa.UniqueConstraint('external_id', name=op.f('uq_external_id'))
    )


def downgrade() -> None:
    op.drop_table('payment')
