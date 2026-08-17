import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Local LLM connection successful.",
        }
    ],
)

print(response["message"]["content"])
