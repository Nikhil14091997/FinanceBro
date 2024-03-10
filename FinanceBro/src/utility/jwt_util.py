from datetime import datetime, timedelta
from typing import Optional, Annotated
from fastapi import HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.utility.configs.config_handler import ConfigHandler
from src.utility.logging_util import LoggerSetup
from src.database.models.user import User as model_user
from dependencies import get_db


logger_setup = LoggerSetup(logger_name="JWTUtil")
logger_setup.add_formatter()
logger = logger_setup.logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenHandler:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.jwt_config = self.config_handler.get_jwt_config()
        self.SECRET_KEY = self.jwt_config['secret_key']
        self.ALGORITHM = self.jwt_config['algorithm']
        self.ACCESS_TOKEN_EXPIRE_MINUTES = self.jwt_config['access_token_expire_minutes']
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return user_id
        except JWTError:
            raise credentials_exception
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            user = db.query(model_user).filter(model_user.email == email).first()
            if user is None:
                raise credentials_exception
            return user
        except JWTError:
            raise credentials_exception
    
    async def get_current_active_user(self, current_user: model_user = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    async def has_role(self, required_role: str):
        def role_checker(current_user: model_user = Depends(self.get_current_active_user)):
            if current_user.user_role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
                )
            return current_user
        return role_checker



