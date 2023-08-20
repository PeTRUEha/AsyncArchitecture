from typing import Annotated
import uvicorn
import httpx
from fastapi import FastAPI, Depends
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer

app = FastAPI()


def confirm_authenticity(request: Request):
    # Не работает. Не смог разобраться, как вычленить данные для авторизации для отправки на SSO сервис
    headers = {"Authorization": request.headers.get("Authorization")}
    responce = httpx.get(url='http://127.0.0.1:8000/confirm_authenticity',
                             headers=headers)
    if responce.status_code == 200:
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")


# route handlers


@app.post("/hey", tags=["user"])
async def create_task(request: Request, _: Annotated[bool, Depends(HTTPBearer())]):
    confirm_authenticity(request)
    return {"res": 'god'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)