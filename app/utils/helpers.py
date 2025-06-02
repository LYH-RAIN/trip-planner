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
    """鐢熸垚UUID"""
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """鐢熸垚鐭璉D"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_share_code(length: int = 6) -> str:
    """鐢熸垚鍒嗕韩鐮�"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def md5_hash(text: str) -> str:
    """MD5鍝堝笇"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256_hash(text: str) -> str:
    """SHA256鍝堝笇"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate_phone(phone: str) -> bool:
    """楠岃瘉鎵嬫満鍙�"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """楠岃瘉閭�绠�"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def mask_phone(phone: str) -> str:
    """鎵嬫満鍙疯劚鏁�"""
    if len(phone) != 11:
        return phone
    return phone[:3] + '****' + phone[7:]


def mask_email(email: str) -> str:
    """閭�绠辫劚鏁�"""
    if '@' not in email:
        return email
    local, domain = email.split('@', 1)
    if len(local) <= 2:
        return email
    return local[:2] + '***' + '@' + domain


def format_currency(amount: Union[int, float, Decimal], currency: str = '楼') -> str:
    """鏍煎紡鍖栬揣甯�"""
    return f"{currency}{amount:,.2f}"


def format_distance(distance: Union[int, float]) -> str:
    """鏍煎紡鍖栬窛绂�"""
    if distance < 1000:
        return f"{distance:.0f}m"
    else:
        return f"{distance / 1000:.1f}km"


def format_duration(minutes: int) -> str:
    """鏍煎紡鍖栨椂闀�"""
    if minutes < 60:
        return f"{minutes}鍒嗛挓"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours}灏忔椂"
        else:
            return f"{hours}灏忔椂{mins}鍒嗛挓"


def parse_location(location_str: str) -> tuple:
    """瑙ｆ瀽鍧愭爣瀛楃�︿覆"""
    try:
        lng, lat = location_str.split(',')
        return float(lng.strip()), float(lat.strip())
    except:
        return None, None


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """璁＄畻涓ょ偣闂磋窛绂伙紙绫筹級"""
    from math import radians, cos, sin, asin, sqrt

    # 杞�鎹�涓哄姬搴�
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # haversine鍏�寮�
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000  # 鍦扮悆鍗婂緞锛堢背锛�

    return c * r


def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """鏃跺尯杞�鎹�"""
    from_timezone = pytz.timezone(from_tz)
    to_timezone = pytz.timezone(to_tz)

    # 濡傛灉datetime鏄痭aive鐨勶紝鍏堟湰鍦板寲
    if dt.tzinfo is None:
        dt = from_timezone.localize(dt)

    return dt.astimezone(to_timezone)


def get_date_range(start_date: date, end_date: date) -> List[date]:
    """鑾峰彇鏃ユ湡鑼冨洿"""
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def format_business_hours(hours_str: str) -> str:
    """鏍煎紡鍖栬惀涓氭椂闂�"""
    if not hours_str:
        return ""

    # 绠€鍗曠殑鏍煎紡鍖栧�勭悊
    hours_str = hours_str.replace(';', ' | ')
    return hours_str


def extract_numbers(text: str) -> List[float]:
    """浠庢枃鏈�涓�鎻愬彇鏁板瓧"""
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    return [float(match) for match in matches]


def clean_text(text: str) -> str:
    """娓呯悊鏂囨湰"""
    if not text:
        return ""

    # 绉婚櫎澶氫綑绌虹櫧
    text = re.sub(r'\s+', ' ', text.strip())

    # 绉婚櫎鐗规畩瀛楃��
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-.,!?()锛堬級]', '', text)

    return text


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """鎴�鏂�鏂囨湰"""
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def url_encode(text: str) -> str:
    """URL缂栫爜"""
    return quote(text, safe='')


def url_decode(text: str) -> str:
    """URL瑙ｇ爜"""
    return unquote(text)


def generate_amap_navigation_url(
        from_lng: float, from_lat: float, from_name: str,
        to_lng: float, to_lat: float, to_name: str,
        mode: str = "car"
) -> str:
    """鐢熸垚楂樺痉瀵艰埅閾炬帴"""
    # 绉诲姩绔�楂樺痉鍦板浘瀵艰埅閾炬帴
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
    """鐢熸垚缃戦〉瀵艰埅閾炬帴"""
    # 楂樺痉鍦板浘缃戦〉鐗堝�艰埅閾炬帴
    web_url = (
        f"https://uri.amap.com/navigation"
        f"?from={from_lng},{from_lat},{url_encode(from_name)}"
        f"&to={to_lng},{to_lat},{url_encode(to_name)}"
        f"&mode={mode}&src=myapp"
    )
    return web_url


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """瀹夊叏鑾峰彇瀛楀吀鍊�"""
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
    """瀹夊叏杞�鎹�涓烘暣鏁�"""
    try:
        return int(value)
    except:
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """瀹夊叏杞�鎹�涓烘诞鐐规暟"""
    try:
        return float(value)
    except:
        return default


