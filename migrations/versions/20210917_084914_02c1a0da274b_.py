"""empty message

Revision ID: 02c1a0da274b
Revises: 4baa25e7dd4a
Create Date: 2021-09-17 08:49:14.004751

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '02c1a0da274b'
down_revision = '4baa25e7dd4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bac_server', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enable_ip_by_nic_name', sa.Boolean(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column('ip_by_nic_name', sa.String(length=80), nullable=False, server_default=""))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bac_server', schema=None) as batch_op:
        batch_op.drop_column('ip_by_nic_name')
        batch_op.drop_column('enable_ip_by_nic_name')

    # ### end Alembic commands ###
