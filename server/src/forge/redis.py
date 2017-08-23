from django.conf import settings
import redis


r = redis.StrictRedis(
    host=settings.REDIS_CONNECTION['HOST'],
    port=settings.REDIS_CONNECTION['PORT'],
    db=settings.REDIS_CONNECTION['DATABASE'],
)
