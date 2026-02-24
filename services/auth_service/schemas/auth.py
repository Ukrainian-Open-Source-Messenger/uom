from pydantic import BaseModel, field_validator, EmailStr, Field
import re

password_regex = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8, max_length=100)
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not password_regex.match(v):
            raise ValueError(
                "Password must contain at least one digit, one uppercase letter, and be at least 8 characters long"
            )
        return v


class LoginRequest(BaseModel):
    password: str
    email: EmailStr
