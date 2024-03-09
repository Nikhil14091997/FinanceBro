from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_db
from src.routers import user_service
from src.database.connection_handler import engine, Base
from src.utility.logging_util import LoggerSetup

logger_setup = LoggerSetup(logger_name="Main")
logger_setup.add_formatter()
logger = logger_setup.logger

app = FastAPI(
    title="FinanceBro",
    description="A finance management application",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

# Add the routers
app.include_router(user_service.router)

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger.info("Application started successfully. ✓")

@app.get("/")
async def root():
    return {"message": "Welcome to FinanceBro!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7999)


