import _asyncio

from fastapi import APIRouter, Request, Response, HTTPException

from app.core.users import USERS

router = APIRouter()

@router.post("login")
async def login(request: Request, response: Response, admin_password : str):
    # Sets a cookie named "session_id"
    token = await USERS.is_valid_user(admin_password)
    if not token:
        raise HTTPException(
            status_code = 401,
            detail = {
                "error": "Invalid password"
            }
        )
    response.set_cookie(key="auth_token", value=token)
    return {"message": "Logged in successfully"}

