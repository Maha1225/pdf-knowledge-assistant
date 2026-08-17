from app.rag.llm.service import generate_answer


context = """
FlexiHire - Developed a web-based platform connecting freelancers
and companies for seamless job posting and recruitment.

The project includes job posting, application management,
and an efficient hiring process.
"""

question = "What is FlexiHire?"

answer = generate_answer(
    question=question,
    context=context,
)

print("=" * 80)
print("ANSWER:")
print(answer)
print("=" * 80)
