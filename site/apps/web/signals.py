from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def clear_cache_on_save(sender, instance, **kwargs):
    """
    When updating things through CMS, we want to see results immediately
    """
    if sender._meta.app_label == 'web':
        cache.clear()
