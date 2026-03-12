from fastapi import FastAPI, Response, Request, HTTPException, Form, Cookie
from fastapi.responses import JSONResponse
import uuid
from typing import Optional

app = FastAPI(title="Task 5 API")

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

active_sessions = {}

@app.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    if username in VALID_USERS and VALID_USERS[username] == password:
        session_token = str(uuid.uuid4())
        
        active_sessions[session_token] = {
            "username": username
        }
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": username, "debug_session_token": session_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/user")
async def get_user(
    session_token: Optional[str] = Cookie(None)
):
    if not session_token:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
        )

    if session_token not in active_sessions:
        return JSONResponse(
            status_code=401,
            content={"message": "Unauthorized"}
        )
    
    user_data = active_sessions[session_token]
    
    return {
        "username": user_data["username"],
        "message": "User profile information"
    }