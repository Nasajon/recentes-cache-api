from typing import Set, Type
from redis import Redis
from nsj_gcf_utils.json_util import json_dumps, json_loads
from src.settings import MAX_HISTORICS

class RedisDao:
    def __init__(self, redis_con : Redis) -> None:
        self.redis_con = redis_con 

    def save(self, key: str, value: any):
        self.redis_con.set(key, json_dumps(value))

    def get_list(self, key: str):
        list_txt = self.redis_con.get(key)
        if list_txt is None or list_txt == '':
            return []
        return json_loads(list_txt)
        
        
