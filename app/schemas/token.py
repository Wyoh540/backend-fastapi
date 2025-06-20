from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: int | None = None
    iat: int | None = None
    scopes: list[str] = []
