from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Схема токена"""
    access_token: str
    token_type: str
