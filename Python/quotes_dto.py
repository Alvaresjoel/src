from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


class FetchQuoteResponse(BaseModel):
    id: UUID
    user_id: UUID
    quote: str = Field(min_length=10)
    author: str = Field(min_length=3)
    like: int = Field(gt=-1, description='Likes must be greater than or equal to 0')
    dislike: int = Field(gt=-1, description='Dislikes must be greater than or equal to 0')
    tags: str = Field(min_length=3, description='Add tags with a semi-colon to separate')

    class Config:
        from_attributes = True


class FetchAllQuotesResponse(BaseModel):
    total: int
    limit: int
    offset: int
    quotes: List[FetchQuoteResponse]


class QuoteQueryParams(BaseModel):
    limit: int = Field(default=5, ge=1, description="No. of quotes per page")
    offset: int = Field(default=0, ge=0, description="No. of quotes to be skipped")
    author: Optional[str] = Field(default=None)
    quote: Optional[str] = Field(default=None)


class CreateQuoteRequest(BaseModel):
    quote: str = Field(min_length=10, example="Machines take me by surprise with great frequency.")
    author: str = Field(min_length=3, example="Alan Turing")
    tags: str = Field(min_length=3, example="IT;Funny")


class UpdateQuoteRequest(BaseModel):
    quote: Optional[str] = Field(default=None)
    author: Optional[str] = Field(default=None)
    tags: Optional[str] = Field(default=None)

class CreateQuoteUserReactionResponse(BaseModel):
    id: UUID
    quote: str
    author: str
    like: int
    dislike: int
    tags: str

class CountReactionResponse(BaseModel):
    like: int
    dislike: int
