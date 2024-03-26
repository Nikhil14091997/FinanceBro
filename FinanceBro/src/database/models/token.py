from sqlalchemy import Column, Integer, String, DateTime,Boolean
from src.database.connection_handler import Base
from datetime import datetime

class TokenTable(Base):

    __tablename__ = "token"

    user_id = Column(String(36))
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)