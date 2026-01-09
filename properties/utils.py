from django.core.cache import cache
from .models import Property

def get_all_properties():
    cached_properties = cache.get("all_properties")

    if cached_properties is None:
        cached_properties = Property.objects.all()
        cache.set("all_properties", cached_properties)

    return cached_properties