"""create customer table

Revision ID: b03c4b2a9e49
Revises: 69ad2238f2f5
Create Date: 2025-03-10 22:22:03.963373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b03c4b2a9e49'
down_revision: Union[str, None] = '69ad2238f2f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('money', sa.Integer, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('customer')
