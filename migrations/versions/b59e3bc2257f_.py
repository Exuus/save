"""empty message

Revision ID: b59e3bc2257f
Revises: 3ea9c829191d
Create Date: 2017-12-19 15:42:25.062062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b59e3bc2257f'
down_revision = '3ea9c829191d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member_social_fund', sa.Column('amount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('member_social_fund', 'amount')
    # ### end Alembic commands ###
