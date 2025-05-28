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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    INDEX idx_open_id (open_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 行程表
CREATE TABLE IF NOT EXISTS trips (
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

-- 行程日程表
CREATE TABLE IF NOT EXISTS trip_days (
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

-- 行程美食表
CREATE TABLE IF NOT EXISTS trip_foods (
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id)
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

ALTER TABLE ai_model_calls
ADD CONSTRAINT fk_ai_model_calls_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
ADD CONSTRAINT fk_ai_model_calls_trip_id FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL;
