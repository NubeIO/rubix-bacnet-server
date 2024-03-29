"""empty message

Revision ID: 68f2a7e4c892
Revises: 2dadff3c2b25
Create Date: 2021-07-06 12:31:17.828893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68f2a7e4c892'
down_revision = '2dadff3c2b25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mappings_bp_gp', schema=None) as batch_op:
        batch_op.alter_column('bacnet_point_uuid', new_column_name='point_uuid')
        batch_op.alter_column('bacnet_point_name', new_column_name='point_name')
        batch_op.alter_column('generic_point_uuid', new_column_name='mapped_point_uuid')
        batch_op.alter_column('generic_point_name', new_column_name='mapped_point_name')
        batch_op.add_column(
            sa.Column('mapping_state', sa.Enum('MAPPED', 'BROKEN', name='mappingstate'), server_default="MAPPED"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mappings_bp_gp', schema=None) as batch_op:
        batch_op.alter_column('point_uuid', new_column_name='bacnet_point_uuid')
        batch_op.alter_column('point_name', new_column_name='bacnet_point_name')
        batch_op.alter_column('mapped_point_uuid', new_column_name='generic_point_uuid')
        batch_op.alter_column('mapped_point_name', new_column_name='generic_point_name')
        batch_op.drop_column('mapping_state')

    # ### end Alembic commands ###
