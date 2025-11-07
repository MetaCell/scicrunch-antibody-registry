"""
Test Router - Handles health check and test endpoints
"""
from ninja import Router
from django.http import HttpRequest


router = Router()


@router.get("/live", response=str, tags=["test"])
def live(request: HttpRequest):
    """Checks if application is healthy"""
    return "I'm alive!"


@router.get("/ping", response=str, tags=["test"])
def ping(request: HttpRequest):
    """Checks if application is up"""
    return "Ping!"


@router.get("/ready", response=str, tags=["test"])
def ready(request: HttpRequest):
    """Checks if application is ready to take requests"""
    return "I'm READY!"
