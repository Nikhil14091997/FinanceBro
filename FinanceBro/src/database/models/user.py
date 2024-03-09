'''
@Author: Nikhil Kumar
@Desc: ORM for the user table
'''
from datetime import datetime
from sqlalchemy import VARCHAR, Boolean, Column, DateTime, String
from src.database.connection_handler import Base

class User(Base):
    __tablename__ = "users"

    id = Column(VARCHAR(36), primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))  # Adjust the length according to your needs
    date_of_birth = Column(DateTime)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.utcnow)
    user_role = Column(String(50), default="basic")
    created_at = Column(DateTime, default=datetime.utcnow)
    location_state = Column(String(50))
    location_country = Column(String(50))