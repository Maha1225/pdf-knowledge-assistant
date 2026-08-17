from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    limit: int = Field(
        default=6,
        ge=1,
        le=10,
    )


class SourceResponse(BaseModel):
    page_number: int
    chunk_index: int
    distance: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
