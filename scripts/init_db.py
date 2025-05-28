#!/usr/bin/env python3
import os
import sys
import pymysql
import time


def wait_for_db(host, port, user, password, max_attempts=30, wait_seconds=2):
    """等待数据库准备就绪"""
    print("等待MySQL数据库准备就绪...")
    attempts = 0
    while attempts < max_attempts:
        try:
            conn = pymysql.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                connect_timeout=5
            )
            conn.close()
            print("数据库连接成功!")
            return True
        except pymysql.Error as e:
            attempts += 1
            print(f"尝试连接数据库 ({attempts}/{max_attempts}): {e}")
            time.sleep(wait_seconds)

    print("无法连接到数据库，超过最大尝试次数")
    return False


def init_database(host, port, user, password, db_name):
    """初始化数据库"""
    try:
        # 首先尝试连接到MySQL服务器
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )

        with conn.cursor() as cursor:
            # 检查数据库是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()

            if not result:
                print(f"创建数据库 {db_name}...")
                cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"数据库 {db_name} 创建成功")
            else:
                print(f"数据库 {db_name} 已存在")

        conn.close()

        # 连接到指定的数据库
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=db_name
        )

        with conn.cursor() as cursor:
            # 读取SQL文件
            sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                         'docker', 'mysql', 'init', 'init.sql')

            with open(sql_file_path, 'r') as f:
                sql_script = f.read()

            # 分割SQL语句并执行
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)

            conn.commit()
            print("数据库表创建成功")

        conn.close()
        return True

    except pymysql.Error as e:
        print(f"数据库初始化失败: {e}")
        return False


if __name__ == "__main__":
    # 从环境变量获取数据库配置
    db_host = os.environ.get('MYSQL_HOST', 'localhost')
    db_port = os.environ.get('MYSQL_PORT', '3306')
    db_user = os.environ.get('MYSQL_USER', 'root')
    db_password = os.environ.get('MYSQL_PASSWORD', 'password')
    db_name = os.environ.get('MYSQL_DATABASE', 'trip_planner')

    # 等待数据库准备就绪
    if not wait_for_db(db_host, db_port, db_user, db_password):
        sys.exit(1)

    # 初始化数据库
    if init_database(db_host, db_port, db_user, db_password, db_name):
        print("数据库初始化完成")
        sys.exit(0)
    else:
        print("数据库初始化失败")
        sys.exit(1)
