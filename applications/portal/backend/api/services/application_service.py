from typing import Tuple
from api.models import Application
from cloudharness import log


def get_or_create_application(name: str) -> Tuple[Application, bool]:
    """
    Get or create an Application instance by name.
    
    Args:
        name: The name of the application
        
    Returns:
        Tuple of (Application instance, created boolean)
    """
    if not name:
        raise ValueError('Application name is required')
    
    # Normalize the name (strip whitespace)
    name = name.strip()
    
    try:
        application = Application.objects.get(name__iexact=name)
        return application, False
    except Application.DoesNotExist:
        application = Application(name=name)
        application.save()
        log.info("Created new application: %s", name)
        return application, True


__all__ = ['get_or_create_application']
