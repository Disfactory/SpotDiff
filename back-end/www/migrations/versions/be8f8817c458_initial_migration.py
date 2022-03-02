"""initial migration

Revision ID: be8f8817c458
Revises: 
Create Date: 2022-03-02 14:51:57.654860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be8f8817c458'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('factory_id', sa.String(length=255), nullable=False),
    sa.Column('done_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_location'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('client_id', sa.String(length=255), nullable=False),
    sa.Column('client_type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('client_id', name=op.f('uq_user_client_id'))
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('year_old', sa.Integer(), nullable=False),
    sa.Column('year_new', sa.Integer(), nullable=False),
    sa.Column('source_url_root', sa.String(), nullable=False),
    sa.Column('land_usage', sa.Integer(), nullable=False),
    sa.Column('expansion', sa.Integer(), nullable=False),
    sa.Column('gold_standard_status', sa.Integer(), nullable=False),
    sa.Column('bbox_left_top_lat', sa.Float(), nullable=True),
    sa.Column('bbox_left_top_lng', sa.Float(), nullable=True),
    sa.Column('bbox_bottom_right_lat', sa.Float(), nullable=True),
    sa.Column('bbox_bottom_right_lng', sa.Float(), nullable=True),
    sa.Column('zoom_level', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name=op.f('fk_answer_location_id_location')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_answer_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_answer'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('user')
    op.drop_table('location')
    # ### end Alembic commands ###
