from django.core.cache import cache
from .models import Property
import logging
from django.redis import get_redis_connection
logger = logging.getLogger(__name__)

def get_all_properties():
    cached_properties = cache.get("all_properties")

    if cached_properties is None:
        cached_properties = Property.objects.all()
        cache.set("all_properties", cached_properties)

    return cached_properties

def get_redis_cache_metrics():
    redis_conn = get_redis_connection("default")

    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses",0)

    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }
    logger.info(
        "Redis cache Metrics | Hits: %s | Misses: %s | Hit Ratio: %.2f",
        hits,
        misses,
        hit_ratio,
    )
    return  metrics

