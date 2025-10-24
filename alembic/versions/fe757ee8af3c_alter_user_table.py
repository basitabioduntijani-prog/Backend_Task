"""alter user table

Revision ID: 089e38c1141a
Revises: 
Create Date: 2025-10-23 11:20:58.234915

"""
from typing import Sequence, Union
from alembic import op 
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '089e38c1141a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE users
    ADD COLUMN userType varchar(100) DEFAULT 'student'
""")
    pass


def downgrade() -> None:
    op.execute("""
    ALTER TABLE users
    DROP COLUMN userType
""")
    pass
