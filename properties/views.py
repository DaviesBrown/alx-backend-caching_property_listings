from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import get_all_properties, get_redis_cache_metrics

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {'properties': properties, 'cache_metrics': get_redis_cache_metrics()})
