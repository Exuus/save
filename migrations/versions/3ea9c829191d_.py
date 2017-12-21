"""empty message

Revision ID: 3ea9c829191d
Revises: 8cc2a2cc7663
Create Date: 2017-12-19 15:38:30.115933

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ea9c829191d'
down_revision = '8cc2a2cc7663'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member_social_fund', sa.Column('external_transaction_id', sa.String(length=30), nullable=True))
    op.add_column('member_social_fund', sa.Column('operator_transaction_id', sa.String(length=30), nullable=True))
    op.create_unique_constraint(None, 'member_social_fund', ['external_transaction_id'])
    op.create_unique_constraint(None, 'member_social_fund', ['operator_transaction_id'])
    op.drop_column('member_social_fund', 'amount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member_social_fund', sa.Column('amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'member_social_fund', type_='unique')
    op.drop_constraint(None, 'member_social_fund', type_='unique')
    op.drop_column('member_social_fund', 'operator_transaction_id')
    op.drop_column('member_social_fund', 'external_transaction_id')
    # ### end Alembic commands ###
