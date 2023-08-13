from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, CHAR
import sqlite3

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key=True)


engine = create_engine("sqlite:///mydb.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)