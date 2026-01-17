import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL').strip()
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    # pool_size=settings.pool_size,
    # max_overflow=settings.pool_size,
    echo=False,  # Set to True for SQL query logging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session

# just for testing the db connection
# if __name__ == "__main__":
#     conn = engine.connect()
#     print("Connected to db")
#     conn.close()
