"""
Django Ninja API for the Antibody Registry
Simplified architecture - works directly with Django models
Django Ninja handles automatic serialization via schemas
"""
import os
from typing import Optional

from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.http import HttpRequest
from cloudharness.middleware import get_authentication_token
from cloudharness.auth import decode_token


# Authentication
class BearerAuth(HttpBearer):
    """
    Bearer token authentication for protected endpoints.
    Validates JWT token using cloudharness.
    """
    def authenticate(self, request: HttpRequest, token: str) -> Optional[dict]:
        # Skip auth validation in local development (non-k8s)
        if not os.environ.get('KUBERNETES_SERVICE_HOST', None):
            # In test/dev mode, if there's an authenticated user on the request, allow it
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                return {"user": str(request.user.username)}
            return {"user": "dev-user"}
        
        try:
            # Decode and validate the token
            payload = decode_token(token)
            return payload
        except Exception:
            # Return None to indicate authentication failure
            return None


# Create auth instance for use in protected endpoints
auth = BearerAuth()

# Create the API WITHOUT global auth
# Individual endpoints will specify auth as needed
api = NinjaAPI(
    title="SciCrunch Antibody Registry API",
    version="1.0.0",
    description="Antibody Registry API",
    urls_namespace="api",
    docs_url="/docs",  # Enable automatic API documentation at /api/docs
)

# Import and register routers
from api.routers import antibody, search, test, ingest, general

# Add routers to the main API
api.add_router("", antibody.router)
api.add_router("", search.router)
api.add_router("", test.router)
api.add_router("", ingest.router)
api.add_router("", general.router)

# Register exception handlers
from api.helpers.response_helpers import add_exception_handlers
add_exception_handlers(api)
