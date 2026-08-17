import hashlib
import uuid
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_page import DocumentPage
from app.models.document_chunk import DocumentChunk
from app.models.ingestion_job import IngestionJob
from app.repositories.document_repository import get_document_by_hash
from app.rag.embeddings.service import generate_embedding
from app.rag.ingestion.chunker import chunk_text


UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def ingest_pdf(
    db: Session,
    filename: str,
    file_bytes: bytes,
):
    # 1. Calculate SHA-256 hash
    content_hash = hashlib.sha256(file_bytes).hexdigest()

    # 2. Prevent duplicate PDFs
    existing = get_document_by_hash(db, content_hash)

    if existing:
        return existing, False

    # 3. Generate stored filename
    document_id = uuid.uuid4()

    stored_filename = f"{document_id}.pdf"
    file_path = UPLOAD_DIR / stored_filename

    file_path.write_bytes(file_bytes)

    try:
        # 4. Read PDF
        reader = PdfReader(str(file_path))

        page_count = len(reader.pages)

        # 5. Create document record
        document = Document(
            id=document_id,
            original_filename=filename,
            stored_filename=stored_filename,
            content_hash=content_hash,
            file_size=len(file_bytes),
            page_count=page_count,
            status="processing",
        )

        db.add(document)

        # 6. Create ingestion job
        job = IngestionJob(
            document_id=document_id,
            status="processing",
        )

        db.add(job)

        # 7. Extract pages
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            document_page = DocumentPage(
                document_id=document_id,
                page_number=page_number,
                text=text,
            )

            db.add(document_page)

            # 8. Create chunks
            chunks = chunk_text(text)

            for chunk_index, chunk in enumerate(chunks):
                embedding = generate_embedding(chunk)

                document_chunk = DocumentChunk(
                    document_id=document_id,
                    page_number=page_number,
                    chunk_index=chunk_index,
                    text=chunk,
                    embedding=embedding,
                )

                db.add(document_chunk)

        # 9. Mark ingestion as completed
        document.status = "completed"
        job.status = "completed"

        db.commit()
        db.refresh(document)

        return document, True

    except Exception as exc:
        db.rollback()

        # Remove partially created database records
        existing_document = db.get(Document, document_id)

        if existing_document:
            db.delete(existing_document)
            db.commit()

        # Remove stored PDF if ingestion failed
        if file_path.exists():
            file_path.unlink()

        raise exc
