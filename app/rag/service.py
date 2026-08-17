from sqlalchemy.orm import Session

from app.rag.llm.service import generate_answer
from app.rag.retrieval.service import search_similar_chunks


def answer_question(
    db: Session,
    question: str,
    limit: int = 6,
) -> dict:
    results = search_similar_chunks(
        db=db,
        query=question,
        limit=limit,
    )

    if not results:
        return {
            "answer": "I could not find the answer in the uploaded document.",
            "sources": [],
        }

    context_parts = []
    sources = []

    for chunk, distance in results:
        context_parts.append(
            f"[Page {chunk.page_number}, Chunk {chunk.chunk_index}]\n"
            f"{chunk.text}"
        )

        sources.append(
            {
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "distance": float(distance),
            }
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }
