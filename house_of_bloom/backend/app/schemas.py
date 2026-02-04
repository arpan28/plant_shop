from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HistoryCreate(BaseModel):
    path: str
    referrer: Optional[str]
    metadata: Optional[Dict[str, Any]]
