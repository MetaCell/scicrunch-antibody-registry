from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Antibody
from api.controllers.antibody_controller import get_antibodies
from api.controllers.api_controller import get_datainfo

@receiver(post_save, sender=Antibody)
@receiver(post_delete, sender=Antibody)
def clear_antibody_cache(sender, **kwargs):
    """Clear cache when Antibody model is updated or deleted."""
    get_antibodies.clear_cache()
    get_datainfo.clear_cache()
    