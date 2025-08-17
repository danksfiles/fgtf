import yaml
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Construct absolute path to the config file
# This makes the script runnable from any directory
_current_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_CONFIG_PATH = os.path.join(_current_dir, '..', 'configs', 'database.yaml')

def get_database_url() -> str:
    with open(DATABASE_CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)["default"]
    
    return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
