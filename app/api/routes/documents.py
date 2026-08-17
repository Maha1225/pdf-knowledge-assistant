from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document_page import DocumentPage
from app.repositories.document_repository import get_document
from app.services.document_service import ingest_pdf


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    document, created = ingest_pdf(
        db=db,
        filename=file.filename,
        file_bytes=file_bytes,
    )

    return {
        "message": (
            "Document uploaded successfully"
            if created
            else "Document already exists"
        ),
        "document_id": str(document.id),
        "filename": document.original_filename,
        "page_count": document.page_count,
        "status": document.status,
        "duplicate": not created,
    }


@router.get("/{document_id}")
def get_document_details(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    document = get_document(db, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == document_id)
        .order_by(DocumentPage.page_number)
        .all()
    )

    return {
        "document_id": str(document.id),
        "filename": document.original_filename,
        "file_size": document.file_size,
        "page_count": document.page_count,
        "status": document.status,
        "created_at": document.created_at,
        "pages": [
            {
                "page_number": page.page_number,
                "text": page.text,
            }
            for page in pages
        ],
    }