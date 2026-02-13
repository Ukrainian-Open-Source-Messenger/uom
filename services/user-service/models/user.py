from pydantic import BaseModel

class MakeRequest(BaseModel):
    username: str
    password: str
    email: str

class GetMeByEmailRequest(BaseModel):
    email: str

class GetMeByIdRequest(BaseModel):
    id: str

class User(BaseModel):
    id: str
    username: str
    password: str
    createdAt: int
    email: str
