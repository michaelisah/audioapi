"""empty message

Revision ID: 0d6eb5295c5d
Revises: 
Create Date: 2021-03-12 04:13:45.646637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d6eb5295c5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio_model',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('fileType', sa.String(length=100), nullable=True),
    sa.Column('metaData', sa.Text(), nullable=False),
    sa.Column('uploadedTime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audio_model')
    # ### end Alembic commands ###
