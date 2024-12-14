from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# The connection string for the MySQL database.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine that connects to the database using the provided
# connection string.
engine = create_engine(DATABASE_URL, echo=False)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Create a declarative base class
Base = declarative_base()

# Create a session maker
Session = sessionmaker(bind=engine)
session = Session()

# Create all the tables in the database
Base.metadata.create_all(engine)
