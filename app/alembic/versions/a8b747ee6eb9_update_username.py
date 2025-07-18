"""update username

Revision ID: a8b747ee6eb9
Revises: 0721676060d6
Create Date: 2025-06-04 23:20:56.733387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a8b747ee6eb9'
down_revision: Union[str, None] = '0721676060d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False))
    op.drop_index('ix_user_full_name', table_name='user')
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', mysql.VARCHAR(length=255), nullable=False))
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.create_index('ix_user_full_name', 'user', ['full_name'], unique=True)
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
