from app.core.database import SessionLocal
from app.rag.retrieval.service import search_similar_chunks


db = SessionLocal()

try:
    results = search_similar_chunks(
        db,
        "What projects are mentioned in the document?",
        limit=3,
    )

    for chunk, distance in results:
        print("=" * 80)
        print("Distance:", distance)
        print("Page:", chunk.page_number)
        print("Chunk:", chunk.chunk_index)
        print("Text:")
        print(chunk.text)

finally:
    db.close()
