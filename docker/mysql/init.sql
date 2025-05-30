-- 创建数据库
CREATE DATABASE IF NOT EXISTS trip_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE trip_planner;

-- 用户表
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

-- 行程表
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
    actual_cost DECIMAL(10,2) COMMENT '实际花费',
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

-- 行程日程表
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

-- 行程景点表
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
    image_url VARCHAR(255) COMMENT '主图片URL',
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

-- 行程美食表
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
    image_url VARCHAR(255) COMMENT '主图片URL',
    images JSON COMMENT '图片列表',
    rating DECIMAL(2,1) COMMENT '评分',
    price DECIMAL(10,2) COMMENT '人均价格',
    start_time TIME COMMENT '用餐时间',
    end_time TIME COMMENT '结束时间',
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

-- 行程交通表
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

-- 行程分享表
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

-- 用户收藏表
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    trip_id BIGINT NOT NULL COMMENT '行程ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_trip (user_id, trip_id),
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';

-- 行程评价表
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

-- AI模型调用记录表
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

-- 添加外键约束
ALTER TABLE trips
ADD CONSTRAINT fk_trips_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE trip_days
ADD CONSTRAINT fk_trip_days_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;

ALTER TABLE trip_places
ADD CONSTRAINT fk_trip_places_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_trip_places_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE;

ALTER TABLE trip_foods
ADD CONSTRAINT fk_trip_foods_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_trip_foods_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE SET NULL;

ALTER TABLE trip_transportations
ADD CONSTRAINT fk_trip_transportations_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_trip_transportations_day_id FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE;

ALTER TABLE trip_shares
ADD CONSTRAINT fk_trip_shares_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_trip_shares_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE user_favorites
ADD CONSTRAINT fk_user_favorites_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_user_favorites_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE;

ALTER TABLE trip_reviews
ADD CONSTRAINT fk_trip_reviews_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_trip_reviews_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE ai_model_calls
ADD CONSTRAINT fk_ai_model_calls_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_ai_model_calls_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL;

-- 创建复合索引优化查询性能
CREATE INDEX idx_trips_composite ON trips(user_id, status, start_datetime);
CREATE INDEX idx_trip_places_composite ON trip_places(trip_id, day_index, visit_order);
CREATE INDEX idx_trip_foods_composite ON trip_foods(trip_id, day_index, visit_order);
CREATE INDEX idx_trip_transportations_composite ON trip_transportations(trip_id, day_index, transport_order);
CREATE INDEX idx_trip_foods_city_rating ON trip_foods(city, rating DESC);

-- 创建视图：行程统计信息
CREATE VIEW v_trip_stats AS
SELECT
    t.id,
    t.title,
    t.user_id,
    t.status,
    COUNT(DISTINCT tp.id) as place_count,
    COUNT(DISTINCT tf.id) as food_count,
    COUNT(DISTINCT tt.id) as transportation_count,
    COUNT(DISTINCT uf.user_id) as favorite_count,
    AVG(tr.rating) as avg_rating,
    COUNT(DISTINCT tr.id) as review_count,
    SUM(CASE WHEN tp.is_highlight = 1 THEN 1 ELSE 0 END) as highlight_place_count,
    SUM(CASE WHEN tf.is_highlight = 1 THEN 1 ELSE 0 END) as highlight_food_count
FROM trips t
LEFT JOIN trip_places tp ON t.id = tp.trip_id
LEFT JOIN trip_foods tf ON t.id = tf.trip_id
LEFT JOIN trip_transportations tt ON t.id = tt.trip_id
LEFT JOIN user_favorites uf ON t.id = uf.trip_id
LEFT JOIN trip_reviews tr ON t.id = tr.trip_id
GROUP BY t.id;

