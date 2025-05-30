#!/bin/bash

# 开发环境启动脚本
set -e

echo "🚀 启动开发环境..."

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，从示例文件复制..."
    cp .env.example .env
    echo "📝 请编辑 .env 文件配置必要的环境变量"
fi

# 创建必要的目录
mkdir -p logs

# 启动开发环境
echo "🐳 启动开发环境容器..."
docker-compose -f docker-compose.dev.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.dev.yml ps

echo "✅ 开发环境启动完成！"
echo "🌐 API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "🗄️  数据库管理: http://localhost:8080"
echo "🔧 Redis管理: http://localhost:8081"
