import os
import time
import schedule
import pymysql
import requests

# 1. 从 Railway 环境变量读取 Zeabur 数据库连接密码
DB_HOST = os.getenv("DB_HOST", "您的Zeabur数据库地址")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "您的密码")
DB_NAME = os.getenv("DB_NAME", "yuqing_db")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def connect_db():
    """连接到 Zeabur 的 MySQL 数据库"""
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=DB_PORT
    )

def crawl_and_save():
    """核心抓取与存储逻辑"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 开始执行全网舆情抓取任务...")
    
    # 这里是模拟思通的抓取逻辑（由于脱水，这里先搭好框架）
    # 实际中我们会接入具体的微博/新闻解析代码
    mock_data = [
        {"title": "半导体行业最新突破", "source": "科技新闻", "sentiment": "positive"},
        {"title": "某大厂AI模型发布", "source": "微博热搜", "sentiment": "neutral"}
    ]
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        # 建表（如果不存在）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public_opinion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                source VARCHAR(100),
                sentiment VARCHAR(50),
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # 写入数据
        for item in mock_data:
            cursor.execute(
                "INSERT INTO public_opinion (title, source, sentiment) VALUES (%s, %s, %s)",
                (item['title'], item['source'], item['sentiment'])
            )
        conn.commit()
        conn.close()
        print("✅ 舆情数据已成功写入 Zeabur 数据库！")
    except Exception as e:
        print(f"❌ 数据库写入失败，请检查连接: {e}")

# 2. 调度器：每隔 1 小时自动抓取一次
schedule.every(1).hours.do(crawl_and_save)

if __name__ == "__main__":
    print("🟢 思通舆情（脱水核心版）已启动，正在监听全网数据...")
    crawl_and_save() # 启动时先抓一次
    while True:
        schedule.run_pending()
        time.sleep(60)
