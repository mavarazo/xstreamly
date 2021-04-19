"""empty message

Revision ID: 0163aa3294d3
Revises: 
Create Date: 2021-04-01 13:37:46.414870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0163aa3294d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('serie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('overview', sa.Text(), nullable=True),
    sa.Column('poster', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('episode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('serie_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('season_nr', sa.Integer(), nullable=True),
    sa.Column('episode_nr', sa.Integer(), nullable=True),
    sa.Column('origin_name', sa.String(length=255), nullable=True),
    sa.Column('origin_url', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('episode')
    op.drop_table('serie')
    # ### end Alembic commands ###
