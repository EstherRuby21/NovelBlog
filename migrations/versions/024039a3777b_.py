"""empty message

Revision ID: 024039a3777b
Revises: 9fdd210ad88d
Create Date: 2023-01-23 15:50:34.328678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024039a3777b'
down_revision = '9fdd210ad88d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('novels', sa.Column('overall_ating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('novels', 'overall_ating')
    # ### end Alembic commands ###
