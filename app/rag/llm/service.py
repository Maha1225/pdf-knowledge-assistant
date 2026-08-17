import ollama


MODEL_NAME = "llama3.2:3b"


def generate_answer(
    question: str,
    context: str,
) -> str:
    prompt = f"""You are a helpful PDF knowledge assistant.

Answer the user's question using ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I could not find the answer in the uploaded document."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"].strip()
