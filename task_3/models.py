from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    age: Optional[int] = Field(None, ge=1, le=150, description="Возраст пользователя")
    is_subscribed: Optional[bool] = Field(False, description="Подписка на рассылку")
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Имя не может быть пустым')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice",
                "email": "alice@example.com",
                "age": 30,
                "is_subscribed": True
            }
        }