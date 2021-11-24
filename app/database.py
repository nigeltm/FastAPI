from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine =  create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DATABASE CONNECTION FOR RAW SQL AND NOT SQLALCHEMY
# while True:
#     try:
#         conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",
#         password="Mahachula123#!",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connected succesfully.")
#         break
#     except Exception as error:
#         print("Connecting to database failed.")
#         print("Error",error)
#         time.sleep(2)