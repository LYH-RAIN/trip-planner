#!/bin/bash

# 检查 Docker 和 Docker Compose 是否安装
if ! command -v docker &> /dev/null; then
    echo "Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建必要的目录
mkdir -p logs
mkdir -p static

# 检查环境变量文件是否存在
if [ ! -f .env ]; then
    echo "未找到 .env 文件，将使用默认配置"
    cat > .env << EOF
# MySQL 配置
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=trip_planner
MYSQL_USER=trip_user
MYSQL_PASSWORD=trip_password
MYSQL_PORT=3306

# Nginx 配置
NGINX_PORT=80

# 应用配置
FLASK_ENV=production
SECRET_KEY=default_secret_key
JWT_SECRET_KEY=default_jwt_secret_key
AMAP_KEY=your_amap_key
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
EOF
    echo "已创建默认 .env 文件，请根据需要修改"
fi

# 启动服务
echo "启动行程规划系统..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

echo "行程规划系统已启动！"
echo "API 访问地址: http://localhost:${NGINX_PORT:-80}/api"
echo "查看日志: docker-compose logs -f"
