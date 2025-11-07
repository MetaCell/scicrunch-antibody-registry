from typing import Union
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI, Router
from api.schemas import ErrorResponseSchema, Antibody as AntibodySchema
from api.exceptions import Http403, Http401, Http400, Http409
from api.utilities.exceptions import DuplicatedAntibody


class CamelCaseRouter(Router):
    """Router subclass that uses by_alias=True by default for camelCase responses"""
    
    def get(self, *args, by_alias=True, **kwargs):
        return super().get(*args, by_alias=by_alias, **kwargs)
    
    def post(self, *args, by_alias=True, **kwargs):
        return super().post(*args, by_alias=by_alias, **kwargs)
    
    def put(self, *args, by_alias=True, **kwargs):
        return super().put(*args, by_alias=by_alias, **kwargs)
    
    def patch(self, *args, by_alias=True, **kwargs):
        return super().patch(*args, by_alias=by_alias, **kwargs)
    
    def delete(self, *args, by_alias=True, **kwargs):
        return super().delete(*args, by_alias=by_alias, **kwargs)


GET_ERR_RESPONSES = {
    400: Union[ErrorResponseSchema, str],
    401: Union[ErrorResponseSchema, str],
    403: Union[ErrorResponseSchema, str],
    404: Union[ErrorResponseSchema, str],
    405: Union[ErrorResponseSchema, str],
    422: Union[ErrorResponseSchema, str],
}
POST_ERR_RESPONSES = {
    400: Union[ErrorResponseSchema, str],
    401: Union[ErrorResponseSchema, str],
    403: Union[ErrorResponseSchema, str],
    404: Union[ErrorResponseSchema, str],
    405: Union[ErrorResponseSchema, str],
    422: Union[ErrorResponseSchema, str],
    429: Union[ErrorResponseSchema, str],
}
UPD_ERR_RESPONSES = {
    400: Union[ErrorResponseSchema, str],
    401: Union[ErrorResponseSchema, str],
    403: Union[ErrorResponseSchema, str],
    404: Union[ErrorResponseSchema, str],
    405: Union[ErrorResponseSchema, str],
    422: Union[ErrorResponseSchema, str],
}
DEL_ERR_RESPONSES = {
    400: Union[ErrorResponseSchema, str],
    401: Union[ErrorResponseSchema, str],
    403: Union[ErrorResponseSchema, str],
    404: Union[ErrorResponseSchema, str],
    405: Union[ErrorResponseSchema, str],
    409: Union[ErrorResponseSchema, str],
    422: Union[ErrorResponseSchema, str],
}


def add_exception_handlers(api: NinjaAPI) -> None:
    # Guard against adding handlers multiple times
    if hasattr(api, '_exception_handlers_added'):
        return
    api._exception_handlers_added = True
    
    api.add_exception_handler(
        Http401,
        _create_exception_handler(api, 401, "Unauthorized"),
    )
    api.add_exception_handler(
        Http400,
        _create_exception_handler(
            api, 400, "Bad Request"
        )
    )
    api.add_exception_handler(Http403, _create_exception_handler(api, 403, "Forbidden"))
    api.add_exception_handler(Http409, _create_exception_handler(api, 409, "Conflict"))
    
    # Custom handler for DuplicatedAntibody that returns the antibody data
    @api.exception_handler(DuplicatedAntibody)
    def duplicated_antibody_handler(request: HttpRequest, exception: DuplicatedAntibody) -> HttpResponse:
        # Let Django Ninja handle serialization by creating a proper API response
        # The antibody data will be serialized using the normal Django Ninja process
        from ninja.responses import Response
        
        # Create a Response object with the antibody data - Django Ninja will handle serialization
        response_data = AntibodySchema.model_validate(exception.antibody)
        return Response(
            response_data.model_dump(by_alias=True), 
            status=409
        )


def _create_exception_handler(api: NinjaAPI, status_code: int, default_message: str):
    def exception_handler(request: HttpRequest, exception) -> HttpResponse:
        message = str(exception) if str(exception) else default_message
        # Conform to ErrorResponseSchema expected by routes: {error: str, success: bool}
        payload = {"error": message, "success": False, "message": message}  # include legacy 'message'
        return api.create_response(request, payload, status=status_code)
    return exception_handler
