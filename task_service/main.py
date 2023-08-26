from typing import Annotated
import uvicorn
import httpx
from fastapi import FastAPI, Depends
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer

from app.db import Session, Task
from ..schema_registry.python.event import TaskCreated
from app.kafka_producer import producer
from app.model import TaskSchema
app = FastAPI()


def confirm_authenticity(request: Request):
    headers = {"Authorization": request.headers.get("Authorization")}
    responce = httpx.get(url='http://127.0.0.1:8000/confirm_authenticity',
                             headers=headers)
    if responce.status_code == 200:
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")


@app.post("/create_task")
async def create_task(request: Request, task: TaskSchema, _: Annotated[bool, Depends(HTTPBearer())]):
    confirm_authenticity(request)
    session = Session()
    new_task_entry = Task(**task.model_dump())
    session.add(new_task_entry)
    event = TaskCreated.from_data(
            data=new_task_entry.model_dump()
    )
    event.validate()
    producer.send('tasks-stream', event.dict)
    producer.flush()
    session.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)