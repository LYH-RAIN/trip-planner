import redis
import json
import pickle
from typing import Any, Optional, Union, Dict, List
from datetime import timedelta
from functools import wraps
from app.core.config import settings


class RedisCache:
    """Redis缓存管理器"""

    def __init__(self):
        self.redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=False,  # 支持pickle序列化
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True
        )

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存值"""
        try:
            value = self.redis_client.get(key)
            if value is None:
                return default

            # 尝试JSON反序列化
            try:
                return json.loads(value.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # 如果JSON失败，尝试pickle反序列化
                try:
                    return pickle.loads(value)
                except:
                    return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis get error: {e}")
            return default

    def set(self, key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
        """设置缓存值"""
        try:
            # 尝试JSON序列化
            try:
                serialized_value = json.dumps(value, ensure_ascii=False, default=str)
            except (TypeError, ValueError):
                # 如果JSON失败，使用pickle序列化
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
        """删除缓存"""
        try:
            return self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Redis delete error: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False

    def expire(self, key: str, time: Union[int, timedelta]) -> bool:
        """设置过期时间"""
        try:
            if isinstance(time, timedelta):
                time = int(time.total_seconds())
            return self.redis_client.expire(key, time)
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False

    def ttl(self, key: str) -> int:
        """获取剩余过期时间"""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            print(f"Redis ttl error: {e}")
            return -1

    def incr(self, key: str, amount: int = 1) -> int:
        """递增"""
        try:
            return self.redis_client.incr(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return 0

    def decr(self, key: str, amount: int = 1) -> int:
        """递减"""
        try:
            return self.redis_client.decr(key, amount)
        except Exception as e:
            print(f"Redis decr error: {e}")
            return 0

    def hget(self, name: str, key: str) -> Any:
        """获取哈希字段值"""
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
        """设置哈希字段值"""
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
        """获取所有哈希字段"""
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
        """删除哈希字段"""
        try:
            return self.redis_client.hdel(name, *keys)
        except Exception as e:
            print(f"Redis hdel error: {e}")
            return 0

    def sadd(self, name: str, *values: Any) -> int:
        """添加集合成员"""
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
        """删除集合成员"""
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
        """获取集合所有成员"""
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


# 全局缓存实例
cache = RedisCache()


# 缓存键常量
class CacheKeys:
    """缓存键常量"""

    # 用户相关
    USER_INFO = "user:info:{user_id}"
    USER_TRIPS = "user:trips:{user_id}"
    USER_FAVORITES = "user:favorites:{user_id}"

    # 行程相关
    TRIP_DETAIL = "trip:detail:{trip_id}"
    TRIP_OVERVIEW = "trip:overview:{trip_id}"
    TRIP_DAY = "trip:day:{trip_id}:{day_index}"
    TRIP_FOODS = "trip:foods:{trip_id}"

    # 地点相关
    LOCATION_DETAIL = "location:detail:{poi_id}"
    LOCATION_SEARCH = "location:search:{keyword}:{city}:{page}"
    LOCATION_AROUND = "location:around:{location}:{radius}:{type}:{page}"

    # 天气相关
    WEATHER_FORECAST = "weather:forecast:{city}:{date}"

    # 统计相关
    DAILY_STATS = "stats:daily:{date}"
    USER_ACTIVITY = "stats:user:{user_id}:{date}"


# 缓存过期时间常量
class CacheTTL:
    """缓存过期时间常量（秒）"""

    MINUTE = 60
    HOUR = 60 * 60
    DAY = 24 * 60 * 60
    WEEK = 7 * 24 * 60 * 60

    # 具体业务缓存时间
    USER_INFO = 30 * MINUTE
    TRIP_DETAIL = 10 * MINUTE
    LOCATION_SEARCH = 2 * HOUR
    WEATHER_FORECAST = 30 * MINUTE
    DAILY_STATS = DAY


def cache_result(key_pattern: str, expire: int = CacheTTL.HOUR):
    """缓存装饰器"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = key_pattern.format(*args, **kwargs)

            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, expire)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = key_pattern.format(*args, **kwargs)

            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache.set(cache_key, result, expire)
            return result

        # 根据函数是否为协程选择包装器
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def invalidate_cache_pattern(pattern: str):
    """删除匹配模式的缓存"""
    try:
        keys = cache.redis_client.keys(pattern)
        if keys:
            cache.redis_client.delete(*keys)
    except Exception as e:
        print(f"Invalidate cache error: {e}")
