from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from dto.quotes_dto import CreateQuoteUserReactionResponse, CountReactionResponse
from constants.error_messages import QuoteErrors, UserQuoteReactionErrors
from models.UserQuoteReaction import UserQuoteReaction
from models.quote import Quote
from enums.user_reactions import UserQuotesReactionEnum, CountOperationsEnum
from models.user import User
 

class UserQuotesReactionService:
    def __init__(self, db: Session = None):
        self.db = db

    def create_reaction(self, quote_id: str, user_id: str, mode: UserQuotesReactionEnum) -> CreateQuoteUserReactionResponse:
        try:
            self.validate_quote(quote_id)
            self.validate_not_own_post(quote_id, user_id, mode)

            existing_reactions = self.db.query(UserQuoteReaction).filter(
                (UserQuoteReaction.quote_id == quote_id) & (UserQuoteReaction.user_id == user_id)).first()
            if existing_reactions is not None:
                if ((existing_reactions.like is True) and (mode is UserQuotesReactionEnum.like)) or (
                        (existing_reactions.dislike is True) and mode is UserQuotesReactionEnum.dislike):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f'You cannot {mode.value} this again because it’s already {mode.value}d')

                # If existing_reaction is liked and mode is disliked or vice versa
                if mode is UserQuotesReactionEnum.dislike:
                    existing_reactions.dislike = True
                    existing_reactions.like = False
                    data = self.toggle_value(quote_id, UserQuotesReactionEnum.dislike)

                else:
                    existing_reactions.like = True
                    existing_reactions.dislike = False
                    data = self.toggle_value(quote_id, UserQuotesReactionEnum.like)
                    

                self.db.add(existing_reactions)
                self.db.commit()
                self.db.refresh(existing_reactions)
                return CreateQuoteUserReactionResponse(
                    id=existing_reactions.id,
                    quote=data.quote,
                    author=data.author,
                    like=data.like,
                    dislike=data.dislike,
                    tags=data.tags
                )
            else:
                # creating either Liked reaction or Disliked reaction
                if mode is UserQuotesReactionEnum.like:
                    new_reaction = UserQuoteReaction(
                        user_id=user_id,
                        quote_id=quote_id,
                        like=True
                    )

                else:
                    new_reaction = UserQuoteReaction(
                        user_id=user_id,
                        quote_id=quote_id,
                        dislike=True
                    )

                data = self.count_operation(quote_id, mode, CountOperationsEnum.INCREMENT)


                self.db.add(new_reaction)
                self.db.commit()
                self.db.refresh(new_reaction)

                return CreateQuoteUserReactionResponse(
                    id=new_reaction.id,
                    quote=data.quote,
                    author=data.author,
                    like=data.like,
                    dislike=data.dislike,
                    tags=data.tags
                )
        except HTTPException as err_msg:
            raise err_msg
        except Exception as err_msg:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to save {mode} reaction. {err_msg}")

    def remove_reaction(self, quote_id: str, user_id: str, mode: UserQuotesReactionEnum):
        try:

            self.validate_not_own_post(quote_id, user_id, mode)

            existing_reactions = self.db.query(UserQuoteReaction).filter(
                (UserQuoteReaction.quote_id == quote_id) & (UserQuoteReaction.user_id == user_id)).first()

            if existing_reactions is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'You havent {mode.value}d this quote yet')

            self.db.query(UserQuoteReaction).filter(
                (UserQuoteReaction.quote_id == quote_id) & (UserQuoteReaction.user_id == user_id)).delete()

            self.count_operation(quote_id, mode, CountOperationsEnum.DECREMENT)

            self.db.commit()


        except HTTPException as err_msg:
            raise err_msg
        except Exception as err_msg:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"{UserQuoteReactionErrors.UPDATE_REACTION_FAILED} {err_msg}")

    def get_users_by_quote_reaction(self, quote_id: str, mode: UserQuotesReactionEnum):
        try:
            query = self.db.query(User).join(UserQuoteReaction).filter(UserQuoteReaction.quote_id == quote_id)
            if not query.all():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=UserQuoteReactionErrors.REACTIONS_NOT_FOUND)
            if mode is UserQuotesReactionEnum.like:
                query = query.filter(UserQuoteReaction.like == True)
            else:
                query = query.filter(UserQuoteReaction.dislike == True)

            users = query.distinct().all()
            user_names = []
            for user in users:
                user_names.append(f"{user.first_name} {user.last_name}")
            return user_names
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching users: {str(e)}"
            )

    def count_operation(self, quote_id: str, mode: UserQuotesReactionEnum, operation: CountOperationsEnum):
        quote = self.db.query(Quote).filter(Quote.id == quote_id).first()

        field = 'like' if mode is UserQuotesReactionEnum.like else 'dislike'
        current_value = getattr(quote, field)

        if operation is CountOperationsEnum.INCREMENT:
            setattr(quote, field, current_value + 1)
        else:  # DECREMENT
            if current_value <= 0:
                raise HTTPException(status_code=400, detail=f"Cannot reduce {field} below 0")
            setattr(quote, field, current_value - 1)

        self.db.add(quote)
        self.db.commit()
        self.db.refresh(quote)
        return quote

    def validate_not_own_post(self, quote_id: str, user_id: str, mode: UserQuotesReactionEnum):
        if self.db.query(Quote).filter((Quote.id == quote_id) & (Quote.user_id == user_id)).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'You cannot {mode.value} your own quote')

    def validate_quote(self, quote_id: str):
        if not self.db.query(Quote).filter(Quote.id == quote_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=QuoteErrors.QUOTE_NOT_FOUND)

    def toggle_value(self, quote_id: str, mode: UserQuotesReactionEnum) :
        self.validate_quote(quote_id)
        quote = self.db.query(Quote).filter(Quote.id == quote_id).first()
        if mode is UserQuotesReactionEnum.dislike:
            quote.like -= 1
            quote.dislike += 1
        else:
            quote.dislike -= 1
            quote.like += 1

        self.db.add(quote)
        self.db.commit()
        self.db.refresh(quote)
        return quote
        

