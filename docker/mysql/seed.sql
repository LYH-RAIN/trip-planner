-- 额外的测试数据
USE trip_planner;

-- 插入更多用户
INSERT INTO users (open_id, nickname, avatar_url, gender, country, province, city, status, vip_level) VALUES
('test_open_id_4', '赵六', 'https://example.com/avatar4.jpg', 2, '中国', '上海市', '上海市', 1, 2),
('test_open_id_5', '孙七', 'https://example.com/avatar5.jpg', 1, '中国', '浙江省', '杭州市', 1, 0);

-- 插入更多行程
INSERT INTO trips (user_id, title, description, start_datetime, end_datetime, days, departure, destinations, travel_mode, people_count, preferences, overview, budget, estimated_cost, tags, status, is_public) VALUES
(3, '上海都市风情游', '体验魔都的现代化魅力', '2024-07-01 10:00:00', '2024-07-03 22:00:00', 3, '北京', '["上海"]', 2, 2, '["都市风光", "购物", "夜景"]', '游览外滩、东方明珠、南京路等标志性景点。', 2500.00, 2300.00, '["都市游", "购物游"]', 1, 1),
(4, '杭州西湖诗意之旅', '感受江南水乡的诗情画意', '2024-08-01 09:00:00', '2024-08-02 18:00:00', 2, '上海', '["杭州"]', 1, 1, '["自然风光", "历史文化", "摄影"]', '漫步西湖，游览雷峰塔、断桥等经典景点。', 1200.00, 1100.00, '["周末游", "文艺游"]', 0, 0);

-- 插入收藏数据
INSERT INTO user_favorites (user_id, trip_id) VALUES
(2, 1),
(3, 1),
(1, 3);

-- 插入评价数据
INSERT INTO trip_reviews (trip_id, user_id, rating, content) VALUES
(1, 2, 5, '行程安排很棒，丹霞山的风景真的很美！'),
(1, 3, 4, '总体不错，就是时间有点紧张。'),
(3, 1, 5, '上海的夜景太美了，推荐！');

-- 插入分享数据
INSERT INTO trip_shares (trip_id, user_id, share_type, share_code, view_count) VALUES
(1, 1, 3, 'ABC123', 25),
(3, 3, 1, 'DEF456', 12);
