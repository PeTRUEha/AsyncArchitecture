from typing import Annotated
from fastapi import FastAPI, Body, Depends

from app.model import UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT


users = [
    UserSchema(
        fullname='name',
        email='email@mail.mail',
        password='password'
    )
]

app = FastAPI()


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

@app.post("/confirm_authenticity", tags=["posts"])
def confirm_authenticity(authenticity: Annotated[bool, Depends(JWTBearer())]):
    return {
        "authenticity": authenticity
    }


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user)  # TODO: replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
