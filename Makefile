.PHONY: help build up down restart logs shell test lint format clean

# 默认目标
help:
	@echo "Trip Planner 项目管理命令:"
	@echo "  build     - 构建Docker镜像"
	@echo "  up        - 启动所有服务"
	@echo "  up-dev    - 启动开发环境"
	@echo "  down      - 停止所有服务"
	@echo "  restart   - 重启所有服务"
	@echo "  logs      - 查看日志"
	@echo "  shell     - 进入应用容器"
	@echo "  test      - 运行测试"
	@echo "  lint      - 代码检查"
	@echo "  format    - 代码格式化"
	@echo "  clean     - 清理Docker资源"
	@echo "  migrate   - 运行数据库迁移"
	@echo "  tools     - 启动管理工具"

# 构建镜像
build:
	docker-compose build

# 启动服务
up:
	chmod +x scripts/start.sh
	./scripts/start.sh

# 启动开发环境
up-dev:
	chmod +x scripts/start-dev.sh
	./scripts/start-dev.sh

# 停止服务
down:
	docker-compose down

# 重启服务
restart:
	docker-compose restart

# 查看日志
logs:
	docker-compose logs -f

# 进入应用容器
shell:
	docker-compose exec app bash

# 运行测试
test:
	docker-compose exec app pytest

# 代码检查
lint:
	docker-compose exec app flake8 app/
	docker-compose exec app mypy app/

# 代码格式化
format:
	docker-compose exec app black app/
	docker-compose exec app isort app/

# 清理Docker资源
clean:
	docker-compose down -v
	docker system prune -f

# 数据库迁移
migrate:
	docker-compose exec app alembic upgrade head

# 启动管理工具
tools:
	docker-compose --profile tools up -d adminer redis-commander
