'''
@Author: Nikhil Kumar
@Desc: Class to handle the database connection
'''
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Updated import statement
from src.utility.logging_util import LoggerSetup
from src.utility.configs.config_handler import ConfigHandler

logger_setup = LoggerSetup(logger_name="ConnectionHandler")
logger_setup.add_formatter()
logger = logger_setup.logger

# Get the configuration
config_handler = ConfigHandler()
database_config = config_handler.get_database_config()

DATABASE_URL = f"{database_config['dialect']}+{database_config['lib']}://" \
               f"{database_config['username']}:{quote(database_config['password'])}@" \
               f"{database_config['host']}:{database_config['port']}/" \
               f"{database_config['database_name']}"

logger.info("Creating database engine...")
engine = create_engine(DATABASE_URL)
logger.info("Database engine created successfully. ✓")

logger.info("Creating session factory...")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Session factory created successfully. ✓")

# Base class for the models
Base = declarative_base()
