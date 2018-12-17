"""init

Revision ID: 23bd4997ac89
Revises: 
Create Date: 2018-12-15 22:44:43.390725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23bd4997ac89'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('image', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('show_in_view', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('command',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('default_value', sa.String(length=64), nullable=True),
    sa.Column('current_value', sa.String(length=64), nullable=True),
    sa.Column('value_type', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type'], ['section.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('section_maps',
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('map_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['map_id'], ['map.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.PrimaryKeyConstraint('section_id', 'map_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('section_maps')
    op.drop_table('command')
    op.drop_table('section')
    op.drop_table('map')
    # ### end Alembic commands ###