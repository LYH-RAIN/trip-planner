-- Create database
CREATE DATABASE IF NOT EXISTS trip_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database
USE trip_planner;

-- 1. Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    open_id VARCHAR(64) UNIQUE COMMENT 'WeChat OpenID',
    union_id VARCHAR(64) COMMENT 'WeChat UnionID',
    nickname VARCHAR(64) COMMENT 'User nickname',
    avatar_url VARCHAR(255) COMMENT 'Avatar URL',
    gender TINYINT COMMENT 'Gender: 0 Unknown, 1 Male, 2 Female',
    country VARCHAR(64) COMMENT 'Country',
    province VARCHAR(64) COMMENT 'Province',
    city VARCHAR(64) COMMENT 'City',
    phone VARCHAR(20) COMMENT 'Phone number',
    status TINYINT DEFAULT 1 COMMENT 'User status: 0 Disabled, 1 Normal',
    vip_level TINYINT DEFAULT 0 COMMENT 'VIP level: 0 Normal, 1 VIP, 2 SVIP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL COMMENT 'Last login time',
    INDEX idx_open_id (open_id),
    INDEX idx_union_id (union_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User information table';

-- 2. Trips table
CREATE TABLE IF NOT EXISTS trips (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'Creator User ID',
    title VARCHAR(128) NOT NULL COMMENT 'Trip title',
    description TEXT COMMENT 'Trip description',
    cover_image VARCHAR(255) COMMENT 'Cover image URL',
    departure_poi_id VARCHAR(64) COMMENT 'Departure POI ID',
    departure_name VARCHAR(255) COMMENT 'Departure location name',
    destinations JSON COMMENT 'Destination city/POI ID list JSON',
    start_datetime TIMESTAMP NOT NULL COMMENT 'Start time',
    end_datetime TIMESTAMP NOT NULL COMMENT 'End time',
    start_timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT 'Start timezone',
    end_timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT 'End timezone',
    days INT NOT NULL COMMENT 'Number of trip days',
    travel_mode TINYINT DEFAULT 1 COMMENT 'Transportation mode: 1 Driving, 2 Public transport',
    people_count INT DEFAULT 1 COMMENT 'Number of people',
    preferences JSON COMMENT 'Preferences list JSON',
    overview TEXT COMMENT 'Trip overview',
    budget DECIMAL(10,2) COMMENT 'Budget',
    estimated_cost DECIMAL(10,2) COMMENT 'Estimated cost',
    weather_info JSON COMMENT 'Weather information JSON',
    tags JSON COMMENT 'Tags list JSON',
    status TINYINT DEFAULT 0 COMMENT 'Status: 0 Planning, 1 Completed, 2 Cancelled, 3 In Progress',
    generation_status TINYINT DEFAULT 0 COMMENT 'Generation status: 0 Not generated, 1 Generating, 2 Success, 3 Failed',
    view_count INT DEFAULT 0 COMMENT 'View count',
    like_count INT DEFAULT 0 COMMENT 'Like count',
    share_count INT DEFAULT 0 COMMENT 'Share count',
    is_public TINYINT DEFAULT 0 COMMENT 'Is public: 0 Private, 1 Public',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_public (is_public, status),
    INDEX idx_start_datetime (start_datetime),
    INDEX idx_created_at (created_at),
    INDEX idx_departure_poi_id (departure_poi_id),
    INDEX idx_generation_status (generation_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trips table';

-- 3. Trip Days table
CREATE TABLE IF NOT EXISTS trip_days (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID',
    day_index INT NOT NULL COMMENT 'Day number (1-indexed)',
    date DATE NOT NULL COMMENT 'Specific date',
    datetime TIMESTAMP NOT NULL COMMENT 'Specific date and time (e.g., for day start)',
    timezone VARCHAR(64) DEFAULT 'Asia/Shanghai' COMMENT 'Timezone',
    title VARCHAR(128) COMMENT 'Day title',
    summary TEXT COMMENT 'Day summary',
    city VARCHAR(64) COMMENT 'City for the day',
    theme VARCHAR(128) COMMENT 'Day theme',
    weather_condition VARCHAR(32) COMMENT 'Weather condition code/short description',
    weather_condition_text TEXT COMMENT 'Weather condition narrative text',
    temperature VARCHAR(16) COMMENT 'Temperature range (e.g., 10-15°C)',
    weather_icon VARCHAR(32) COMMENT 'Weather icon code',
    humidity VARCHAR(16) COMMENT 'Humidity (e.g., 50%)',
    wind VARCHAR(32) COMMENT 'Wind information',
    precipitation VARCHAR(16) COMMENT 'Precipitation probability (e.g., 20%)',
    uv_index VARCHAR(16) COMMENT 'UV index',
    sunrise TIME COMMENT 'Sunrise time',
    sunset TIME COMMENT 'Sunset time',
    accommodation_poi_id VARCHAR(64) COMMENT 'Accommodation POI ID',
    accommodation_name VARCHAR(255) COMMENT 'Accommodation name',
    accommodation_address VARCHAR(255) COMMENT 'Accommodation address',
    accommodation_price DECIMAL(10,2) COMMENT 'Accommodation cost',
    accommodation_rating DECIMAL(2,1) COMMENT 'Accommodation rating',
    accommodation_latitude DECIMAL(10,6) COMMENT 'Accommodation latitude',
    accommodation_longitude DECIMAL(10,6) COMMENT 'Accommodation longitude',
    accommodation_contact VARCHAR(64) COMMENT 'Accommodation contact phone',
    start_point_poi_id VARCHAR(64) COMMENT 'Start point POI ID',
    start_point_name VARCHAR(255) COMMENT 'Start point name',
    start_point_time TIME COMMENT 'Start point time',
    start_point_type VARCHAR(32) COMMENT 'Start point type',
    end_point_poi_id VARCHAR(64) COMMENT 'End point POI ID',
    end_point_name VARCHAR(255) COMMENT 'End point name',
    end_point_time TIME COMMENT 'End point time',
    end_point_type VARCHAR(32) COMMENT 'End point type',
    estimated_cost DECIMAL(10,2) COMMENT 'Estimated cost for the day',
    is_generated TINYINT DEFAULT 0 COMMENT 'Detailed itinerary generated: 0 No, 1 Yes',
    place_count INT DEFAULT 0 COMMENT 'Number of places',
    food_count INT DEFAULT 0 COMMENT 'Number of food items',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    INDEX idx_trip_date (date),
    INDEX idx_is_generated (is_generated),
    UNIQUE KEY uk_trip_day (trip_id, day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip days table';

-- 4. Trip Places table
CREATE TABLE IF NOT EXISTS trip_places (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID',
    day_id BIGINT NOT NULL COMMENT 'Trip Day ID',
    day_index INT NOT NULL COMMENT 'Day number (1-indexed)',
    visit_order INT NOT NULL COMMENT 'Visit order for the day',
    name VARCHAR(128) NOT NULL COMMENT 'Place name',
    address VARCHAR(255) COMMENT 'Detailed address',
    city VARCHAR(64) COMMENT 'City where place is located',
    category VARCHAR(32) COMMENT 'Category (e.g., attraction, restaurant)',
    image_url VARCHAR(255) COMMENT 'Primary image URL',
    images JSON COMMENT 'Image list JSON',
    rating DECIMAL(2,1) COMMENT 'Rating',
    price DECIMAL(10,2) COMMENT 'Ticket price / Cost',
    start_time TIME COMMENT 'Start time / Opening time',
    end_time TIME COMMENT 'End time / Closing time',
    duration INT COMMENT 'Visit duration (minutes)',
    transportation VARCHAR(32) COMMENT 'Mode of transport to this place',
    transportation_details TEXT COMMENT 'Transportation details',
    distance DECIMAL(10,2) COMMENT 'Distance from previous place (km)',
    estimated_time INT COMMENT 'Estimated travel time (minutes)',
    latitude DECIMAL(10,6) COMMENT 'Latitude',
    longitude DECIMAL(10,6) COMMENT 'Longitude',
    amap_poi_id VARCHAR(64) COMMENT 'AMAP POI ID',
    amap_navigation_url VARCHAR(512) COMMENT 'AMAP navigation URL',
    web_navigation_url VARCHAR(512) COMMENT 'Web navigation URL',
    booking_required TINYINT DEFAULT 0 COMMENT 'Is booking required: 0 No, 1 Yes',
    booking_url VARCHAR(255) COMMENT 'Booking URL',
    contact VARCHAR(64) COMMENT 'Contact phone',
    notes TEXT COMMENT 'Notes',
    is_highlight TINYINT DEFAULT 0 COMMENT 'Is this a trip highlight: 0 No, 1 Yes',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index),
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_is_highlight (is_highlight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip places table';

-- 5. Trip Foods table
CREATE TABLE IF NOT EXISTS trip_foods (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID',
    day_id BIGINT COMMENT 'Trip Day ID',
    day_index INT COMMENT 'Day number (1-indexed)',
    visit_order INT COMMENT 'Visit order for the day',
    name VARCHAR(128) NOT NULL COMMENT 'Food/Restaurant name',
    address VARCHAR(255) COMMENT 'Detailed address',
    city VARCHAR(64) COMMENT 'City where food place is located',
    category VARCHAR(32) COMMENT 'Category (e.g., restaurant, snack)',
    image_url VARCHAR(255) COMMENT 'Primary image URL',
    images JSON COMMENT 'Image list JSON',
    rating DECIMAL(2,1) COMMENT 'Rating',
    price DECIMAL(10,2) COMMENT 'Price per person',
    start_time TIME COMMENT 'Meal time / Opening time',
    duration INT COMMENT 'Meal duration (minutes)',
    latitude DECIMAL(10,6) COMMENT 'Latitude',
    longitude DECIMAL(10,6) COMMENT 'Longitude',
    amap_poi_id VARCHAR(64) COMMENT 'AMAP POI ID',
    amap_navigation_url VARCHAR(512) COMMENT 'AMAP navigation URL',
    web_navigation_url VARCHAR(512) COMMENT 'Web navigation URL',
    contact VARCHAR(64) COMMENT 'Contact phone',
    description TEXT COMMENT 'Description',
    recommendation TEXT COMMENT 'Recommendation reason',
    business_hours VARCHAR(255) COMMENT 'Business hours',
    is_highlight TINYINT DEFAULT 0 COMMENT 'Is this a trip highlight: 0 No, 1 Yes',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE SET NULL,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day (trip_id, day_index),
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_is_highlight (is_highlight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip foods table';

-- 6. Trip Transportations table
CREATE TABLE IF NOT EXISTS trip_transportations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID',
    day_id BIGINT NOT NULL COMMENT 'Trip Day ID',
    day_index INT NOT NULL COMMENT 'Day number (1-indexed)',
    transport_order INT NOT NULL COMMENT 'Transportation order for the day',
    from_place_id BIGINT COMMENT 'Origin TripPlace ID',
    to_place_id BIGINT COMMENT 'Destination TripPlace ID',
    from_name VARCHAR(255) NOT NULL COMMENT 'Origin name',
    from_latitude DECIMAL(10,6) COMMENT 'Origin latitude',
    from_longitude DECIMAL(10,6) COMMENT 'Origin longitude',
    from_address VARCHAR(255) COMMENT 'Origin address',
    to_name VARCHAR(255) NOT NULL COMMENT 'Destination name',
    to_latitude DECIMAL(10,6) COMMENT 'Destination latitude',
    to_longitude DECIMAL(10,6) COMMENT 'Destination longitude',
    to_address VARCHAR(255) COMMENT 'Destination address',
    transportation_mode VARCHAR(32) NOT NULL COMMENT 'Transportation mode (e.g., driving, walking, bus)',
    distance DECIMAL(10,2) COMMENT 'Distance (km)',
    duration INT COMMENT 'Travel time (minutes)',
    price DECIMAL(10,2) COMMENT 'Transportation cost',
    start_time TIME COMMENT 'Departure time',
    end_time TIME COMMENT 'Arrival time',
    description TEXT COMMENT 'Description/Notes',
    booking_url VARCHAR(255) COMMENT 'Booking URL for tickets etc.',
    amap_navigation_url VARCHAR(512) COMMENT 'AMAP navigation URL',
    web_navigation_url VARCHAR(512) COMMENT 'Web navigation URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (day_id) REFERENCES trip_days(id) ON DELETE CASCADE,
    FOREIGN KEY (from_place_id) REFERENCES trip_places(id) ON DELETE SET NULL,
    FOREIGN KEY (to_place_id) REFERENCES trip_places(id) ON DELETE SET NULL,
    INDEX idx_trip_id (trip_id),
    INDEX idx_day_id (day_id),
    INDEX idx_trip_day_order (trip_id, day_index, transport_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip transportations table';

-- 7. Trip Shares table
CREATE TABLE IF NOT EXISTS trip_shares (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID',
    user_id BIGINT NOT NULL COMMENT 'User who owns the trip (sharer)',
    shared_with_user_id BIGINT COMMENT 'User with whom trip is shared (optional, if direct share)',
    share_token VARCHAR(64) UNIQUE COMMENT 'Unique token for sharing link',
    role VARCHAR(32) DEFAULT 'viewer' COMMENT 'Role of shared user (e.g., viewer, editor)',
    access_level TINYINT DEFAULT 1 COMMENT 'Access level: 1 View, 2 Edit',
    expires_at TIMESTAMP NULL COMMENT 'When the share link expires',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_trip_id (trip_id),
    INDEX idx_user_id (user_id),
    INDEX idx_shared_with_user_id (shared_with_user_id),
    INDEX idx_share_token (share_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip shares table';

-- 8. User Favorites table
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'User ID',
    trip_id BIGINT COMMENT 'Favorited Trip ID (if favorite is a trip)',
    place_id BIGINT COMMENT 'Favorited Place ID (maps to locations.id)',
    item_type VARCHAR(32) NOT NULL COMMENT 'Type of item favorited (e.g., trip, place)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_item (user_id, item_type, trip_id, place_id),
    INDEX idx_user_item (user_id, item_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User favorites table';

-- 9. Trip Reviews table
CREATE TABLE IF NOT EXISTS trip_reviews (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT NOT NULL COMMENT 'Trip ID being reviewed',
    user_id BIGINT NOT NULL COMMENT 'User ID who wrote the review',
    rating DECIMAL(2,1) NOT NULL COMMENT 'Rating (e.g., 1.0-5.0)',
    title VARCHAR(128) COMMENT 'Review title',
    comment TEXT COMMENT 'Review comment',
    images JSON COMMENT 'Images for review JSON',
    status TINYINT DEFAULT 1 COMMENT 'Review status: 0 Hidden, 1 Published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_trip_user (trip_id, user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Trip reviews table';

-- 10. AI Model Calls table
CREATE TABLE IF NOT EXISTS ai_model_calls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT COMMENT 'User ID who initiated the call',
    trip_id BIGINT COMMENT 'Associated Trip ID (if any)',
    model_name VARCHAR(64) NOT NULL COMMENT 'AI Model name used',
    prompt TEXT COMMENT 'Prompt sent to AI model',
    response TEXT COMMENT 'Response received from AI model',
    status VARCHAR(32) COMMENT 'Call status (e.g., success, failed, pending)',
    duration INT COMMENT 'Duration of the call in ms',
    cost DECIMAL(10,5) COMMENT 'Cost of the AI call',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_trip_id (trip_id),
    INDEX idx_model_name (model_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI model calls log table';

-- 11. Locations table (for caching POIs, etc.)
CREATE TABLE IF NOT EXISTS locations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    amap_poi_id VARCHAR(64) UNIQUE NOT NULL COMMENT 'AMAP POI ID or other unique external ID',
    name VARCHAR(255) NOT NULL COMMENT 'Location Name',
    address TEXT COMMENT 'Address',
    city_code VARCHAR(32) COMMENT 'City Code',
    city_name VARCHAR(64) COMMENT 'City Name',
    province_name VARCHAR(64) COMMENT 'Province Name',
    country_name VARCHAR(64) COMMENT 'Country Name',
    latitude DECIMAL(10,6) COMMENT 'Latitude',
    longitude DECIMAL(10,6) COMMENT 'Longitude',
    category_id BIGINT COMMENT 'Category ID from location_categories',
    category_name VARCHAR(64) COMMENT 'Category Name (denormalized)',
    tags JSON COMMENT 'Tags JSON array',
    rating DECIMAL(2,1) COMMENT 'Rating',
    price_level VARCHAR(16) COMMENT 'Price level (e.g., cheap, moderate, expensive)',
    phone_numbers VARCHAR(255) COMMENT 'Phone numbers (comma-separated or JSON)',
    website_url VARCHAR(255) COMMENT 'Website URL',
    images JSON COMMENT 'Images JSON array',
    business_hours TEXT COMMENT 'Business hours (text or JSON)',
    description TEXT COMMENT 'Description',
    source VARCHAR(32) DEFAULT 'amap' COMMENT 'Data source (e.g., amap, google, user)',
    raw_data JSON COMMENT 'Raw data from source JSON',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_name (name(191)),
    INDEX idx_city_name (city_name),
    INDEX idx_category_id (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Locations table (POI cache)';

-- 12. Location Categories table
CREATE TABLE IF NOT EXISTS location_categories (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL COMMENT 'Category Name (e.g., Restaurant, Attraction)',
    parent_id BIGINT COMMENT 'Parent Category ID (for subcategories)',
    icon_url VARCHAR(255) COMMENT 'Icon URL for category',
    description TEXT COMMENT 'Category description',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES location_categories(id) ON DELETE SET NULL,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Location categories table';

-- Add FK from locations to location_categories now that it's defined
ALTER TABLE locations
ADD CONSTRAINT fk_locations_category_id
FOREIGN KEY (category_id) REFERENCES location_categories(id) ON DELETE SET NULL;

-- 13. Location Search Logs table
CREATE TABLE IF NOT EXISTS location_search_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT COMMENT 'User ID who performed search',
    query TEXT NOT NULL COMMENT 'Search query',
    search_type VARCHAR(32) COMMENT 'Type of search (e.g., keyword, category)',
    filters JSON COMMENT 'Applied filters JSON',
    latitude DECIMAL(10,6) COMMENT 'Latitude of search center',
    longitude DECIMAL(10,6) COMMENT 'Longitude of search center',
    results_count INT COMMENT 'Number of results returned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_search_type (search_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Location search logs table';

-- 14. User Location History table
CREATE TABLE IF NOT EXISTS user_location_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'User ID',
    location_id BIGINT COMMENT 'Location ID from locations table (if specific POI)',
    amap_poi_id VARCHAR(64) COMMENT 'AMAP POI ID (if specific POI, denormalized or for external refs)',
    name VARCHAR(255) COMMENT 'Location name (can be custom or from locations table)',
    latitude DECIMAL(10,6) NOT NULL COMMENT 'Latitude',
    longitude DECIMAL(10,6) NOT NULL COMMENT 'Longitude',
    visit_type VARCHAR(32) COMMENT 'Type of visit (e.g., searched, viewed, added_to_trip)',
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp of visit/interaction',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_amap_poi_id (amap_poi_id),
    INDEX idx_visit_type (visit_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User location interaction history';

-- 15. Location Recommendations table
CREATE TABLE IF NOT EXISTS location_recommendations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'User for whom recommendation is made',
    location_id BIGINT NOT NULL COMMENT 'Recommended Location ID (from locations table)',
    amap_poi_id VARCHAR(64) COMMENT 'Recommended AMAP POI ID (denormalized)',
    recommendation_score DECIMAL(5,4) COMMENT 'Score of recommendation',
    reason TEXT COMMENT 'Reason for recommendation',
    source VARCHAR(64) COMMENT 'Source of recommendation (e.g., CF, content-based)',
    status VARCHAR(32) DEFAULT 'pending' COMMENT 'Status: pending, shown, clicked, dismissed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_user_status_score (user_id, status, recommendation_score DESC),
    INDEX idx_location_id (location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Location recommendations for users';

-- 插入测试用户数据
INSERT INTO users (
  open_id, union_id, nickname, avatar_url, gender, country, province, city, phone, status, vip_level, created_at, updated_at, last_login_at
) VALUES
('test_open_id_1', NULL, '张三', 'https://example.com/avatar1.jpg', 1, '中国', '广东省', '广州', NULL, 1, 0, NOW(), NOW(), NULL),
('test_open_id_2', NULL, '李四', 'https://example.com/avatar2.jpg', 2, '中国', '广东省', '深圳', NULL, 1, 1, NOW(), NOW(), NULL),
('test_open_id_3', NULL, '王五', 'https://example.com/avatar3.jpg', 1, '中国', '北京市', '北京', NULL, 1, 0, NOW(), NOW(), NULL);

-- 插入测试行程数据
INSERT INTO trips (
  user_id, title, description, cover_image, departure_poi_id, departure_name, destinations, start_datetime, end_datetime, start_timezone, end_timezone, days, travel_mode, people_count, preferences, overview, budget, estimated_cost, weather_info, tags, status, generation_status, view_count, like_count, share_count, is_public, created_at, updated_at
) VALUES
(1, '广东三日游', '探索广东的自然风光和美食文化', NULL, '广州', '广州', '["韶关", "肇庆"]', '2024-05-01 09:00:00', '2024-05-03 18:00:00', 'Asia/Shanghai', 'Asia/Shanghai', 3, 1, 2, '["自然风光", "摄影", "美食"]', '本次行程将游览丹霞山、南华寺等著名景点，品尝地道特色美食。', 2000.00, 1850.00, NULL, '["丹霞山", "南华寺"]', 1, 2, 0, 0, 0, 1, NOW(), NOW()),
(2, '北京文化深度游', '感受首都的历史文化底蕴', NULL, '深圳', '深圳', '["北京"]', '2024-06-01 08:00:00', '2024-06-04 20:00:00', 'Asia/Shanghai', 'Asia/Shanghai', 4, 2, 1, '["历史文化", "博物馆", "建筑"]', '北京行程包含故宫、长城、天安门等历史文化景点。', 3000.00, 2800.00, NULL, '["文化游", "历史游"]', 0, 2, 0, 0, 0, 0, NOW(), NOW());

-- 插入测试行程天数数据
INSERT INTO trip_days (
  trip_id, day_index, date, datetime, timezone, title, summary, city, theme, weather_condition, weather_condition_text, temperature, weather_icon, humidity, wind, precipitation, uv_index, sunrise, sunset, accommodation_poi_id, accommodation_name, accommodation_address, accommodation_price, accommodation_rating, accommodation_latitude, accommodation_longitude, accommodation_contact, start_point_poi_id, start_point_name, start_point_time, start_point_type, end_point_poi_id, end_point_name, end_point_time, end_point_type, estimated_cost, is_generated, place_count, food_count, created_at, updated_at
) VALUES
(1, 1, '2024-05-01', '2024-05-01 09:00:00', 'Asia/Shanghai', 'DAY1 - 韶关丹霞山', '游览丹霞山，欣赏南国奇观', '韶关', '自然风光', '晴', '晴朗', '25°-30°', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '韶关市丹霞山宾馆', '广东省韶关市仁化县丹霞山风景区', 380.00, 4.5, NULL, NULL, NULL, NULL, '广州火车站', '09:00:00', 'departure', NULL, '韶关丹霞山宾馆', '20:00:00', 'accommodation', 450.00, 1, 2, 1, NOW(), NOW()),
(1, 2, '2024-05-02', '2024-05-02 08:00:00', 'Asia/Shanghai', 'DAY2 - 南华寺祈福', '参观南华寺，体验禅宗文化', '韶关', '文化体验', '多云', '多云', '23°-28°', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '韶关市丹霞山宾馆', '广东省韶关市仁化县丹霞山风景区', 380.00, 4.5, NULL, NULL, NULL, NULL, '韶关丹霞山宾馆', '08:00:00', 'accommodation', NULL, '韶关丹霞山宾馆', '19:30:00', 'accommodation', 380.00, 1, 3, 2, NOW(), NOW());

-- 插入测试景点数据
INSERT INTO trip_places (
  trip_id, day_id, day_index, visit_order, name, address, city, category, image_url, images, rating, price, start_time, end_time, duration, transportation, transportation_details, distance, estimated_time, latitude, longitude, amap_poi_id, amap_navigation_url, web_navigation_url, booking_required, booking_url, contact, notes, is_highlight, created_at, updated_at
) VALUES
(1, 1, 1, 1, '南华寺', '广东省韶关市曲江区马坝镇', '韶关', '寺庙', 'https://example.com/nanhuasi.jpg', NULL, 4.8, 20.00, '10:00:00', '12:00:00', 120, NULL, NULL, NULL, NULL, 24.969615, 113.601624, 'B0FFG9KCPD', NULL, NULL, 0, NULL, '0751-6502013', NULL, 1, NOW(), NOW()),
(1, 1, 1, 2, '丹霞山', '广东省韶关市仁化县丹霞山风景区', '韶关', '自然景观', 'https://example.com/danxiashan.jpg', NULL, 4.9, 120.00, '14:00:00', '17:00:00', 180, NULL, NULL, NULL, NULL, 25.022758, 113.736513, 'B0FFHCF6VV', NULL, NULL, 0, NULL, '0751-6292721', NULL, 1, NOW(), NOW());

-- 插入测试美食数据
INSERT INTO trip_foods (
  trip_id, day_id, day_index, visit_order, name, address, city, category, image_url, images, rating, price, start_time, duration, latitude, longitude, amap_poi_id, amap_navigation_url, web_navigation_url, contact, description, recommendation, business_hours, is_highlight, created_at, updated_at
) VALUES
(1, 1, 1, 1, '韶关特色腊味馆', '广东省韶关市浈江区建设路123号', '韶关', '粤菜', 'https://example.com/food1.jpg', NULL, 4.6, 80.00, '12:30:00', 60, 24.801234, 113.591234, 'B0FFHCF6YY', NULL, NULL, '0751-8888888', NULL, '腊味拼盘、艇仔粥、牛杂', '10:00-22:00', 1, NOW(), NOW());

-- 插入测试地点数据
INSERT INTO locations (
  amap_poi_id, name, address, city_code, city_name, province_name, country_name, latitude, longitude, category_id, category_name, tags, rating, price_level, phone_numbers, website_url, images, business_hours, description, source, raw_data, created_at, updated_at
) VALUES
('B0FFHCF6VV', '丹霞山', '广东省韶关市仁化县丹霞山风景区', NULL, '韶关市', '广东省', '中国', 25.022758, 113.736513, NULL, '景点', '["世界自然遗产", "国家5A景区", "地貌奇观"]', 4.9, NULL, '0751-6292721', NULL, NULL, NULL, '丹霞山以独特的丹霞地貌著称，是世界自然遗产地。', 'amap', NULL, NOW(), NOW()),
('B0FFG9KCPD', '南华寺', '广东省韶关市曲江区马坝镇', NULL, '韶关市', '广东省', '中国', 24.969615, 113.601624, NULL, '景点', '["禅宗祖庭", "历史文化", "摄影胜地"]', 4.8, NULL, '0751-6502013', NULL, NULL, NULL, '南华寺是中国著名古刹之一，六祖慧能弘法圣地。', 'amap', NULL, NOW(), NOW());

-- 鍒涘缓澶栭敭绾︽潫
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

-- 鎻掑叆瀹屾垚鎻愮ず
SELECT '鏁版嵁搴撳垵濮嬪寲瀹屾垚锛?' as message;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?鐢ㄦ埛') as user_count FROM users;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?琛岀▼') as trip_count FROM trips;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?琛岀▼鏃ョ▼') as trip_day_count FROM trip_days;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?鏅?鐐?') as place_count FROM trip_places;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?缇庨??') as food_count FROM trip_foods;
SELECT CONCAT('鍒涘缓浜? ', COUNT(*), ' 涓?鍦扮偣') as location_count FROM locations;
