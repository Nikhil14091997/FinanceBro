from uuid import uuid4
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, status
from dependencies import get_db
from src.database.schema.api_response import ApiResponse
from src.database.schema.user import UserResponse, UserRequest
from src.utility.logging_util import LoggerSetup
from src.database.models.user import User as model_user

logger_setup = LoggerSetup(logger_name="ConnectionHandler")
logger_setup.add_formatter()
logger = logger_setup.logger

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

# db dependency
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[UserResponse])
async def register_user(user: UserRequest, db: Session = Depends(get_db)):

    # check if user already exists
    existing_user = db.query(model_user).filter(model_user.email == user.email).first()
    if existing_user:
        logger.warning(f"User {user.email} already exists.")
        raise HTTPException(status_code=400, detail="User already exists.")
    
    user_id = str(uuid4())
    while db.query(model_user).filter(model_user.id == user_id).first():
        user_id = str(uuid4())
    try:
        date_of_birth = datetime.strptime(user.date_of_birth, '%m/%d/%Y')
    except ValueError as e:
        logger.error(f"Date format error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use MM/DD/YYYY.")
    
    # set default values for the user
    is_active = True
    created_at = datetime.utcnow()

    new_user = model_user(
        id=user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=user.password,
        date_of_birth=date_of_birth,
        is_active=is_active,
        last_login=created_at,
        user_role="basic",
        created_at=created_at,
        location_state=user.location_state,
        location_country=user.location_country
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User {new_user.email} registered successfully.")
        return ApiResponse(
            status_code=status.HTTP_201_CREATED,
            message="User registered successfully",
            data=  UserResponse(
                id=new_user.id,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                email=new_user.email,
                is_active=new_user.is_active,
                last_login=str(new_user.last_login),
                user_role=new_user.user_role,
                created_at=str(new_user.created_at)
            )
        )
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        db.rollback()
        return ApiResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error"
        )
    