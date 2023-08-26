from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
import sqlite3

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', String)
    assignee = Column('assignee', ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    role = Column('role', String)


engine = create_engine("sqlite:///mydb.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()