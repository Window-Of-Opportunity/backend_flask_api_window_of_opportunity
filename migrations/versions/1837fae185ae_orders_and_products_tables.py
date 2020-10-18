"""orders and products tables

Revision ID: 1837fae185ae
Revises: f8e9dcb2659f
Create Date: 2020-10-17 01:47:21.349003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1837fae185ae'
down_revision = 'f8e9dcb2659f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('window_type', sa.String(length=32), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('color', sa.String(length=32), nullable=True),
    sa.Column('manufacturer', sa.String(length=32), nullable=True),
    sa.Column('pane_width', sa.Integer(), nullable=True),
    sa.Column('num_panes', sa.Integer(), nullable=True),
    sa.Column('obscured', sa.Boolean(), nullable=True),
    sa.Column('tempered', sa.Boolean(), nullable=True),
    sa.Column('gas_fill_type', sa.String(length=16), nullable=True),
    sa.Column('lowe3', sa.Boolean(), nullable=True),
    sa.Column('frame_material', sa.String(length=64), nullable=True),
    sa.Column('nailing_flange', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cust_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cust_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('window')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('window',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('window_type', sa.VARCHAR(length=32), nullable=True),
    sa.Column('width', sa.INTEGER(), nullable=True),
    sa.Column('height', sa.INTEGER(), nullable=True),
    sa.Column('color', sa.VARCHAR(length=32), nullable=True),
    sa.Column('manufacturer', sa.VARCHAR(length=32), nullable=True),
    sa.Column('pane_width', sa.INTEGER(), nullable=True),
    sa.Column('num_panes', sa.INTEGER(), nullable=True),
    sa.Column('obscured', sa.BOOLEAN(), nullable=True),
    sa.Column('tempered', sa.BOOLEAN(), nullable=True),
    sa.Column('gas_fill_type', sa.VARCHAR(length=16), nullable=True),
    sa.Column('lowe3', sa.BOOLEAN(), nullable=True),
    sa.Column('frame_material', sa.VARCHAR(length=64), nullable=True),
    sa.Column('nailing_flange', sa.BOOLEAN(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.CheckConstraint('lowe3 IN (0, 1)'),
    sa.CheckConstraint('nailing_flange IN (0, 1)'),
    sa.CheckConstraint('obscured IN (0, 1)'),
    sa.CheckConstraint('tempered IN (0, 1)'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('order_item')
    op.drop_table('order')
    op.drop_table('product')
    # ### end Alembic commands ###