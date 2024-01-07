#  ==================================================================================================
#  File Name: utils.py
#  Description: File to define helper class for Redis.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

#from functools import cache
import json
import redis
#import json
rds = redis.StrictRedis(port=6379, db=0)

class Red:
    def set(cache_key,data):
        data = json.dumps(data)
        rds.set(cache_key,data)
        return True

    def get(cache_key):
        cache_data=rds.get(cache_key)
        if not cache_data:
            return None
        cache_data = json.loads(cache_data)
        cache_data = cache_data.decode("utf-8")
        return cache_data
