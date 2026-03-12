from fastapi import FastAPI, Response, HTTPException, Form, Cookie, Header
from fastapi.responses import JSONResponse
import uuid
import time
from typing import Optional
from itsdangerous import URLSafeSerializer
from datetime import datetime
from models import CommonHeaders

app = FastAPI(title="Task 5 API")

SECRET_KEY = "secret-key-for-signing-cookies-ekud"
serializer = URLSafeSerializer(SECRET_KEY)

VALID_USERS = {
    "user123": {
        "password": "password123",
        "user_id": str(uuid.uuid4())
    },
    "admin": {
        "password": "admin123",
        "user_id": str(uuid.uuid4())
    }
}

@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    if username in VALID_USERS and VALID_USERS[username]["password"] == password:
        user_id = VALID_USERS[username]["user_id"]
        timestamp = int(time.time())
        session_data = f"{user_id}.{timestamp}"
        session_token = serializer.dumps(session_data)
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=300,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/profile")
async def get_profile(
    response: Response,
    session_token: Optional[str] = Cookie(None)
):
    if not session_token:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
        )

    try:
        session_data = serializer.loads(session_token)
        user_id, timestamp_str = session_data.split(".")
        timestamp = int(timestamp_str)
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"message": "Invalid session"}
        )
    
    current_time = int(time.time())
    time_diff = current_time - timestamp
    
    if time_diff >= 300:
        return JSONResponse(
            status_code=401,
            content={"message": "Session expired"}
        )
    
    username = None
    for uname, data in VALID_USERS.items():
        if data["user_id"] == user_id:
            username = uname
            break
    
    if username is None:
        return JSONResponse(
            status_code=401,
            content={"message": "User not found"}
        )
    
    if time_diff >= 180:
        new_timestamp = current_time
        new_session_data = f"{user_id}.{new_timestamp}"
        new_session_token = serializer.dumps(new_session_data)
        
        response.set_cookie(
            key="session_token",
            value=new_session_token,
            httponly=True,
            max_age=300,
            secure=False,
            samesite="lax"
        )
    
    return {
        "username": username,
        "user_id": user_id,
        "message": "User profile information"
    }

@app.get("/headers")
async def get_headers(headers: CommonHeaders = Header(...)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def get_info(
    response: Response,
    headers: CommonHeaders = Header(...)
):
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }