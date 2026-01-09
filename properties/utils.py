# properties/utils.py
import logging
from django.core.cache import cache
from django_redis import get_redis_connection

from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    cached_properties = cache.get("all_properties")

    if cached_properties is None:
        cached_properties = Property.objects.all()
        cache.set("all_properties", cached_properties, 3600)

    return cached_properties


def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(
            "Redis Metrics | Hits: %s | Misses: %s | Hit Ratio: %.2f",
            hits,
            misses,
            hit_ratio,
        )

        return metrics

    except Exception as e:
        logger.error("Failed to retrieve Redis cache metrics: %s", e)
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0,
        }
