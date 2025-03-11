"""create shop table

Revision ID: 69ad2238f2f5
Revises: 
Create Date: 2025-03-10 22:17:40.204909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69ad2238f2f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'shop',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('shop')
