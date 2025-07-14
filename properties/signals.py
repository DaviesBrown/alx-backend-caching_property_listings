from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver(post_save, sender=Property)
def post_save_handler(sender, instance, **kwargs):
    """Invalidate cache when a Property is saved (created or updated)"""
    cache.delete('all_properties')
    print(f'Cache invalidated: Property {instance.id} was saved')

@receiver(post_delete, sender=Property)
def post_delete_handler(sender, instance, **kwargs):
    """Invalidate cache when a Property is deleted"""
    cache.delete('all_properties')
    print(f'Cache invalidated: Property {instance.id} was deleted')
