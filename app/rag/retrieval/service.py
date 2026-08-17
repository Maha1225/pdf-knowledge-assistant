from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.rag.embeddings.service import generate_embedding


def search_similar_chunks(
    db: Session,
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            DocumentChunk,
            distance.label("distance"),
        )
        .order_by(distance)
        .limit(limit)
    )

    results = db.execute(statement).all()

    return results
