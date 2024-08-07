import redis
from django.conf import settings

PER_REDIS_DB = '2'

persistent_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=PER_REDIS_DB)
