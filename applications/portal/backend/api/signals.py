from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Antibody, STATUS
from api.services.antibody_service import get_antibodies, last_update

@receiver(post_save, sender=Antibody)
@receiver(post_delete, sender=Antibody)
def clear_antibody_cache(instance, **kwargs):
    """Clear cache when Antibody model is updated or deleted."""
    if instance.status == STATUS.CURATED:
        get_antibodies.cache_clear()
        last_update.cache_clear()
    