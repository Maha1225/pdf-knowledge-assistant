from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.openai_api_key,
)


response = client.responses.create(
    model="gpt-5-mini",
    input="Reply with exactly: LLM connection successful.",
)


print(response.output_text)
