from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response
from sqlalchemy.orm import Session
from starlette import status
from dependencies.get_db import get_db
from dto.quotes_dto import QuoteQueryParams, CreateQuoteRequest, UpdateQuoteRequest
from dto.response_dto import ResponseDto
from routes.auth_routes import access_token_bearer
from services.quote_service import QuoteService
from services.user_quotes_reaction_service import UserQuotesReactionService
from enums.user_reactions import UserQuotesReactionEnum
from fastapi_throttle import RateLimiter
from dependencies.optional_token_bearer import optional_access_token_bearer, rate_limit_dependency_check

router = APIRouter(
    prefix="/quotes",
    tags=["Quotes"]
)


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=ResponseDto,
            summary="Get all quotes",
            description="Retrieve all the quotes and optionally filter by author and/or quote"
            )
async def fetch_all_quotes(_request: Request, _response: Response, db: Session = Depends(get_db),
                           # rate_limit: None = Depends(rate_limit_dependency_check),
                           query_params: QuoteQueryParams = Depends()):
    quotes = QuoteService(db).fetch_all_quotes(query_params)
    return ResponseDto(message="Quotes fetched successfully", data=quotes)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseDto,
             summary="Add a quote",
             description="Create a new quote"
             )
async def create_quote(request: CreateQuoteRequest, payload: dict = Depends(access_token_bearer),
                       db: Session = Depends(get_db)):
    new_quote = QuoteService(db).create_quote(request, payload["user_id"])
    return ResponseDto(message="Quote created successfully", data=new_quote)


@router.patch("/{id}",
              status_code=status.HTTP_201_CREATED,
              response_model=ResponseDto,
              summary="Update a quote",
              description="Updated the quote with the specific id"
              )
async def update_quote(id: UUID, update_request: UpdateQuoteRequest, payload: dict = Depends(access_token_bearer),
                       db: Session = Depends(get_db)):
    updated_quote = QuoteService(db).update_quote(update_request, str(id), payload["user_id"])
    return ResponseDto(message="Quote created successfully", data=updated_quote)


@router.patch('/{id}/like/up',
              status_code=status.HTTP_200_OK,
              summary="Add a like",
              description="Add a like to a quote,increase the like value")
async def like_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).create_reaction(str(id), payload["user_id"],
                                                                   mode=UserQuotesReactionEnum.like)
    return ResponseDto(message="Like added successfully", data=quote_reaction)


@router.patch('/{id}/like/down',
              status_code=status.HTTP_200_OK,
              summary="Remove a like",
              description="Remove the like to a quote,decrease the like value")
async def like_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).remove_reaction(str(id), payload["user_id"],
                                                                   mode=UserQuotesReactionEnum.like)
    return ResponseDto(message="Like removed successfully", data=quote_reaction)


@router.get('/{id}/like/users',
            status_code=status.HTTP_200_OK,
            summary="Get users who liked quote",
            description="Displays all the user's names who liked the quote")
async def like_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).get_users_by_quote_reaction(str(id),
                                                                               mode=UserQuotesReactionEnum.like)
    return ResponseDto(message="Users who disliked the quote", data=quote_reaction)


@router.patch('/{id}/dislike/up',
              status_code=status.HTTP_200_OK,
              summary="Add a dislike",
              description="Add a dislike to a quote,increase the dislike value")
async def dislike_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).create_reaction(str(id), payload["user_id"],
                                                                   mode=UserQuotesReactionEnum.dislike)
    return ResponseDto(message="Dislike added successfully", data=quote_reaction)


@router.patch('/{id}/dislike/down',
              status_code=status.HTTP_200_OK,
              summary="Remove a dislike",
              description="Remove a dislike to a quote,decrease the dislike value")
async def dislike_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).remove_reaction(str(id), payload["user_id"],
                                                                   mode=UserQuotesReactionEnum.dislike)
    return ResponseDto(message="Dislike removed successfully", data=quote_reaction)


@router.get('/{id}/dislike/users',
            status_code=status.HTTP_200_OK,
            summary="Get users who disliked quote",
            description="Displays all the user's names who disliked the quote")
async def like_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote_reaction = UserQuotesReactionService(db).get_users_by_quote_reaction(str(id),
                                                                               mode=UserQuotesReactionEnum.dislike)
    return ResponseDto(message="Users who disliked the quote", data=quote_reaction)


@router.delete("/{id}",
               status_code=status.HTTP_200_OK,
               response_model=ResponseDto,
               summary="Delete a quote",
               description="Delete the quote with the specified id")
async def delete_quote(id: UUID, payload: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    QuoteService(db).delete_quote(str(id), payload["user_id"])
    return ResponseDto(message="Quote deleted successfully")


@router.get("/tags",
            status_code=status.HTTP_200_OK,
            response_model=ResponseDto,
            summary="Fetch all tags",
            description="Fetch all unique tags used")
async def fetch_tags(_: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    tags_list = QuoteService(db).fetch_all_unique_tags()
    return ResponseDto(message="Quote fetched successfully", data=tags_list)


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=ResponseDto,
            summary="Get a quote",
            description="Get the quote with the specified id")
async def fetch_quote_by_id(id: UUID, _: dict = Depends(access_token_bearer), db: Session = Depends(get_db)):
    quote = QuoteService(db).fetch_quote_by_id(str(id))
    return ResponseDto(message="Quote fetched successfully", data=quote)
