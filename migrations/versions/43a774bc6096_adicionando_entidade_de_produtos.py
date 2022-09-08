"""adicionando entidade de produtos

Revision ID: 43a774bc6096
Revises: 34a7af3d0a25
Create Date: 2022-09-07 23:48:01.414923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43a774bc6096'
down_revision = '34a7af3d0a25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###