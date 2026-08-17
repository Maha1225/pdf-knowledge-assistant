from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


def get_document_by_hash(
    db: Session,
    content_hash: str,
) -> Document | None:
    return db.scalar(
        select(Document).where(
            Document.content_hash == content_hash
        )
    )


def get_document(
    db: Session,
    document_id,
) -> Document | None:
    return db.get(Document, document_id)


def create_document(
    db: Session,
    document: Document,
) -> Document:
    db.add(document)
    db.commit()
    db.refresh(document)

    return document