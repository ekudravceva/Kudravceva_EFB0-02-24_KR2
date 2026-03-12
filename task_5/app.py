from fastapi import FastAPI, Response, HTTPException, Form, Cookie
from fastapi.responses import JSONResponse
import uuid
from typing import Optional
from itsdangerous import URLSafeSerializer

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
        session_token = serializer.dumps(user_id)
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": username}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/profile")
async def get_profile(
    session_token: Optional[str] = Cookie(None)
):
    if not session_token:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
        )

    try:
        user_id = serializer.loads(session_token)
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
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
    
    return {
        "username": username,
        "user_id": user_id,
        "message": "User profile information"
    }