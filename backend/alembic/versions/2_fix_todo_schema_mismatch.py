"""Fix todo table schema mismatch

Revision ID: 2_fix_todo_schema_mismatch
Revises: 1f050f102f42
Create Date: 2026-02-04 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2_fix_todo_schema_mismatch'
down_revision: Union[str, Sequence[str], None] = '1f050f102f42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to add missing columns and ensure proper types."""

    # Create enum types if they don't exist (PostgreSQL-safe approach)
    # Check if enum type exists first
    conn = op.get_bind()
    res = conn.execute(sa.text("""
        SELECT 1 FROM pg_type WHERE typname = 'todo_status_enum';
    """)).fetchone()

    if not res:
        op.execute("CREATE TYPE todo_status_enum AS ENUM ('pending', 'in_progress', 'completed')")

    # Check which columns already exist and only add missing ones
    columns_result = conn.execute(sa.text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'todo' AND table_schema = 'public';
    """))
    existing_columns = {row[0] for row in columns_result.fetchall()}

    # Add missing columns to todo table individually to handle existing columns gracefully
    if 'project_id' not in existing_columns:
        op.add_column('todo', sa.Column('project_id', postgresql.UUID(as_uuid=True),
                                        sa.ForeignKey('project.id'), nullable=True))

    if 'tags' not in existing_columns:
        op.add_column('todo', sa.Column('tags', sa.String(500), nullable=True))

    if 'reminder_time' not in existing_columns:
        op.add_column('todo', sa.Column('reminder_time', sa.DateTime(), nullable=True))

    # The status column might already exist, so we'll only add it if it doesn't exist
    if 'status' not in existing_columns:
        op.add_column('todo', sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='todo_status_enum'),
                                       nullable=False, server_default='pending'))

    # Due date and completed_at might already exist based on the output
    if 'due_date' not in existing_columns:
        op.add_column('todo', sa.Column('due_date', sa.DateTime(), nullable=True))

    if 'completed_at' not in existing_columns:
        op.add_column('todo', sa.Column('completed_at', sa.DateTime(), nullable=True))

    # Update existing todos to set proper status based on completed field
    # Only run this if the status column exists
    if 'status' not in existing_columns or 'completed' in existing_columns:
        op.execute("""
            UPDATE todo
            SET status = CASE
                WHEN completed = true THEN 'completed'
                ELSE 'pending'
            END
            WHERE status IS NULL OR status = ''
        """)


def downgrade() -> None:
    """Downgrade schema."""

    # Remove added columns from todo table
    with op.batch_alter_table('todo') as batch_op:
        batch_op.drop_column('completed_at')
        batch_op.drop_column('due_date')
        batch_op.drop_column('status')
        batch_op.drop_column('reminder_time')
        batch_op.drop_column('tags')
        batch_op.drop_column('project_id')

    # Drop enum type if it exists
    op.execute("DROP TYPE IF EXISTS todo_status_enum CASCADE")