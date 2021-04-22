"""empty message

Revision ID: 4320c7a94e60
Revises: 0163aa3294d3
Create Date: 2021-04-02 11:14:35.031592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4320c7a94e60'
down_revision = '0163aa3294d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('episode', sa.Column('overview', sa.Text(), nullable=True))
    op.add_column('episode', sa.Column('tmdb_id', sa.Integer(), nullable=True))
    op.add_column('serie', sa.Column('tmdb_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('serie', 'tmdb_id')
    op.drop_column('episode', 'tmdb_id')
    op.drop_column('episode', 'overview')
    # ### end Alembic commands ###