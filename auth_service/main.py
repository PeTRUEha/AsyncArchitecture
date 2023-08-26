import time
from typing import Annotated
from fastapi import FastAPI, Body, Depends, Request
import uvicorn
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.constants import Role
from app.db import User, Session
from app.event.event import UserCreated
from app.kafka_setup import producer
from app.model import UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, decodeJWT

import uuid

app = FastAPI()


def get_user_role(user_email: str):
    return Session().query(User).filter_by(email=user_email).all()[0].role


def check_user(data: UserLoginSchema):
    query = Session().query(User).filter(
        User.email == data.email, User.password == data.password
    )
    if len(query.all()) > 0:
        return True
    else:
        return False


async def get_user_email(request: Request):
    credentials: HTTPAuthorizationCredentials = await HTTPBearer().__call__(request)
    return decodeJWT(credentials.credentials)['user_id']

# route handlers


@app.post("/user/create_new_user", tags=["user"])
async def create_user(
        authenticity: Annotated[bool, Depends(JWTBearer())],
        request: Request,
        new_user: UserSchema = Body(...),
    ):
    current_user_email = await get_user_email(request)
    assert Role(get_user_role(current_user_email)) == Role.ADMINISTRATOR

    session = Session()
    new_user_entry = User(**new_user.model_dump())
    session.add(new_user_entry)
    event = UserCreated(
            **new_user_entry.model_dump()
    )
    event.validate()
    producer.send('users-stream', event.dict)
    producer.flush()
    session.commit()
    return signJWT(new_user.email)


@app.get("/confirm_authenticity")
def confirm_authenticity(authenticity: Annotated[bool, Depends(JWTBearer())]):
    return {
        "authenticity": authenticity
    }


@app.get('/get_current_user_role')
async def get_current_user_role(request: Request):
    user_email = await get_user_email(request)
    role = get_user_role(user_email)
    return {
        'role': role
    }


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)