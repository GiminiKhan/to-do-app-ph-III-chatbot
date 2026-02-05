#!/usr/bin/env python3
"""
Script to add missing columns to the Neon database that weren't properly migrated.
"""

import os
from sqlalchemy import create_engine, text
from src.core.config import settings

def add_missing_columns():
    """Add missing columns to the Neon database."""
    print("Connecting to Neon database...")

    # Connect to the Neon database using the settings
    engine = create_engine(settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://'))

    # Check if enum type exists, create if not
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 1 FROM pg_type WHERE typname = 'todo_status_enum';
        """)).fetchone()

        if not result:
            print("Creating todo_status_enum...")
            conn.execute(text("CREATE TYPE todo_status_enum AS ENUM ('pending', 'in_progress', 'completed')"))
            conn.commit()
            print("Enum type created successfully.")

    # Add missing columns one by one
    missing_columns = [
        ("project_id", "UUID REFERENCES project(id)", "project_id column"),
        ("tags", "VARCHAR(500)", "tags column"),
        ("reminder_time", "TIMESTAMP", "reminder_time column")
    ]

    with engine.connect() as conn:
        for col_name, col_type, col_desc in missing_columns:
            try:
                print(f"Adding {col_desc}...")
                # Check if column exists first
                exists_query = text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'todo' AND column_name = :col_name;
                """)
                result = conn.execute(exists_query, {"col_name": col_name}).fetchone()

                if not result:
                    alter_query = text(f"ALTER TABLE todo ADD COLUMN {col_name} {col_type};")
                    conn.execute(alter_query)
                    conn.commit()
                    print(f"[SUCCESS] {col_desc} added successfully")
                else:
                    print(f"[WARNING] {col_desc} already exists")

            except Exception as e:
                print(f"[ERROR] Failed to add {col_desc}: {str(e)}")

    print("\n[INFO] Column addition process completed.")

if __name__ == "__main__":
    add_missing_columns()