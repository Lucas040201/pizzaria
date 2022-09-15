"""Removendo a coluna salt

Revision ID: c78d53a26f7f
Revises: ccd78551dabb
Create Date: 2022-09-12 23:02:45.217820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c78d53a26f7f'
down_revision = 'ccd78551dabb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'salt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('salt', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###