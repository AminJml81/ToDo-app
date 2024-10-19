from django.utils import timezone

from celery import shared_task
from decouple import config
import redis


@shared_task
def delete_yesterday_caches():
    r = redis.StrictRedis(
        host=config("REDIS_HOST_NAME"),
        port=config("REDIS_PORT"),
        db=config("REDIS_WEATHER_DB_NUMBER"),
    )
    yesterday = (timezone.now() - timezone.timedelta(days=1)).day
    for key in r.keys(f":1:{yesterday}-*"):
        r.delete(key)
