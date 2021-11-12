from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite://user:password@postgresserver/db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@127.0.0.1:3306/projetoDois"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