def safe_decimal(value: Any, default: Decimal = Decimal('0')) -> Decimal:
    """瀹夊叏杞�鎹�涓篋ecimal"""
    try:
        return Decimal(str(value))
    except:
        return default


def batch_process(items: List[Any], batch_size: int = 100):
    """鎵归噺澶勭悊鐢熸垚鍣�"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def remove_duplicates(items: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    """鏍规嵁鎸囧畾閿�鍘婚噸"""
    seen = set()
    result = []
    for item in items:
        if item.get(key) not in seen:
            seen.add(item.get(key))
            result.append(item)
    return result


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """鍚堝苟瀛楀吀"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """鎵佸钩鍖栧瓧鍏�"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by(items: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    """鎸夋寚瀹氶敭鍒嗙粍"""
    groups = {}
    for item in items:
        group_key = item.get(key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


def sort_by_multiple_keys(items: List[Dict[str, Any]], keys: List[tuple]) -> List[Dict[str, Any]]:
    """鎸夊�氫釜閿�鎺掑簭

    Args:
        items: 瑕佹帓搴忕殑鍒楄〃
        keys: 鎺掑簭閿�鍒楄〃锛屾牸寮忥細[('key1', True), ('key2', False)]锛孴rue琛ㄧず鍗囧簭锛孎alse琛ㄧず闄嶅簭
    """

    def sort_key(item):
        return tuple(
            item.get(key) if reverse else -item.get(key, 0) if isinstance(item.get(key), (int, float)) else item.get(
                key)
            for key, reverse in keys
        )

    return sorted(items, key=sort_key)


class DateTimeHelper:
    """鏃ユ湡鏃堕棿杈呭姪绫�"""

    @staticmethod
    def now_in_timezone(timezone_str: str = "Asia/Shanghai") -> datetime:
        """鑾峰彇鎸囧畾鏃跺尯鐨勫綋鍓嶆椂闂�"""
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz)

    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """鏍煎紡鍖栨棩鏈熸椂闂�"""
        return dt.strftime(format_str)

    @staticmethod
    def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """瑙ｆ瀽鏃ユ湡鏃堕棿瀛楃�︿覆"""
        return datetime.strptime(dt_str, format_str)

    @staticmethod
    def get_week_range(dt: date) -> tuple:
        """鑾峰彇鎸囧畾鏃ユ湡鎵€鍦ㄥ懆鐨勫紑濮嬪拰缁撴潫鏃ユ湡"""
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        return start, end

    @staticmethod
    def get_month_range(dt: date) -> tuple:
        """鑾峰彇鎸囧畾鏃ユ湡鎵€鍦ㄦ湀鐨勫紑濮嬪拰缁撴潫鏃ユ湡"""
        start = dt.replace(day=1)
        if dt.month == 12:
            end = dt.replace(year=dt.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = dt.replace(month=dt.month + 1, day=1) - timedelta(days=1)
        return start, end

    @staticmethod
    def is_weekend(dt: date) -> bool:
        """鍒ゆ柇鏄�鍚︿负鍛ㄦ湯"""
        return dt.weekday() >= 5

    @staticmethod
    def is_holiday(dt: date) -> bool:
        """鍒ゆ柇鏄�鍚︿负鑺傚亣鏃ワ紙绠€鍗曞疄鐜帮紝鍙�鎵╁睍锛�"""
        # 杩欓噷鍙�浠ユ帴鍏ヨ妭鍋囨棩API鎴栫淮鎶よ妭鍋囨棩鍒楄〃
        holidays = [
            date(2024, 1, 1),  # 鍏冩棪
            date(2024, 2, 10),  # 鏄ヨ妭
            date(2024, 4, 4),  # 娓呮槑鑺�
            date(2024, 5, 1),  # 鍔冲姩鑺�
            date(2024, 6, 10),  # 绔�鍗堣妭
            date(2024, 9, 17),  # 涓�绉嬭妭
            date(2024, 10, 1),  # 鍥藉簡鑺�
        ]
        return dt in holidays
