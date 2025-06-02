import redis
import json
import pickle
from typing import Any, Optional, Union, Dict, List
from datetime import timedelta
from functools import wraps
from app.core.config import settings


class RedisCache:
    """Redis缂撳瓨绠＄悊鍣�"""

    def __init__(self):
        self.redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=False,  # 鏀�鎸乸ickle搴忓垪鍖�
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )

    def get(self, key: str, default: Any = None) -> Any:
        """鑾峰彇缂撳瓨鍊�"""
        try:
            value = self.redis_client.get(key)
            if value is None:
                return default

            # 灏濊瘯JSON鍙嶅簭鍒楀寲
            try:
                return json.loads(value.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # 濡傛灉JSON澶辫触锛屽皾璇昿ickle鍙嶅簭鍒楀寲
                try:
                    return pickle.loads(value)
                except:
                    return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis get error: {e}")
            return default

    def set(self, key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
        """璁剧疆缂撳瓨鍊�"""
        try:
            # 灏濊瘯JSON搴忓垪鍖�
            try:
                serialized_value = json.dumps(value, ensure_ascii=False, default=str)
            except (TypeError, ValueError):
                # 濡傛灉JSON澶辫触锛屼娇鐢╬ickle搴忓垪鍖�
                serialized_value = pickle.dumps(value)

            if expire:
                if isinstance(expire, timedelta):
                    expire = int(expire.total_seconds())
                return self.redis_client.setex(key, expire, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    def delete(self, *keys: str) -> int:
        """鍒犻櫎缂撳瓨"""
        try:
            return self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Redis delete error: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """妫€鏌ラ敭鏄�鍚﹀瓨鍦�"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False

    def expire(self, key: str, time: Union[int, timedelta]) -> bool:
        """璁剧疆杩囨湡鏃堕棿"""
        try:
            if isinstance(time, timedelta):
                time = int(time.total_seconds())
            return self.redis_client.expire(key, time)
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False

    def ttl(self, key: str) -> int:
        """鑾峰彇鍓╀綑杩囨湡鏃堕棿"""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            print(f"Redis ttl error: {e}")
            return -1

    def incr(self, key: str, amount: int = 1) -> int:
        """閫掑��"""
        try:
            return self.redis_client.incr(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return 0

    def decr(self, key: str, amount: int = 1) -> int:
        """閫掑噺"""
        try:
            return self.redis_client.decr(key, amount)
        except Exception as e:
            print(f"Redis decr error: {e}")
            return 0

    def hget(self, name: str, key: str) -> Any:
        """鑾峰彇鍝堝笇瀛楁�靛€�"""
        try:
            value = self.redis_client.hget(name, key)
            if value is None:
                return None

            try:
                return json.loads(value.decode('utf-8'))
            except:
                return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis hget error: {e}")
            return None

    def hset(self, name: str, key: str, value: Any) -> bool:
        """璁剧疆鍝堝笇瀛楁�靛€�"""
        try:
            try:
                serialized_value = json.dumps(value, ensure_ascii=False, default=str)
            except:
                serialized_value = str(value)

            return bool(self.redis_client.hset(name, key, serialized_value))
        except Exception as e:
            print(f"Redis hset error: {e}")
            return False

    def hgetall(self, name: str) -> Dict[str, Any]:
        """鑾峰彇鎵€鏈夊搱甯屽瓧娈�"""
        try:
            result = self.redis_client.hgetall(name)
            decoded_result = {}
            for k, v in result.items():
                key = k.decode('utf-8') if isinstance(k, bytes) else k
                try:
                    value = json.loads(v.decode('utf-8'))
                except:
                    value = v.decode('utf-8') if isinstance(v, bytes) else v
                decoded_result[key] = value
            return decoded_result
        except Exception as e:
            print(f"Redis hgetall error: {e}")
            return {}

    def hdel(self, name: str, *keys: str) -> int:
        """鍒犻櫎鍝堝笇瀛楁��"""
        try:
            return self.redis_client.hdel(name, *keys)
        except Exception as e:
            print(f"Redis hdel error: {e}")
            return 0

    def sadd(self, name: str, *values: Any) -> int:
        """娣诲姞闆嗗悎鎴愬憳"""
        try:
            serialized_values = []
            for value in values:
                try:
                    serialized_values.append(json.dumps(value, ensure_ascii=False, default=str))
                except:
                    serialized_values.append(str(value))
            return self.redis_client.sadd(name, *serialized_values)
        except Exception as e:
            print(f"Redis sadd error: {e}")
            return 0

    def srem(self, name: str, *values: Any) -> int:
        """鍒犻櫎闆嗗悎鎴愬憳"""
        try:
            serialized_values = []
            for value in values:
                try:
                    serialized_values.append(json.dumps(value, ensure_ascii=False, default=str))
                except:
                    serialized_values.append(str(value))
            return self.redis_client.srem(name, *serialized_values)
        except Exception as e:
            print(f"Redis srem error: {e}")
            return 0

    def smembers(self, name: str) -> set:
        """鑾峰彇闆嗗悎鎵€鏈夋垚鍛�"""
        try:
            members = self.redis_client.smembers(name)
            result = set()
            for member in members:
                try:
                    value = json.loads(member.decode('utf-8'))
                except:
                    value = member.decode('utf-8') if isinstance(member, bytes) else member
                result.add(value)
            return result
        except Exception as e:
            print(f"Redis smembers error: {e}")
            return set()


# 鍏ㄥ眬缂撳瓨瀹炰緥
cache = RedisCache()


# 缂撳瓨閿�甯搁噺
class CacheKeys:
    """缂撳瓨閿�甯搁噺"""

    # 鐢ㄦ埛鐩稿叧
    USER_INFO = "user:info:{user_id}"
    USER_TRIPS = "user:trips:{user_id}"
    USER_FAVORITES = "user:favorites:{user_id}"

    # 琛岀▼鐩稿叧
    TRIP_DETAIL = "trip:detail:{trip_id}"
    TRIP_OVERVIEW = "trip:overview:{trip_id}"
    TRIP_DAY = "trip:day:{trip_id}:{day_index}"
    TRIP_FOODS = "trip:foods:{trip_id}"

    # 鍦扮偣鐩稿叧
    LOCATION_DETAIL = "location:detail:{poi_id}"
    LOCATION_SEARCH = "location:search:{keyword}:{city}:{page}"
    LOCATION_AROUND = "location:around:{location}:{radius}:{type}:{page}"

    # 澶╂皵鐩稿叧
    WEATHER_FORECAST = "weather:forecast:{city}:{date}"

    # 缁熻�＄浉鍏�
    DAILY_STATS = "stats:daily:{date}"
    USER_ACTIVITY = "stats:user:{user_id}:{date}"


# 缂撳瓨杩囨湡鏃堕棿甯搁噺
class CacheTTL:
    """缂撳瓨杩囨湡鏃堕棿甯搁噺锛堢�掞級"""

    MINUTE = 60
    HOUR = 60 * 60
    DAY = 24 * 60 * 60
    WEEK = 7 * 24 * 60 * 60

    # 鍏蜂綋涓氬姟缂撳瓨鏃堕棿
    USER_INFO = 30 * MINUTE
    TRIP_DETAIL = 10 * MINUTE
    LOCATION_SEARCH = 2 * HOUR
    WEATHER_FORECAST = 30 * MINUTE
    DAILY_STATS = DAY


def cache_result(key_pattern: str, expire: int = CacheTTL.HOUR):
    """缂撳瓨瑁呴グ鍣�"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 鐢熸垚缂撳瓨閿�
            cache_key = key_pattern.format(*args, **kwargs)

            # 灏濊瘯浠庣紦瀛樿幏鍙�
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 鎵ц�屽嚱鏁板苟缂撳瓨缁撴灉
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, expire)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 鐢熸垚缂撳瓨閿�
            cache_key = key_pattern.format(*args, **kwargs)

            # 灏濊瘯浠庣紦瀛樿幏鍙�
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 鎵ц�屽嚱鏁板苟缂撳瓨缁撴灉
            result = func(*args, **kwargs)
            cache.set(cache_key, result, expire)
            return result

        # 鏍规嵁鍑芥暟鏄�鍚︿负鍗忕▼閫夋嫨鍖呰�呭櫒
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def invalidate_cache_pattern(pattern: str):
    """鍒犻櫎鍖归厤妯″紡鐨勭紦瀛�"""
    try:
        keys = cache.redis_client.keys(pattern)
        if keys:
            cache.redis_client.delete(*keys)
    except Exception as e:
        print(f"Invalidate cache error: {e}")
