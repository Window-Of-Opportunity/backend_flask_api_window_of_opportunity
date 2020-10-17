"""renamed_tables

Revision ID: f8e9dcb2659f
Revises: fa778c0cefcf
Create Date: 2020-10-04 19:33:58.072861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8e9dcb2659f'
down_revision = 'fa778c0cefcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing__address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street_address_1', sa.String(length=32), nullable=True),
    sa.Column('street_address_2', sa.String(length=32), nullable=True),
    sa.Column('zip_code', sa.String(length=16), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('country', sa.String(length=32), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mailing__address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street_address_1', sa.String(length=32), nullable=True),
    sa.Column('street_address_2', sa.String(length=32), nullable=True),
    sa.Column('zip_code', sa.String(length=16), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('country', sa.String(length=32), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('mailing_address')
    op.drop_table('biiling_address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('biiling_address',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('street_address_1', sa.VARCHAR(length=32), nullable=True),
    sa.Column('street_address_2', sa.VARCHAR(length=32), nullable=True),
    sa.Column('zip_code', sa.VARCHAR(length=16), nullable=True),
    sa.Column('state', sa.VARCHAR(length=2), nullable=True),
    sa.Column('country', sa.VARCHAR(length=32), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mailing_address',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('street_address_1', sa.VARCHAR(length=32), nullable=True),
    sa.Column('street_address_2', sa.VARCHAR(length=32), nullable=True),
    sa.Column('zip_code', sa.VARCHAR(length=16), nullable=True),
    sa.Column('state', sa.VARCHAR(length=2), nullable=True),
    sa.Column('country', sa.VARCHAR(length=32), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('mailing__address')
    op.drop_table('billing__address')
    # ### end Alembic commands ###
