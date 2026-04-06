"""
Docker supports a 'health check' to ensure that the code has not crashed.
This endpoint is used to verify that the API is running correctly.
"""


from datetime import datetime
from fastapi import APIRouter


router = APIRouter()

@router.get("/health_check")
async def health_check():
    """
    Health Check endpoint to verify the API's health.
    """
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "message": "API is running successfully."
    }