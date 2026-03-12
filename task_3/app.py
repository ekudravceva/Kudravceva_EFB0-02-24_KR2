from fastapi import FastAPI, status
from models import UserCreate

app = FastAPI(
    title="Task 3 API",
)

@app.get("/")
def root():
    """Корневой эндпоинт для проверки работы API"""
    return {
        "message": "Task 3 API is running",
        "available_endpoints": [
            "POST /create_user - создать пользователя",
        ]
    }

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return user