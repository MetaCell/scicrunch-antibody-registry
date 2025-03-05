from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Antibody
from api.services.antibody_service import get_antibodies, count, last_update

@receiver(post_save, sender=Antibody)
@receiver(post_delete, sender=Antibody)
def clear_antibody_cache(sender, **kwargs):
    """Clear cache when Antibody model is updated or deleted."""
    get_antibodies.clear_cache()
    count.clear_cache()
    last_update.clear_cache()
    