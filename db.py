from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Integer, String, Column, create_engine, Float
import os

SQLURL = os.getenv("SQLURL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(SQLURL)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)


Base.metadata.create_all(bind=engine)
##SQLURL = "postgresql://postgres:postgres@127.0.0.1:5432/postgres?client_encoding=utf8"