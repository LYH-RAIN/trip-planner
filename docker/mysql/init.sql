-- 创建数据库
CREATE DATABASE IF NOT EXISTS trip_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE trip_planner;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
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
    status TINYINT DEFAULT 1 COMMENT '用户状态：0禁用，1正常',
    vip_level TINYINT DEFAULT 0 COMMENT 'VIP等级：0普通，1VIP，2SVIP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    INDEX idx_open_id (open_id),
    INDEX idx_union_id (union_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 2. 行程表
CREATE TABLE IF NOT EXISTS trips (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '创建用户ID',
    title VARCHAR(128) NOT NULL COMMENT '行程标题',
    description TEXT COMMENT '行程描述',
    cover_image VARCHAR(255) COMMENT '封面图片',
    start_datetime TIMESTAMP NOT NULL COMMENT '开始时间',
    end_datetime TIMESTAMP NOT NULL COMMENT '结束时间',
    start_timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT '开始时区',
    end_timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT '结束时区',
    days INT NOT NULL COMMENT '行程天数',
    departure VARCHAR(64) NOT NULL COMMENT '出发地',
    destinations JSON COMMENT '目的地城市列表',
    travel_mode TINYINT DEFAULT 1 COMMENT '交通方式：1自驾，2公共交通',
    people_count INT DEFAULT 1 COMMENT '出行人数',
    preferences JSON COMMENT '偏好列表',
    overview TEXT COMMENT '行程总览',
    budget DECIMAL(10,2) COMMENT '预算',
    estimated_cost DECIMAL(10,2) COMMENT '预估费用',
    weather_info TEXT COMMENT '天气信息JSON',
    tags JSON COMMENT '标签列表',
    status TINYINT DEFAULT 0 COMMENT '状态：0规划中，1已完成，2已取消',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    like_count INT DEFAULT 0 COMMENT '点赞次数',
    share_count INT DEFAULT 0 COMMENT '分享次数',
    is_public TINYINT DEFAULT 0 COMMENT '是否公开：0私密，1公开',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_public (is_public, status),
    INDEX idx_start_datetime (start_datetime),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程表';

-- 3. 行程日程表
CREATE TABLE IF NOT EXISTS trip_days (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_index INT NOT NULL COMMENT '第几天',
    date DATE NOT NULL COMMENT '具体日期',
    datetime TIMESTAMP NOT NULL COMMENT '具体日期时间',
    timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT '时区',
    title VARCHAR(128) COMMENT '当天标题',
    summary TEXT COMMENT '当天概述',
    city VARCHAR(64) COMMENT '当天所在城市',
    theme VARCHAR(128) COMMENT '当天主题',
    weather_condition VARCHAR(32) COMMENT '天气状况',
    temperature VARCHAR(16) COMMENT '温度范围',
    weather_icon VARCHAR(32) COMMENT '天气图标',
    humidity VARCHAR(16) COMMENT '湿度',
    wind VARCHAR(32) COMMENT '风力',
    precipitation VARCHAR(16) COMMENT '降水概率',
    uv_index VARCHAR(16) COMMENT '紫外线指数',
    sunrise TIME COMMENT '日出时间',
    sunset TIME COMMENT '日落时间',
    accommodation_name VARCHAR(255) COMMENT '住宿名称',
    accommodation_address VARCHAR(255) COMMENT '住宿地址',
    accommodation_price DECIMAL(10,2) COMMENT '住宿费用',
    accommodation_rating DECIMAL(2,1) COMMENT '住宿评分',
    accommodation_latitude DECIMAL(10,6) COMMENT '住宿纬度',
    accommodation_longitude DECIMAL(10,6) COMMENT '住宿经度',
    accommodation_contact VARCHAR(64) COMMENT '住宿联系电话',
    start_point_name VARCHAR(255) COMMENT '起点名称',
    start_point_time TIME COMMENT '起点时间',
    start_point_type VARCHAR(32) COMMENT '起点类型',
    end_point_name VARCHAR(255) COMMENT '终点名称',
    end_point_time TIME COMMENT '终点时间',
    end_point_type VARCHAR(32) COMMENT '终点类型',
    estimated_cost DECIMAL(10,2) COMMENT '当日预估费用',
    is_generated TINYINT DEFAULT 0 COMMENT '是否已生成详细行程：0否，1是',
    place_count INT DEFAULT 0 COMMENT '景点数量',
    food_count INT DEFAULT 0 COMMENT '美食数量',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    UNIQUE KEY uk_trip_day (trip_id, day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程日程表';

-- 4. 行程景点表
CREATE TABLE IF NOT EXISTS trip_places (
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
    images JSON COMMENT '图片列表',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '门票价格',
    start_time TIME COMMENT '开始时间',
    end_time TIME COMMENT '结束时间',
    duration INT COMMENT '游玩时长(分钟)',
    transportation VARCHAR(32) COMMENT '交通方式',
    transportation_details TEXT COMMENT '交通详情',
    distance DECIMAL(10,2) COMMENT '与上一地点距离(km)',
    estimated_time INT COMMENT '预计交通时间(分钟)',
    latitude DECIMAL(10,6) COMMENT '纬度',
    longitude DECIMAL(10,6) COMMENT '经度',
    amap_poi_id VARCHAR(64) COMMENT '高德POI ID',
    amap_navigation_url VARCHAR(512) COMMENT '高德导航链接',
    web_navigation_url VARCHAR(512) COMMENT '网页导航链接',
    booking_required TINYINT DEFAULT 0 COMMENT '是否需要预订',
    booking_url VARCHAR(255) COMMENT '预订链接',
    contact VARCHAR(64) COMMENT '联系电话',
    notes TEXT COMMENT '备注',
    is_highlight TINYINT DEFAULT 0 COMMENT '是否为行程亮点：0否，1是',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index),
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_is_highlight (is_highlight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程景点表';

-- 5. 行程美食表
CREATE TABLE IF NOT EXISTS trip_foods (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_id BIGINT COMMENT '行程日程ID',
    day_index INT COMMENT '第几天',
    visit_order INT COMMENT '当天访问顺序',
    name VARCHAR(128) NOT NULL COMMENT '美食名称',
    address VARCHAR(255) COMMENT '详细地址',
    city VARCHAR(64) COMMENT '所在城市',
    category VARCHAR(32) COMMENT '分类',
    image_url VARCHAR(255) COMMENT '图片URL',
    images JSON COMMENT '图片列表',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '人均价格',
    start_time TIME COMMENT '用餐时间',
    duration INT COMMENT '用餐时长(分钟)',
    latitude DECIMAL(10,6) COMMENT '纬度',
    longitude DECIMAL(10,6) COMMENT '经度',
    amap_poi_id VARCHAR(64) COMMENT '高德POI ID',
    amap_navigation_url VARCHAR(512) COMMENT '高德导航链接',
    web_navigation_url VARCHAR(512) COMMENT '网页导航链接',
    contact VARCHAR(64) COMMENT '联系电话',
    description TEXT COMMENT '描述',
    recommendation TEXT COMMENT '推荐理由',
    business_hours VARCHAR(255) COMMENT '营业时间',
    is_highlight TINYINT DEFAULT 0 COMMENT '是否为行程亮点：0否，1是',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index),
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_is_highlight (is_highlight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程美食表';

-- 6. 行程交通表
CREATE TABLE IF NOT EXISTS trip_transportations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    day_id BIGINT NOT NULL COMMENT '行程日程ID',
    day_index INT NOT NULL COMMENT '第几天',
    transport_order INT NOT NULL COMMENT '当天交通顺序',
    from_name VARCHAR(255) NOT NULL COMMENT '起点名称',
    from_latitude DECIMAL(10,6) COMMENT '起点纬度',
    from_longitude DECIMAL(10,6) COMMENT '起点经度',
    to_name VARCHAR(255) NOT NULL COMMENT '终点名称',
    to_latitude DECIMAL(10,6) COMMENT '终点纬度',
    to_longitude DECIMAL(10,6) COMMENT '终点经度',
    start_time TIME COMMENT '出发时间',
    duration INT COMMENT '交通时长(分钟)',
    distance DECIMAL(10,2) COMMENT '距离(km)',
    transportation_mode VARCHAR(32) COMMENT '交通方式',
    description TEXT COMMENT '交通描述',
    amap_navigation_url VARCHAR(512) COMMENT '高德导航链接',
    web_navigation_url VARCHAR(512) COMMENT '网页导航链接',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程交通表';

-- 7. 行程分享表
CREATE TABLE IF NOT EXISTS trip_shares (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    user_id BIGINT NOT NULL COMMENT '分享用户ID',
    share_type TINYINT NOT NULL COMMENT '分享类型：1微信，2朋友圈，3链接，4二维码',
    share_url VARCHAR(255) COMMENT '分享链接',
    share_code VARCHAR(32) COMMENT '分享码',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    expires_at TIMESTAMP COMMENT '过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_user_id (user_id),
    INDEX idx_share_code (share_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程分享表';

-- 8. 用户收藏表
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_trip (user_id, trip_id),
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';

-- 9. 行程评价表
CREATE TABLE IF NOT EXISTS trip_reviews (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    user_id BIGINT NOT NULL COMMENT '评价用户ID',
    rating TINYINT NOT NULL COMMENT '评分1-5',
    content TEXT COMMENT '评价内容',
    images JSON COMMENT '评价图片列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_id (trip_id),
    INDEX idx_user_id (user_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行程评价表';

-- 10. AI模型调用记录表
CREATE TABLE IF NOT EXISTS ai_model_calls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    trip_id BIGINT COMMENT '关联行程ID',
    prompt TEXT NOT NULL COMMENT '输入提示词',
    response TEXT COMMENT 'AI返回结果',
    model_name VARCHAR(64) COMMENT '模型名称',
    call_type VARCHAR(32) COMMENT '调用类型：trip_generate, trip_update, etc',
    status TINYINT DEFAULT 0 COMMENT '状态：0处理中，1成功，2失败',
    error_message VARCHAR(255) COMMENT '错误信息',
    tokens_used INT COMMENT '使用的token数量',
    cost DECIMAL(10,4) COMMENT '调用费用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id),
    INDEX idx_call_type (call_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI模型调用记录表';

-- 11. 地点信息表
CREATE TABLE IF NOT EXISTS locations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    amap_poi_id VARCHAR(64) UNIQUE NOT NULL COMMENT '高德POI ID',
    name VARCHAR(128) NOT NULL COMMENT '地点名称',
    type VARCHAR(32) COMMENT '地点类型',
    type_code VARCHAR(16) COMMENT '类型代码',
    address VARCHAR(255) COMMENT '详细地址',
    latitude DECIMAL(10,6) COMMENT '纬度',
    longitude DECIMAL(10,6) COMMENT '经度',
    district VARCHAR(64) COMMENT '区县',
    city VARCHAR(64) COMMENT '城市',
    province VARCHAR(64) COMMENT '省份',
    tel VARCHAR(64) COMMENT '联系电话',
    website VARCHAR(255) COMMENT '官网',
    business_hours VARCHAR(255) COMMENT '营业时间',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '价格',
    images JSON COMMENT '图片列表',
    tags JSON COMMENT '标签列表',
    description TEXT COMMENT '描述',
    introduction TEXT COMMENT '详细介绍',
    transportation TEXT COMMENT '交通信息',
    tips TEXT COMMENT '游玩提示',
    view_count INT DEFAULT 0 COMMENT '查看次数',
    search_count INT DEFAULT 0 COMMENT '搜索次数',
    data_source VARCHAR(32) DEFAULT 'amap' COMMENT '数据来源',
    last_sync_at TIMESTAMP COMMENT '最后同步时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_name (name),
    INDEX idx_city_type (city, type),
    INDEX idx_location (latitude, longitude),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地点信息表';

-- 插入测试用户数据
INSERT INTO users (open_id, nickname, avatar_url, gender, country, province, city, status, vip_level) VALUES
('test_open_id_1', '张三', 'https://example.com/avatar1.jpg', 1, '中国', '广东省', '广州市', 1, 0),
('test_open_id_2', '李四', 'https://example.com/avatar2.jpg', 2, '中国', '广东省', '深圳市', 1, 1),
('test_open_id_3', '王五', 'https://example.com/avatar3.jpg', 1, '中国', '北京市', '北京市', 1, 0);

-- 插入测试行程数据
INSERT INTO trips (user_id, title, description, start_datetime, end_datetime, days, departure, destinations, travel_mode, people_count, preferences, overview, budget, estimated_cost, tags, status, is_public) VALUES
(1, '广东三日游', '探索广东的自然风光和美食文化', '2024-05-01 09:00:00', '2024-05-03 18:00:00', 3, '广州', '["韶关", "清远"]', 1, 2, '["自然风光", "摄影", "美食"]', '本次行程将游览丹霞山、南华寺等著名景点，品尝当地特色美食。', 2000.00, 1850.00, '["周末游", "亲子游"]', 1, 1),
(2, '北京文化之旅', '感受首都的历史文化底蕴', '2024-06-01 08:00:00', '2024-06-04 20:00:00', 4, '深圳', '["北京"]', 2, 1, '["历史文化", "博物馆", "古建筑"]', '深度游览故宫、长城、天坛等历史文化景点。', 3000.00, 2800.00, '["文化游", "历史游"]', 0, 0);

-- 插入测试行程日程数据
INSERT INTO trip_days (trip_id, day_index, date, datetime, title, summary, city, theme, weather_condition, temperature, accommodation_name, accommodation_address, accommodation_price, accommodation_rating, start_point_name, start_point_time, start_point_type, end_point_name, end_point_time, end_point_type, estimated_cost, is_generated, place_count, food_count) VALUES
(1, 1, '2024-05-01', '2024-05-01 09:00:00', 'DAY1 - 抵达韶关', '抵达韶关，游览南华寺', '韶关', '历史文化探索', '晴', '25°-30°', '韶关丹霞山酒店', '广东省韶关市仁化县丹霞山镇', 380.00, 4.5, '广州白云国际机场', '09:00:00', 'departure', '韶关丹霞山酒店', '20:00:00', 'accommodation', 450.00, 1, 2, 1),
(1, 2, '2024-05-02', '2024-05-02 08:00:00', 'DAY2 - 丹霞山深度游', '深度游览丹霞山风景区', '韶关', '自然风光体验', '多云', '23°-28°', '韶关丹霞山酒店', '广东省韶关市仁化县丹霞山镇', 380.00, 4.5, '韶关丹霞山酒店', '08:00:00', 'accommodation', '韶关丹霞山酒店', '19:30:00', 'accommodation', 380.00, 1, 3, 2),
(1, 3, '2024-05-03', '2024-05-03 09:00:00', 'DAY3 - 返程', '清远一日游后返程', '清远', '休闲放松', '晴', '26°-31°', '', '', 0, 0, '韶关丹霞山酒店', '09:00:00', 'accommodation', '广州白云国际机场', '18:00:00', 'departure', 320.00, 1, 1, 1);

-- 插入测试景点数据
INSERT INTO trip_places (trip_id, day_id, day_index, visit_order, name, address, city, category, image_url, rating, price, start_time, end_time, duration, latitude, longitude, amap_poi_id, contact, is_highlight) VALUES
(1, 1, 1, 1, '南华寺', '广东省韶关市曲江区马坝镇', '韶关', '寺庙', 'https://example.com/nanhuasi.jpg', 4.8, 20.00, '10:00:00', '12:00:00', 120, 24.969615, 113.601624, 'B0FFG9KCPD', '0751-6502013', 1),
(1, 1, 1, 2, '丹霞山', '广东省韶关市仁化县丹霞山镇', '韶关', '自然景观', 'https://example.com/danxiashan.jpg', 4.9, 120.00, '14:00:00', '17:00:00', 180, 25.022758, 113.736513, 'B0FFHCF6VV', '0751-6292721', 1),
(1, 2, 2, 1, '阳元石', '广东省韶关市仁化县丹霞山风景区内', '韶关', '自然景观', 'https://example.com/yangyuanshi.jpg', 4.7, 0, '09:00:00', '10:30:00', 90, 25.025000, 113.740000, 'B0FFHCF6XX', '', 1);

-- 插入测试美食数据
INSERT INTO trip_foods (trip_id, day_id, day_index, visit_order, name, address, city, category, image_url, rating, price, start_time, duration, latitude, longitude, amap_poi_id, contact, recommendation, business_hours, is_highlight) VALUES
(1, 1, 1, 1, '韶关特色餐厅', '广东省韶关市武江区建国路123号', '韶关', '粤菜', 'https://example.com/food1.jpg', 4.6, 80.00, '12:30:00', 60, 24.801234, 113.591234, 'B0FFHCF6YY', '0751-8888888', '白切鸡、炒河粉、老火汤', '10:00-22:00', 1),
(1, 2, 2, 1, '丹霞山农家乐', '广东省韶关市仁化县丹霞山镇景区附近', '韶关', '农家菜', 'https://example.com/food2.jpg', 4.4, 60.00, '12:00:00', 60, 25.020000, 113.735000, 'B0FFHCF6ZZ', '0751-6292888', '土鸡煲、野菜、山泉水豆腐', '09:00-21:00', 0);

-- 插入测试地点数据
INSERT INTO locations (amap_poi_id, name, type, type_code, address, latitude, longitude, district, city, province, tel, rating, price, tags, description, data_source) VALUES
('B0FFHCF6VV', '丹霞山', '景点', '110202', '广东省韶关市仁化县丹霞山镇', 25.022758, 113.736513, '仁化县', '韶关市', '广东省', '0751-6292721', 4.9, 120.00, '["世界自然遗产", "国家5A级景区", "地质公园"]', '丹霞山以赤壁丹崖为特色，是世界自然遗产，以奇特的红砂岩地貌著称。', 'amap'),
('B0FFG9KCPD', '南华寺', '景点', '110202', '广东省韶关市曲江区马坝镇', 24.969615, 113.601624, '曲江区', '韶关市', '广东省', '0751-6502013', 4.8, 20.00, '["佛教寺庙", "历史文化", "六祖慧能"]', '南华寺是中国佛教名寺之一，六祖慧能弘扬南宗禅法的发源地。', 'amap');

-- 创建外键约束
ALTER TABLE trips ADD CONSTRAINT fk_trips_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE trip_days ADD CONSTRAINT fk_trip_days_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_places ADD CONSTRAINT fk_trip_places_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_places ADD CONSTRAINT fk_trip_places_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE;
ALTER TABLE trip_foods ADD CONSTRAINT fk_trip_foods_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_foods ADD CONSTRAINT fk_trip_foods_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE;
ALTER TABLE trip_transportations ADD CONSTRAINT fk_trip_transportations_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_transportations ADD CONSTRAINT fk_trip_transportations_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE;
ALTER TABLE trip_shares ADD CONSTRAINT fk_trip_shares_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_shares ADD CONSTRAINT fk_trip_shares_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_favorites ADD CONSTRAINT fk_user_favorites_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_favorites ADD CONSTRAINT fk_user_favorites_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_reviews ADD CONSTRAINT fk_trip_reviews_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;
ALTER TABLE trip_reviews ADD CONSTRAINT fk_trip_reviews_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE ai_model_calls ADD CONSTRAINT fk_ai_model_calls_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE ai_model_calls ADD CONSTRAINT fk_ai_model_calls_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL;

-- 插入完成提示
SELECT '数据库初始化完成！' as message;
SELECT CONCAT('创建了 ', COUNT(*), ' 个用户') as user_count FROM users;
SELECT CONCAT('创建了 ', COUNT(*), ' 个行程') as trip_count FROM trips;
SELECT CONCAT('创建了 ', COUNT(*), ' 个行程日程') as trip_day_count FROM trip_days;
SELECT CONCAT('创建了 ', COUNT(*), ' 个景点') as place_count FROM trip_places;
SELECT CONCAT('创建了 ', COUNT(*), ' 个美食') as food_count FROM trip_foods;
SELECT CONCAT('创建了 ', COUNT(*), ' 个地点') as location_count FROM locations;
