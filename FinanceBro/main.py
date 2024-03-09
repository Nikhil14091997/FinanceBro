from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Annotated
from models import User
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# app instance
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

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
    last_login: str
    user_role: str
    created_at: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user: UserRequest, db: Session = Depends(get_db)):
    # Generate a random UUID for the user id
    user_id = str(uuid4())
    logger.info(f"Generated UUID: {user_id}")

    # Check if the generated user_id already exists
    while db.query(User).filter(User.id == user_id).first():
        # If user_id already exists, generate a new one
        user_id = str(uuid4())

    # Convert the date_of_birth string to a datetime object
    try:
        date_of_birth = datetime.strptime(user.date_of_birth, '%m/%d/%Y')
    except ValueError as e:
        logger.error(f"Date format error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use MM/DD/YYYY.")

    # Set the default values for additional fields
    is_active = True
    created_at = datetime.utcnow()

    # Create a new user instance with all the data
    new_user = models.User(
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

    # Add the new user to the database and commit the transaction
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User {new_user.email} registered successfully.")
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    # Return the newly created user
    return UserResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        is_active=new_user.is_active,
        last_login=str(new_user.last_login),
        user_role=new_user.user_role,
        created_at=str(new_user.created_at)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7999)
