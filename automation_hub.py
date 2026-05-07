import schedule
import time
import requests
import asyncio
from app import ContentFactoryWeb # 复用核心类

# 配置信息
CONFIG = {
    "api_key": "sk-e0f19ae66d0d40b79a2b02b1e05c5cb4",
    "base_url": "https://api.deepseek.com",
    "model_name": "deepseek-chat",
    "tavily_key": "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",
    "webhook": "https://oapi.dingtalk.com/robot/send?access_token=3eb7a5bf73c50bd6e05f34e265d52180027d9613bbb57894b359a55ce50e92d6", # 钉钉/飞书
    "topics": ["AI新基建", "低空经济趋势"]
}

def send_alert(content, topic):
    payload = {"msgtype": "markdown", "markdown": {"title": topic, "text": content}}
    requests.post(CONFIG["webhook"], json=payload)

def automated_job():
    print("开始执行定时任务...")
    factory = ContentFactoryWeb(CONFIG["api_key"], CONFIG["base_url"], CONFIG["model_name"], CONFIG["tavily_key"])
    for topic in CONFIG["topics"]:
        data = factory.fetch_real_time_trends(topic)
        analysis = factory.trend_analyzer_agent(data)
        script = factory.script_writer_agent(analysis)
        factory.save_to_db(topic, data, script)
        send_alert(script, f"自动产出：{topic}")

# 每天 09:00 自动执行
schedule.every().day.at("09:00").do(automated_job)

# 【关键修正】：加上括号 () 即可立刻开始测试运行
print("正在执行首次启动测试...")
automated_job()

print("\n🕒 自动化中枢已启动，正在后台监听定时任务...")
while True:
    schedule.run_pending()
    time.sleep(1)