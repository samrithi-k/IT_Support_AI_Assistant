from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=1000
    )


class AskResponse(BaseModel):
    ticket_id: int
    answer: str
    retrieved_context: str