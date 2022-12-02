from datetime import datetime
from typing import Dict, List
from src.dao.redis_dao import RedisDao
from nsj_gcf_utils.json_util import json_dumps, json_loads
from src.settings import EXPIRATION_SECONDS, MAX_HISTORICS, DATETIME_FORMAT
class RedisService:
    
    def __init__(self, redis_dao: RedisDao) -> None:
        self._redis_dao = redis_dao
        
        
    def _purge_expirated(self, key: str, primary_key: str):
        data = self.get(key)
        now = datetime.now()
        result_list = []
        expiration_list = []
        values_list = []
        
        
        if (data is not None) and data:
            expiration_list = data['expiration']
            result_expiration_list = expiration_list[:]
            values_list = data['values']
            value_set = set()
            for value in values_list:
                value_set.add(value[primary_key])
                
            if expiration_list:
                for obj in expiration_list:
                    touched_date = datetime.strptime(obj['touched'], DATETIME_FORMAT )
                    interval = now - touched_date
                    seconds = interval.total_seconds()
                    if seconds > float(EXPIRATION_SECONDS):
                        result_expiration_list.remove(obj)
                        value_set.remove(obj['id'])
                        
                for obj in values_list:
                    if obj[primary_key] not in value_set:
                        continue
                    result_list.append(obj)
        data = {
            'expiration' : result_expiration_list, 
            'values' : result_list
        }
        self._redis_dao.save(key, data)
        
        
    
    def save_in_list(self, key: str, data : Dict[str, List[any]], primary_key: str, purge = True):
        self._purge_expirated(key, primary_key)
            
        stored = self.get(key)
        now = datetime.now()
        values = stored['values']
        expirations =stored['expiration']
        
        for value in values:
            if data[primary_key] == value[primary_key]:
                values.remove(value)
        for expiration in expirations:
            if expiration['id'] == data[primary_key]:
                expirations.remove(expiration)
        
        values.insert(0, data)
        expirations.append({
            'id': data[primary_key], 
            'touched' : now.strftime(DATETIME_FORMAT)
        })
        
        new_value = {
            'values': values, 
            'expiration': expirations
        }
        self._redis_dao.save(key, new_value)
        
        
        
        
    
    def get_list(self, key, primary_key):
        self._purge_expirated(key, primary_key)
        data =  self._redis_dao.get_list(key)
        if 'values' in data:
            return data['values']
        return data
    
    def get(self, key):
        return self._redis_dao.get_list(key)