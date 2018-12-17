"""added img in Section

Revision ID: d951fd338943
Revises: 23bd4997ac89
Create Date: 2018-12-15 23:01:17.125914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd951fd338943'
down_revision = '23bd4997ac89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section', sa.Column('image', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('section', 'image')
    # ### end Alembic commands ###