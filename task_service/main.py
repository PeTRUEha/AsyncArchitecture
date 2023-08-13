from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Body, Depends
from fastapi import Request, HTTPException

app = FastAPI()


def confirm_authenticity(request: Request):
    # Не работает. Не смог разобраться, как вычленить данные для авторизации для отправки на SSO сервис
    if RedirectResponse(url='http://127.0.0.1:8000/confirm_authenticity'):
        return
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")


# route handlers


@app.post("/hey", tags=["user"])
async def create_task(request: Request):
    confirm_authenticity(request)
    return {"res": 'good'}