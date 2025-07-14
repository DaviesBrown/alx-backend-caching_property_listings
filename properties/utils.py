import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')
    if properties:
        return properties
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)
    return properties

# Initialize logger
logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics
    Returns dictionary with:
        - hits: Total keyspace hits
        - misses: Total keyspace misses
        - hit_ratio: Calculated hit ratio (0.0 to 1.0)
        - total_operations: Total cache operations
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info()
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_operations = hits + misses
        hit_ratio = hits / total_operations if total_operations > 0 else 0.0

        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio,
            'total_operations': total_operations
        }
        
        # Log metrics
        logger.info(
            f"Redis Cache Metrics: "
            f"{hits} hits, {misses} misses, "
            f"hit ratio: {hit_ratio:.2f}"
        )
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {str(e)}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0,
            'total_operations': 0,
            'error': str(e)
        }

