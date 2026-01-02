"""Initial migration

Revision ID: 6fe0f9a9b6b4
Revises: ecc357d873c7
Create Date: 2026-01-02 22:22:14.972006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fe0f9a9b6b4'
down_revision: Union[str, Sequence[str], None] = 'ecc357d873c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
