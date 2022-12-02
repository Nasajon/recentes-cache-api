from redis import Redis
from src.settings import REDIS_DB, REDIS_HOST, REDIS_PORT

redis_con = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset="utf-8", decode_responses=True)
