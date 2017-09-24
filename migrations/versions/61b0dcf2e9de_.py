"""empty message

Revision ID: 61b0dcf2e9de
Revises: d50b3b510f98
Create Date: 2017-09-22 16:49:50.855615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61b0dcf2e9de'
down_revision = 'd50b3b510f98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member_fine', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member_fine', sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
