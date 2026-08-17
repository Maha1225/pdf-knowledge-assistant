from app.core.config import settings
from app.core.database import SessionLocal
from app.rag.service import answer_question


db = SessionLocal()

try:
    question = "What projects are mentioned in the document?"

    result = answer_question(
        db=db,
        question=question,
        limit=6,
    )

    print("=" * 80)
    print("QUESTION:")
    print(question)

    print("=" * 80)
    print("ANSWER:")
    print(result["answer"])

    print("=" * 80)
    print("SOURCES:")

    for source in result["sources"]:
        print(
            f"Page {source['page_number']} | "
            f"Chunk {source['chunk_index']} | "
            f"Distance {source['distance']:.4f}"
        )

finally:
    db.close()
