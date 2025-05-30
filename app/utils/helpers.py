import hashlib
import uuid
import random
import string
import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date, time, timedelta
from decimal import Decimal
import pytz
from urllib.parse import quote, unquote


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """生成短ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_share_code(length: int = 6) -> str:
    """生成分享码"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def md5_hash(text: str) -> str:
    """MD5哈希"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256_hash(text: str) -> str:
    """SHA256哈希"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate_phone(phone: str) -> bool:
    """验证手机号"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """验证邮箱"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if len(phone) != 11:
        return phone
    return phone[:3] + '****' + phone[7:]


def mask_email(email: str) -> str:
    """邮箱脱敏"""
    if '@' not in email:
        return email
    local, domain = email.split('@', 1)
    if len(local) <= 2:
        return email
    return local[:2] + '***' + '@' + domain


def format_currency(amount: Union[int, float, Decimal], currency: str = '¥') -> str:
    """格式化货币"""
    return f"{currency}{amount:,.2f}"


def format_distance(distance: Union[int, float]) -> str:
    """格式化距离"""
    if distance < 1000:
        return f"{distance:.0f}m"
    else:
        return f"{distance / 1000:.1f}km"


def format_duration(minutes: int) -> str:
    """格式化时长"""
    if minutes < 60:
        return f"{minutes}分钟"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours}小时"
        else:
            return f"{hours}小时{mins}分钟"


def parse_location(location_str: str) -> tuple:
    """解析坐标字符串"""
    try:
        lng, lat = location_str.split(',')
        return float(lng.strip()), float(lat.strip())
    except:
        return None, None


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """计算两点间距离（米）"""
    from math import radians, cos, sin, asin, sqrt

    # 转换为弧度
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # 地球半径（米）

    return c * r


def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """时区转换"""
    from_timezone = pytz.timezone(from_tz)
    to_timezone = pytz.timezone(to_tz)

    # 如果datetime是naive的，先本地化
    if dt.tzinfo is None:
        dt = from_timezone.localize(dt)

    return dt.astimezone(to_timezone)


def get_date_range(start_date: date, end_date: date) -> List[date]:
    """获取日期范围"""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def format_business_hours(hours_str: str) -> str:
    """格式化营业时间"""
    if not hours_str:
        return ""

    # 简单的格式化处理
    hours_str = hours_str.replace(';', ' | ')
    return hours_str


def extract_numbers(text: str) -> List[float]:
    """从文本中提取数字"""
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    return [float(match) for match in matches]


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""

    # 移除多余空白
    text = re.sub(r'\s+', ' ', text.strip())

    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-.,!?()（）]', '', text)

    return text


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """截断文本"""
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def url_encode(text: str) -> str:
    """URL编码"""
    return quote(text, safe='')


def url_decode(text: str) -> str:
    """URL解码"""
    return unquote(text)


def generate_amap_navigation_url(
        from_lng: float, from_lat: float, from_name: str,
        to_lng: float, to_lat: float, to_name: str,
        mode: str = "car"
) -> str:
    """生成高德导航链接"""
    # 移动端高德地图导航链接
    amap_url = (
        f"androidamap://route/plan/"
        f"?sourceApplication=appname"
        f"&slat={from_lat}&slon={from_lng}&sname={url_encode(from_name)}"
        f"&dlat={to_lat}&dlon={to_lng}&dname={url_encode(to_name)}"
        f"&dev=0&m=0&t={'1' if mode == 'car' else '0'}"
    )
    return amap_url


def generate_web_navigation_url(
        from_lng: float, from_lat: float, from_name: str,
        to_lng: float, to_lat: float, to_name: str,
        mode: str = "car"
) -> str:
    """生成网页导航链接"""
    # 高德地图网页版导航链接
    web_url = (
        f"https://uri.amap.com/navigation"
        f"?from={from_lng},{from_lat},{url_encode(from_name)}"
        f"&to={to_lng},{to_lat},{url_encode(to_name)}"
        f"&mode={mode}&src=myapp"
    )
    return web_url


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """安全获取字典值"""
    try:
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    except:
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """安全转换为整数"""
    try:
        return int(value)
    except:
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """安全转换为浮点数"""
    try:
        return float(value)
    except:
        return default


def safe_decimal(value: Any, default: Decimal = Decimal('0')) -> Decimal:
    """安全转换为Decimal"""
    try:
        return Decimal(str(value))
    except:
        return default


def batch_process(items: List[Any], batch_size: int = 100):
    """批量处理生成器"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def remove_duplicates(items: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """根据指定键去重"""
    seen = set()
    result = []
    for item in items:
        if item.get(key) not in seen:
            seen.add(item.get(key))
            result.append(item)
    return result


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """合并字典"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """扁平化字典"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by(items: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    """按指定键分组"""
    groups = {}
    for item in items:
        group_key = item.get(key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


def sort_by_multiple_keys(items: List[Dict[str, Any]], keys: List[tuple]) -> List[Dict[str, Any]]:
    """按多个键排序

    Args:
        items: 要排序的列表
        keys: 排序键列表，格式：[('key1', True), ('key2', False)]，True表示升序，False表示降序
    """

    def sort_key(item):
        return tuple(
            item.get(key) if reverse else -item.get(key, 0) if isinstance(item.get(key), (int, float)) else item.get(
                key)
            for key, reverse in keys
        )

    return sorted(items, key=sort_key)


class DateTimeHelper:
    """日期时间辅助类"""

    @staticmethod
    def now_in_timezone(timezone_str: str = "Asia/Shanghai") -> datetime:
        """获取指定时区的当前时间"""
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz)

    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """格式化日期时间"""
        return dt.strftime(format_str)

    @staticmethod
    def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """解析日期时间字符串"""
        return datetime.strptime(dt_str, format_str)

    @staticmethod
    def get_week_range(dt: date) -> tuple:
        """获取指定日期所在周的开始和结束日期"""
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        return start, end

    @staticmethod
    def get_month_range(dt: date) -> tuple:
        """获取指定日期所在月的开始和结束日期"""
        start = dt.replace(day=1)
        if dt.month == 12:
            end = dt.replace(year=dt.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = dt.replace(month=dt.month + 1, day=1) - timedelta(days=1)
        return start, end

    @staticmethod
    def is_weekend(dt: date) -> bool:
        """判断是否为周末"""
        return dt.weekday() >= 5

    @staticmethod
    def is_holiday(dt: date) -> bool:
        """判断是否为节假日（简单实现，可扩展）"""
        # 这里可以接入节假日API或维护节假日列表
        holidays = [
            date(2024, 1, 1),  # 元旦
            date(2024, 2, 10),  # 春节
            date(2024, 4, 4),  # 清明节
            date(2024, 5, 1),  # 劳动节
            date(2024, 6, 10),  # 端午节
            date(2024, 9, 17),  # 中秋节
            date(2024, 10, 1),  # 国庆节
        ]
        return dt in holidays
