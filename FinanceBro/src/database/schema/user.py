from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Annotated
from src.database.models.user import User
from src.database.connection_handler import SessionLocal, engine
from src.utility.logging_util import LoggerSetup

logger_setup = LoggerSetup(logger_name="UserHandler")
logger_setup.add_formatter()
logger = logger_setup.logger

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    password: str
    location_state: str
    location_country: str

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    last_login: datetime
    user_role: str
    created_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str