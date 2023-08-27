from pydantic import BaseModel, Field, EmailStr


class TaskSchema(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    assignee: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Do stuff",
                "description": "stuff to do",
                "assignee": "developer developerovich"
            }
        }