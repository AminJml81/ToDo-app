from django.utils import timezone

from celery import shared_task
from decouple import config
import redis


@shared_task
def delete_yesterday_caches():
    r = redis.StrictRedis(
        host=config("REDIS_HOST_NAME", 'localhost'),
        port=config("REDIS_PORT", cast=int, default=6379),
        db=config("REDIS_WEATHER_DB_NUMBER", default=0, cast=int),
    )
    yesterday = (timezone.now() - timezone.timedelta(days=1)).day
    for key in r.keys(f":1:{yesterday}-*"):
        r.delete(key)
