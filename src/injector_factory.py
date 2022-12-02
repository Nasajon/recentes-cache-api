from typing import Type
from src.redis_config import redis_con


class InjectorFactory:

    @staticmethod
    def get_redis_dao():
        from src.dao.redis_dao import RedisDao
        return RedisDao(redis_con=redis_con)
        
    @staticmethod
    def get_redis_service():
        from src.service.redis_service import RedisService
        return RedisService(InjectorFactory.get_redis_dao())
        