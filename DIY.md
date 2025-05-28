# 行程规划系统数据库设计与API规划
### 1 用户表 (users)
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    open_id VARCHAR(64) UNIQUE COMMENT '微信OpenID',
    union_id VARCHAR(64) COMMENT '微信UnionID',
    nickname VARCHAR(64) COMMENT '用户昵称',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    gender TINYINT COMMENT '性别：0未知，1男，2女',
    country VARCHAR(64) COMMENT '国家',
    province VARCHAR(64) COMMENT '省份',
    city VARCHAR(64) COMMENT '城市',
    phone VARCHAR(20) COMMENT '手机号',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    INDEX idx_open_id (open_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';
```

### 2 行程表 (trips)
```sql
CREATE TABLE trips (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    title VARCHAR(128) NOT NULL COMMENT '行程标题',
    description TEXT COMMENT '行程描述',
    cover_image VARCHAR(255) COMMENT '封面图片',
    start_date DATE NOT NULL COMMENT '开始日期',
    end_date DATE NOT NULL COMMENT '结束日期',
    days INT NOT NULL COMMENT '行程天数',
    departure VARCHAR(64) NOT NULL COMMENT '出发地',
    destinations TEXT COMMENT '目的地JSON，包含名称和停留天数',
    travel_mode TINYINT DEFAULT 1 COMMENT '交通方式：1自驾，2公共交通',
    people_count INT DEFAULT 1 COMMENT '出行人数',
    preferences TEXT COMMENT '偏好JSON',
    overview TEXT COMMENT '行程总览',
    status TINYINT DEFAULT 0 COMMENT '状态：0规划中，1已完成，2已取消',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    like_count INT DEFAULT 0 COMMENT '点赞次数',
    share_count INT DEFAULT 0 COMMENT '分享次数',
    is_public TINYINT DEFAULT 0 COMMENT '是否公开：0私密，1公开',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_public (is_public, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程表';
```

### 3 行程日程表 (trip_days)
```sql
CREATE TABLE trip_days (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_index INT NOT NULL COMMENT '第几天',
    date DATE NOT NULL COMMENT '具体日期',
    title VARCHAR(128) COMMENT '当天标题',
    summary TEXT COMMENT '当天概述',
    city VARCHAR(64) COMMENT '当天所在城市',
    weather VARCHAR(32) COMMENT '天气',
    temperature VARCHAR(16) COMMENT '温度范围',
    accommodation VARCHAR(255) COMMENT '住宿地点',
    accommodation_price DECIMAL(10,2) COMMENT '住宿费用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    UNIQUE KEY uk_trip_day (trip_id, day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程日程表';
```

### 4 行程景点表 (trip_places)
```sql
CREATE TABLE trip_places (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_id BIGINT NOT NULL COMMENT '行程日程ID',
    day_index INT NOT NULL COMMENT '第几天',
    visit_order INT NOT NULL COMMENT '当天访问顺序',
    name VARCHAR(128) NOT NULL COMMENT '景点名称',
    address VARCHAR(255) COMMENT '详细地址',
    city VARCHAR(64) COMMENT '所在城市',
    category VARCHAR(32) COMMENT '分类',
    image_url VARCHAR(255) COMMENT '图片URL',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '门票价格',
    start_time TIME COMMENT '开始时间',
    end_time TIME COMMENT '结束时间',
    duration INT COMMENT '游玩时长(分钟)',
    transportation VARCHAR(32) COMMENT '交通方式',
    transportation_details TEXT COMMENT '交通详情',
    distance DECIMAL(10,2) COMMENT '与上一地点距离(km)',
    notes TEXT COMMENT '备注',
    is_highlight TINYINT DEFAULT 0 COMMENT '是否为亮点：0否，1是',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程景点表';
```

### 5 行程美食表 (trip_foods)
```sql
CREATE TABLE trip_foods (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_id BIGINT COMMENT '行程日程ID',
    day_index INT COMMENT '第几天',
    name VARCHAR(128) NOT NULL COMMENT '美食名称',
    address VARCHAR(255) COMMENT '详细地址',
    city VARCHAR(64) COMMENT '所在城市',
    category VARCHAR(32) COMMENT '分类',
    image_url VARCHAR(255) COMMENT '图片URL',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '人均价格',
    description TEXT COMMENT '描述',
    recommendation TEXT COMMENT '推荐理由',
    business_hours VARCHAR(255) COMMENT '营业时间',
    is_highlight TINYINT DEFAULT 0 COMMENT '是否为亮点：0否，1是',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程美食表';
```

### 6 AI模型调用记录表 (ai_model_calls)
```sql
CREATE TABLE ai_model_calls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    trip_id BIGINT COMMENT '关联行程ID',
    prompt TEXT NOT NULL COMMENT '输入提示词',
    response TEXT COMMENT 'AI返回结果',
    model_name VARCHAR(64) COMMENT '模型名称',
    call_type VARCHAR(32) COMMENT '调用类型：trip_generate, trip_update, etc',
    status TINYINT DEFAULT 0 COMMENT '状态：0处理中，1成功，2失败',
    error_message VARCHAR(255) COMMENT '错误信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI模型调用记录表';
```

## 2. API设计
### 2.1 用户认证API
```plain
POST /api/v1/auth/wechat/login
```

**请求参数**:

```json
{
  "code": "微信授权code"
}
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "jwt_token",
    "user": {
      "id": 1,
      "nickname": "用户昵称",
      "avatarUrl": "头像URL",
      "isNewUser": false
    }
  }
}
```

### 2.2 地点查询API（使用高德API）
#### 2.2.1 行政区域查询API
```plain
GET /api/v1/locations/districts
```

**请求参数**:

```plain
keywords: 查询关键字（可选，如"广东省"、"广州市"）
subdistrict: 子级行政区级数，0-3（可选，默认1）
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "districts": [
      {
        "id": "440000",
        "name": "广东省",
        "center": "113.280637,23.125178",
        "level": "province",
        "children": [
          {
            "id": "440100",
            "name": "广州市",
            "center": "113.280637,23.125178",
            "level": "city"
          },
          {
            "id": "440200",
            "name": "韶关市",
            "center": "113.591544,24.801322",
            "level": "city"
          }
        ]
      }
    ]
  }
}
```

#### 2.2.2 地点搜索API
```plain
GET /api/v1/locations/search
```

**请求参数**:

```plain
keyword: 搜索关键词（必填）
city: 城市名称或adcode（可选，如"广州"或"440100"）
page: 页码（可选，默认1）
page_size: 每页记录数（可选，默认20）
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 42,
    "locations": [
      {
        "id": "B0FFHCF6VV",
        "name": "丹霞山",
        "type": "景点",
        "address": "广东省韶关市仁化县丹霞山镇",
        "location": "113.736513,25.022758",
        "district": "仁化县",
        "city": "韶关市",
        "province": "广东省",
        "image_url": "http://store.is.autonavi.com/showpic/231c877c3d3c4d64ff0ee64862df97f7"
      },
      {
        "id": "B0FFG9KCPD",
        "name": "南华寺",
        "type": "景点",
        "address": "广东省韶关市曲江区马坝镇",
        "location": "113.601624,24.969615",
        "district": "曲江区",
        "city": "韶关市",
        "province": "广东省",
        "image_url": "http://store.is.autonavi.com/showpic/7a3d547761b7281fb15f1a4b0e1141b0"
      }
    ]
  }
}
```

#### 2.2.3 地点详情API
```plain
GET /api/v1/locations/detail
```

**请求参数**:

```plain
id: 地点ID（必填，如"B0FFHCF6VV"）
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "B0FFHCF6VV",
    "name": "丹霞山",
    "type": "景点",
    "type_code": "110202",
    "address": "广东省韶关市仁化县丹霞山镇",
    "location": "113.736513,25.022758",
    "district": "仁化县",
    "city": "韶关市",
    "province": "广东省",
    "tel": "0751-6292721",
    "website": "http://www.danxiashan.org.cn",
    "business_hours": "08:00-17:30",
    "rating": 4.9,
    "price": 120,
    "images": [
      "http://store.is.autonavi.com/showpic/231c877c3d3c4d64ff0ee64862df97f7",
      "http://store.is.autonavi.com/showpic/55df2b6fa310ca5b60f7ee6e"
    ],
    "tags": ["世界自然遗产", "国家5A级景区", "地质公园"],
    "description": "丹霞山以赤壁丹崖为特色，是世界自然遗产，以奇特的红砂岩地貌著称。",
    "transportation": "可乘坐韶关至丹霞山的旅游专线车，或自驾前往。",
    "tips": "建议游玩时间4-6小时，门票120元/人，学生票60元/人。"
  }
}
```

#### 2.2.4. 周边搜索API
```plain
GET /api/v1/locations/around
```

**请求参数**:

```plain
location: 中心点坐标，格式为"经度,纬度"（必填，如"113.736513,25.022758"）
radius: 搜索半径，单位米（可选，默认3000，最大50000）
type: 搜索类型（可选，如"餐饮"、"住宿"、"景点"、"购物"）
page: 页码（可选，默认1）
page_size: 每页记录数（可选，默认20）
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 15,
    "locations": [
      {
        "id": "B0FFHCF6XX",
        "name": "丹霞山景区餐厅",
        "type": "餐饮",
        "address": "广东省韶关市仁化县丹霞山镇景区内",
        "location": "113.735513,25.021758",
        "distance": 150,
        "district": "仁化县",
        "city": "韶关市",
        "province": "广东省",
        "tel": "0751-6292722",
        "business_hours": "08:30-20:00",
        "rating": 4.2,
        "price": 80
      },
      {
        "id": "B0FFHCF6YY",
        "name": "丹霞山宾馆",
        "type": "住宿",
        "address": "广东省韶关市仁化县丹霞山镇景区附近",
        "location": "113.738513,25.023758",
        "distance": 320,
        "district": "仁化县",
        "city": "韶关市",
        "province": "广东省",
        "tel": "0751-6292723",
        "rating": 4.5,
        "price": 380
      }
    ]
  }
}
```

### 2.3 行程管理API
#### 创建行程
```plain
POST /api/v1/trips
```

**请求参数**:

```json
{
  "title": "广东四日游",
  "departure": "广州",
  "destinations": ["韶关", "清远"],
  "startDate": "2023-05-07",
  "endDate": "2023-05-10",
  "peopleCount": 2,
  "travelMode": 1,
  "preferences": ["自然风光", "摄影", "美食"]
}
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "title": "广东四日游",
    "startDate": "2023-05-07",
    "endDate": "2023-05-10"
  }
}
```

#### 获取行程列表
```plain
GET /api/v1/trips
```

**请求参数**:

```plain
status: 行程状态(all/planning/completed/cancelled)
page: 页码
page_size: 每页数量
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 5,
    "list": [
      {
        "id": 123,
        "title": "广东四日游",
        "cover_image": "https://example.com/cover.jpg",
        "startDate": "2023-05-07",
        "endDate": "2023-05-10",
        "days": 4,
        "destinations": ["韶关", "清远"],
        "status": 1,
        "createdAt": "2023-04-20T12:00:00Z"
      }
    ]
  }
}
```

#### 获取行程详情
```plain
GET /api/v1/trips/{tripId}
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "title": "广东四日游",
    "cover_image": "https://example.com/cover.jpg",
    "description": "这是一个感受广东山水风景的四日游行程...",
    "startDate": "2023-05-07",
    "endDate": "2023-05-10",
    "days": 4,
    "departure": "广州",
    "destinations": ["韶关", "清远"],
    "travelMode": 1,
    "peopleCount": 2,
    "preferences": ["自然风光", "摄影", "美食"],
    "status": 1,
    "overview": "本次行程将游览丹霞山、南华寺、清远峡谷等著名景点，感受广东独特的山水风景...",
    "days_detail": [
      {
        "day_index": 1,
        "date": "2023-05-07",
        "title": "DAY1",
        "summary": "抵达韶关，游览南华寺和丹霞山",
        "city": "韶关",
        "weather": "晴",
        "temperature": "27°-31°",
        "places": [
          {
            "id": 101,
            "name": "南华寺",
            "address": "广东省韶关市曲江区马坝镇",
            "visit_order": 1,
            "start_time": "09:00",
            "end_time": "11:00",
            "transportation": "自驾",
            "notes": "南华寺是中国佛教禅宗六祖惠能的道场",
            "is_highlight": true
          },
          {
            "id": 102,
            "name": "丹霞山",
            "address": "广东省韶关市仁化县丹霞山镇",
            "visit_order": 2,
            "start_time": "13:00",
            "end_time": "17:00",
            "transportation": "自驾",
            "notes": "丹霞山以赤壁丹崖为特色，是世界自然遗产",
            "is_highlight": true
          }
        ]
      },
      {
        "day_index": 2,
        "date": "2023-05-08",
        "title": "DAY2",
        "summary": "游览韶关其他景点",
        "city": "韶关",
        "weather": "多云",
        "temperature": "25°-30°",
        "places": [
          {
            "id": 103,
            "name": "丹霞山",
            "address": "广东省韶关市仁化县丹霞山镇",
            "visit_order": 1,
            "start_time": "08:00",
            "end_time": "12:00",
            "transportation": "自驾",
            "notes": "继续游览丹霞山其他景点"
          }
        ]
      }
    ],
    "foods": [
      {
        "id": 301,
        "name": "云南大理三道茶美食餐厅",
        "address": "广东省韶关市XX路XX号",
        "city": "韶关",
        "image_url": "https://example.com/food1.jpg",
        "rating": 4.8,
        "price": 120,
        "description": "云南特色美食，不错的用餐体验",
        "recommendation": "三道茶、过桥米线、汽锅鸡",
        "is_highlight": true
      }
    ],
    "createdAt": "2023-04-20T12:00:00Z"
  }
}
```

#### 获取行程总览
```plain
GET /api/v1/trips/{tripId}/overview
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "title": "广东四日游",
    "cover_image": "https://example.com/cover.jpg",
    "days": 4,
    "startDate": "2023-05-07",
    "endDate": "2023-05-10",
    "overview": "本次行程将游览丹霞山、南华寺、清远峡谷等著名景点，感受广东独特的山水风景...",
    "highlights": [
      {
        "day_index": 1,
        "name": "南华寺",
        "image_url": "https://example.com/nanhuasi.jpg"
      },
      {
        "day_index": 1,
        "name": "丹霞山",
        "image_url": "https://example.com/danxiashan.jpg"
      }
    ],
    "days_summary": [
      {
        "day_index": 1,
        "date": "2023-05-07",
        "title": "DAY1",
        "summary": "抵达韶关，游览南华寺和丹霞山",
        "city": "韶关",
        "weather": "晴",
        "temperature": "27°-31°",
        "main_places": ["南华寺", "丹霞山"]
      },
      {
        "day_index": 2,
        "date": "2023-05-08",
        "title": "DAY2",
        "summary": "游览韶关其他景点",
        "city": "韶关",
        "weather": "多云",
        "temperature": "25°-30°",
        "main_places": ["丹霞山", "广东大峡谷", "古村寨"]
      }
    ],
    "food_highlights": [
      {
        "id": 301,
        "name": "云南大理三道茶美食餐厅",
        "image_url": "https://example.com/food1.jpg",
        "rating": 4.8,
        "price": 120
      }
    ]
  }
}
```

#### 获取行程日程详情
```plain
GET /api/v1/trips/{tripId}/days/{dayIndex}
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "trip_id": 123,
    "day_index": 1,
    "date": "2023-05-07",
    "title": "DAY1",
    "summary": "抵达韶关，游览南华寺和丹霞山",
    "city": "韶关",
    "weather": "晴",
    "temperature": "27°-31°",
    "accommodation": "韶关XX酒店",
    "places": [
      {
        "id": 101,
        "name": "南华寺",
        "address": "广东省韶关市曲江区马坝镇",
        "category": "文化古迹",
        "image_url": "https://example.com/nanhuasi.jpg",
        "rating": 4.7,
        "price": 80,
        "visit_order": 1,
        "start_time": "09:00",
        "end_time": "11:00",
        "duration": 120,
        "transportation": "自驾",
        "transportation_details": "从酒店自驾前往，约30分钟",
        "notes": "南华寺是中国佛教禅宗六祖惠能的道场",
        "is_highlight": true
      },
      {
        "id": 102,
        "name": "丹霞山",
        "address": "广东省韶关市仁化县丹霞山镇",
        "category": "自然风光",
        "image_url": "https://example.com/danxiashan.jpg",
        "rating": 4.9,
        "price": 120,
        "visit_order": 2,
        "start_time": "13:00",
        "end_time": "17:00",
        "duration": 240,
        "transportation": "自驾",
        "transportation_details": "从南华寺自驾前往，约45分钟",
        "notes": "丹霞山以赤壁丹崖为特色，是世界自然遗产",
        "is_highlight": true
      }
    ],
    "foods": [
      {
        "id": 301,
        "name": "云南大理三道茶美食餐厅",
        "address": "广东省韶关市XX路XX号",
        "category": "云南菜",
        "image_url": "https://example.com/food1.jpg",
        "rating": 4.8,
        "price": 120,
        "description": "云南特色美食，不错的用餐体验",
        "recommendation": "三道茶、过桥米线、汽锅鸡",
        "business_hours": "10:00-22:00",
        "is_highlight": true
      }
    ]
  }
}
```

#### 获取行程美食攻略
```plain
GET /api/v1/trips/{tripId}/foods
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "trip_id": 123,
    "total": 5,
    "foods": [
      {
        "id": 301,
        "name": "云南大理三道茶美食餐厅",
        "address": "广东省韶关市XX路XX号",
        "city": "韶关",
        "category": "云南菜",
        "image_url": "https://example.com/food1.jpg",
        "rating": 4.8,
        "price": 120,
        "description": "云南特色美食，不错的用餐体验",
        "recommendation": "三道茶、过桥米线、汽锅鸡",
        "business_hours": "10:00-22:00",
        "is_highlight": true,
        "day_index": 1
      },
      {
        "id": 302,
        "name": "成都·觉上的麻辣香锅",
        "address": "广东省清远市XX路XX号",
        "city": "清远",
        "category": "川菜",
        "image_url": "https://example.com/food2.jpg",
        "rating": 4.7,
        "price": 98,
        "description": "正宗川味麻辣香锅",
        "recommendation": "麻辣香锅、毛血旺、冰粉",
        "business_hours": "11:00-23:00",
        "is_highlight": true,
        "day_index": 3
      }
    ]
  }
}
```

#### 取消行程
```plain
POST /api/v1/trips/{tripId}/cancel
```

**请求参数**:

```json
{
  "confirm": true
}
```

**响应**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "status": 2,
    "cancel_time": "2023-05-10T15:30:00Z"
  }
}
```

