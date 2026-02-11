from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class VerifyRequest(BaseModel):
    token: str

class User(BaseModel):
    id: str
    username: str
    password: str
    createdAt: int