-- 创建视图：每日行程概览
CREATE VIEW v_trip_day_overview AS
SELECT
    td.id,
    td.trip_id,
    td.day_index,
    td.date,
    td.city,
    td.theme,
    td.estimated_cost,
    COUNT(DISTINCT tp.id) as place_count,
    COUNT(DISTINCT tf.id) as food_count,
    COUNT(DISTINCT tt.id) as transportation_count,
    GROUP_CONCAT(DISTINCT tp.name ORDER BY tp.visit_order SEPARATOR ', ') as main_attractions,
    SUM(CASE WHEN tp.is_highlight = 1 THEN 1 ELSE 0 END) as highlight_count
FROM trip_days td
LEFT JOIN trip_places tp ON td.id = tp.day_id
LEFT JOIN trip_foods tf ON td.id = tf.day_id
LEFT JOIN trip_transportations tt ON td.id = tt.day_id
GROUP BY td.id;

-- 插入测试数据（可选）
INSERT INTO users (open_id, nickname, avatar_url, gender, city) VALUES
('test_open_id_1', '测试用户1', 'https://example.com/avatar1.jpg', 1, '广州'),
('test_open_id_2', '测试用户2', 'https://example.com/avatar2.jpg', 2, '深圳');

-- 插入测试行程数据
INSERT INTO trips (user_id, title, description, start_datetime, end_datetime, days, departure, destinations, preferences, tags, budget) VALUES
(1, '广东四日游', '探索广东的自然风光和美食文化', '2023-05-07 01:00:00', '2023-05-10 10:00:00', 4, '广州', '["韶关", "清远"]', '["自然风光", "摄影", "美食"]', '["周末游", "亲子游"]', 2000.00);

-- 插入测试日程数据
INSERT INTO trip_days (trip_id, day_index, date, datetime, title, city, theme, estimated_cost) VALUES
(1, 1, '2023-05-07', '2023-05-07 01:00:00', 'DAY1 - 抵达韶关', '韶关', '历史文化探索', 450.00),
(1, 2, '2023-05-08', '2023-05-08 01:00:00', 'DAY2 - 丹霞山深度游', '韶关', '自然风光体验', 380.00),
(1, 3, '2023-05-09', '2023-05-09 01:00:00', 'DAY3 - 前往清远', '清远', '山水风光', 420.00),
(1, 4, '2023-05-10', '2023-05-10 01:00:00', 'DAY4 - 返程广州', '广州', '购物美食', 300.00);

-- 插入测试景点数据
INSERT INTO trip_places (trip_id, day_id, day_index, visit_order, name, address, city, category, rating, price, start_time, end_time, duration, latitude, longitude, amap_poi_id, is_highlight) VALUES
(1, 1, 1, 1, '南华寺', '广东省韶关市曲江区马坝镇', '韶关', '景点', 4.8, 20.00, '09:00:00', '11:00:00', 120, 24.969615, 113.601624, 'B0FFG9KCPD', 1),
(1, 1, 1, 2, '丹霞山', '广东省韶关市仁化县丹霞山镇', '韶关', '景点', 4.9, 120.00, '14:00:00', '17:00:00', 180, 25.022758, 113.736513, 'B0FFHCF6VV', 1);

-- 插入测试美食数据
INSERT INTO trip_foods (trip_id, day_id, day_index, visit_order, name, address, city, category, rating, price, start_time, duration, latitude, longitude, amap_poi_id, is_highlight) VALUES
(1, 1, 1, 3, '韶关特色餐厅', '广东省韶关市XX路XX号', '韶关', '粤菜', 4.7, 80.00, '12:00:00', 60, 24.801234, 113.591234, 'B0FFHCF6XX', 1);

-- 插入测试交通数据
INSERT INTO trip_transportations (trip_id, day_id, day_index, transport_order, from_name, to_name, start_time, duration, distance, transportation_mode, description) VALUES
(1, 1, 1, 1, '广州白云国际机场', '南华寺', '08:00:00', 120, 85.5, '自驾', '从机场出发前往南华寺'),
(1, 1, 1, 2, '南华寺', '韶关特色餐厅', '11:00:00', 30, 15.2, '自驾', '前往午餐地点'),
(1, 1, 1, 3, '韶关特色餐厅', '丹霞山', '13:30:00', 30, 20.8, '自驾', '前往丹霞山景区');
