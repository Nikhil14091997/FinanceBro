from pydantic import BaseModel
from datetime import datetime

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_at:datetime