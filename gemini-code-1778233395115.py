import schedule
import time
import requests
import asyncio
from app import ContentFactoryWeb # 复用核心类

# 配置信息
CONFIG = {
    # 如果你是官方 OpenAI，用 sk-xxx，绘画 DALL-E 3 也用这个。
    "api_key": "YOUR_OPENAI_KEY_FOR_DALLE", 
    "base_url": "https://api.deepseek.com", # DeepSeek 没有绘画，绘图会调用 dall-e-3
    "model_name": "deepseek-chat",
    "tavily_key": "YOUR_TAVILY_KEY",
    "webhook": "YOUR_DINGTALK_WEBHOOK", 
    "topics": ["AI新基建"]
}

def send_alert(content, topic):
    """注意：Markdown 表格和本地图片路径在钉钉中展示通常有限制"""
    payload = {"msgtype": "markdown", "markdown": {"title": topic, "text": content}}
    requests.post(CONFIG["webhook"], json=payload)

def automated_job():
    print("开始后台定时自动化配图任务...")
    factory = ContentFactoryWeb(CONFIG["api_key"], CONFIG["base_url"], CONFIG["model_name"], CONFIG["tavily_key"])
    for topic in CONFIG["topics"]:
        data = factory.fetch_real_time_trends(topic)
        analysis = factory.trend_analyzer_agent(data)
        script = factory.script_writer_agent(analysis)
        
        # 调用绘画 Agent
        script_with_images = factory. artist_agent(script, topic)
        
        # 入库
        factory.save_to_db(topic, data, script_with_images)
        # 钉钉推送
        send_alert(script_with_images, topic)
        print(f"话题 {topic} 配图完成并推送。")

automated_job() # 首次启动立即执行

schedule.every().day.at("09:00").do(automated_job)

while True:
    schedule.run_pending()
    time.sleep(1)