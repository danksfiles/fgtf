import sys
sys.path.append('.')

from src.database import engine, Base
from src.models import *

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
