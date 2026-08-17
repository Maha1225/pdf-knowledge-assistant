"""add document chunks and embeddings

Revision ID: 07ed92724dff
Revises: f9e86caf0550
Create Date: 2026-08-17 09:26:41.361174

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "07ed92724dff"
down_revision: Union[str, Sequence[str], None] = "f9e86caf0550"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Make sure PostgreSQL has the pgvector extension.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "document_chunks",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "document_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "page_number",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "text",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "embedding",
            Vector(384),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_document_chunks_document_id"),
        "document_chunks",
        ["document_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_document_chunks_document_id"),
        table_name="document_chunks",
    )

    op.drop_table("document_chunks")
