from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = URL.create(
    drivername="postgresql",
    username="agtern",
    password="password",
    host="localhost",
    database="agtern"
)

engine = create_engine(url)

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DatabaseModel = declarative_base(name="DatabaseModel")
