"""add last_password_change to user

Revision ID: 629a2bd5720a
Revises: 517a245b1ee5
Create Date: 2025-06-08 22:46:11.669716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '629a2bd5720a'
down_revision: Union[str, None] = '517a245b1ee5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_password_change', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_password_change')
    # ### end Alembic commands ###
