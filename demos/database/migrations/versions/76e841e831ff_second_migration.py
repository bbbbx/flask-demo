"""second migration

Revision ID: 76e841e831ff
Revises: a419561685dc
Create Date: 2019-01-07 13:41:39.573149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e841e831ff'
down_revision = 'a419561685dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'gender')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gender', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###