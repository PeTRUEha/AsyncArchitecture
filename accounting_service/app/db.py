from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
import sqlite3

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key=True)
    cost = Column('name', Integer)

engine = create_engine("sqlite:///mydb.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()