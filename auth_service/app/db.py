from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    fullname = Column('fullname', String)
    role = Column('role', String)
    email = Column('email', String)
    password = Column('password', String)


engine = create_engine("sqlite:///mydb.sqlite3", echo=True)
Session = sessionmaker(bind=engine)


if __name__ == '__main__':

    Base.metadata.create_all(bind=engine)

    session = Session()

    session.query(User).delete()
    session.commit()

    users = [
        User(
            fullname='admin',
            email='admin@mail.mail',
            password='password',
            role="ADMINISTRATOR",
        ),
        User(
            fullname='developer developerovich',
            email='dev@mail.mail',
            password='password',
            role="DEVELOPER",
        ),
        User(
            fullname='manager managerovich',
            email='manager@mail.mail',
            password='password',
            role="MANAGER",
        ),
        User(
            fullname='accountant acoountovich',
            email='accountant@mail.mail',
            password='password',
            role="ACCOUNTANT",
        )
    ]
    for user in users:
        session.add(user)
    session.commit()