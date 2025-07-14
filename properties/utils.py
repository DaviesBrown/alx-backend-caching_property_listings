from .models import Property
from django.core.cache import cache

def get_all_properties():
    properties = cache.get('all_properties')
    if properties:
        return properties
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)
    return properties