#!/bin/bash

# 设置环境变量
export FLASK_ENV=testing
export PYTHONPATH=$(pwd)

# 运行测试并生成覆盖率报告
echo "运行测试并生成覆盖率报告..."
pytest --cov=app --cov-report=term --cov-report=html:coverage_report tests/ -v --ignore=tests/integration/test_amap_client.py

# 如果设置了高德API密钥，运行真实API测试
if [ ! -z "$TEST_AMAP_KEY" ]; then
    echo "运行高德API测试..."
    export TEST_WITH_REAL_AMAP_API=1
    pytest tests/integration/test_amap_client.py -v
fi

echo "测试完成! 覆盖率报告已生成在 coverage_report 目录"
