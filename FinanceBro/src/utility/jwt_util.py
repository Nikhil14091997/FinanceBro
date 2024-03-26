from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import HTTPException, Depends, Request,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.utility.configs.config_handler import ConfigHandler
from src.utility.logging_util import LoggerSetup
from src.database.models.user import User as model_user
from dependencies import get_db


logger_setup = LoggerSetup(logger_name="JWTUtil")
logger_setup.add_formatter()
logger = logger_setup.logger

# Details of the token
SECRET_KEY = ConfigHandler().get_jwt_config()['secret_key']
ALGORITHM = ConfigHandler().get_jwt_config()['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = ConfigHandler().get_jwt_config()['access_token_expire_minutes']
REFRESH_TOKEN_EXPIRE_MINUTES = ConfigHandler().get_jwt_config()['refresh_token_expire_minutes']
REFRESH_SECRET_KEY = ConfigHandler().get_jwt_config()['refresh_secret_key']



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str, secret_key: str = SECRET_KEY):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        logger.error(f"Error decoding token:{token}")
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    def verify_jwt(self, token: str):
        is_token_valid = False
        try:
            payload = decode_token(token)
            logger.info(f"Payload: {payload}")
        except:
            logger.error(f"Error decoding token:{token}")
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


    



