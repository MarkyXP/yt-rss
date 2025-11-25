"""
References:
> https://dev.to/idsulik/a-beginners-guide-to-docker-health-checks-and-container-monitoring-3kh6
"""

from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/check")
def health_check():
    """
    Simply returns a JSON response of `{'status' : 'OK'}`.
    If no response is returned indicates the program has crashed.
    """
    return {"status": "OK"}
