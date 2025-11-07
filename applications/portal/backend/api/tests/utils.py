from django.conf import settings
import abc
import uuid
from typing import Callable, Dict, Union, Optional
from unittest.mock import Mock

from django.contrib.auth.models import Group, User, AnonymousUser

from api.helpers.response_helpers import add_exception_handlers

from ninja import NinjaAPI
from ninja.router import Router
from ninja.testing.client import NinjaResponse, TestClient

from cloudharness.middleware import set_authentication_token



class BaseTestClient(TestClient, abc.ABC):
    _exception_handlers_added = set()
    
    def __init__(self, api_or_router: Union[NinjaAPI, Router], headers=None):
        if isinstance(api_or_router, Router):
            # We wrap the router in a dummy testing api instance to allow for adding standard exception handlers
            # Use a unique namespace for each test to avoid conflicts
            import uuid
            api = NinjaAPI(title="Test API", urls_namespace=f"test_{uuid.uuid4().hex[:8]}")
            api_or_router.api = None
            api.add_router("", api_or_router)
            # Only add exception handlers for wrapped routers, not for the main API
            add_exception_handlers(api)
        else:
            api = api_or_router
            # For the main API, exception handlers are already added in api.py

        super().__init__(api, headers)


class LoggedinTestClient(BaseTestClient):
    def __init__(
        self,
        api_or_router: Union[NinjaAPI, Router],
        user: User,
        headers=None,
        auth_token: Optional[str] = None,
    ):
        self.user = user
        self.auth_token = auth_token or "test-bearer-token"  # Provide a default test token
        
        # Merge provided headers with Authorization header
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.auth_token}'
        
        super().__init__(api_or_router, headers)

    def _call(self, func: Callable, request: Mock, kwargs: Dict) -> "NinjaResponse":
        request.user = self.user
        request.get_host = lambda: self.headers.get('HTTP_HOST', 'www.antibodyregistry.org')
        
        # Set authentication token in context
        set_authentication_token(self.auth_token)

        return NinjaResponse(func(request, **kwargs))


class AnonymousTestClient(LoggedinTestClient):
    def __init__(
        self,
        api_or_router: Union[NinjaAPI, Router],
        headers=None,
    ):
        super().__init__(api_or_router, AnonymousUser(), headers)


class LoggedinWithOrganizationTestClient(LoggedinTestClient):
    def __init__(self, api_or_router: Union[NinjaAPI, Router], user: User, organization_subdomain: str, headers=None):
        self.organization_subdomain = organization_subdomain
        self.user = user
        if headers is None:
            headers = {}
        headers['HTTP_HOST'] = organization_subdomain + '.neuroglass.io'
        super().__init__(api_or_router, user, headers)

    def _call(self, func: Callable, request: Mock, kwargs: Dict) -> "NinjaResponse":
        request.get_host = lambda: self.headers['HTTP_HOST']
        request.user = self.user

        return NinjaResponse(func(request, **kwargs))





