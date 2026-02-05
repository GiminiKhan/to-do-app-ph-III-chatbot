"""Initial migration with User, Todo, and Project models

Revision ID: 1f050f102f42
Revises:
Create Date: 2026-02-01 01:32:30.711074

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '1f050f102f42'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum types for priority and status
    op.execute("CREATE TYPE todo_priority_enum AS ENUM ('low', 'medium', 'high', 'urgent')")
    op.execute("CREATE TYPE todo_status_enum AS ENUM ('pending', 'in_progress', 'completed')")

    # Create users table
    op.create_table('user',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )

    # Create projects table
    op.create_table('project',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('color', sa.String(7), nullable=False, default='#000000'),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )

    # Create todos table
    op.create_table('todo',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', 'urgent', name='todo_priority_enum'), nullable=False, default='medium'),
        sa.Column('completed', sa.Boolean, nullable=False, default=False),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='todo_status_enum'), nullable=False, default='pending'),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('project_id', UUID(as_uuid=True), sa.ForeignKey('project.id'), nullable=True),
        sa.Column('due_date', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop todos table
    op.drop_table('todo')

    # Drop projects table
    op.drop_table('project')

    # Drop users table
    op.drop_table('user')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS todo_priority_enum")
    op.execute("DROP TYPE IF EXISTS todo_status_enum")
