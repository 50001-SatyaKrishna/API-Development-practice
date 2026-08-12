from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='freecodecamp.org2026',cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("Database connection is successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed!")
#         print(f"Error: {error}")
#         time.sleep(2)

#Dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()