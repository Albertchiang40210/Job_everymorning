import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_discord_notification(jobs: list):
    """
    將推薦的職缺列表發送到 Discord Webhook。
    jobs 的格式預期為：
    [
        {
            "title": "AI 工程師",
            "company": "某某科技",
            "link": "https://...",
            "platform": "104",
            "score": 90,
            "reason": "熟悉 PyTorch，與職缺要求相符。"
        },
        ...
    ]
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("未設定 DISCORD_WEBHOOK_URL，跳過通知發送。")
        return

    if not jobs:
        print("今日沒有推薦的職缺。")
        # 也可選擇發送一則空通知
        return

    # Discord 每個 embed 訊息有字數限制，我們用 Embed 來美化
    embeds = []
    
    # 按照分數由高到低排序
    jobs_sorted = sorted(jobs, key=lambda x: x.get('score', 0), reverse=True)

    for job in jobs_sorted:
        score = job.get('score', 0)
        
        # 決定顏色 (高分綠色，中分黃色，低分紅色)
        color = 5763719 # 預設綠色
        if score < 70:
            color = 16711680 # 紅色
        elif score < 85:
            color = 16776960 # 黃色
            
        embed = {
            "title": f"[{job.get('platform')}] {job.get('title')}",
            "url": job.get('link'),
            "description": f"**公司:** {job.get('company')}\n**匹配度:** {score} 分\n**AI 簡評:** {job.get('reason')}",
            "color": color
        }
        embeds.append(embed)

    # 由於 Discord webhook 一次最多發送 10 個 embeds，需要分批發送
    chunk_size = 10
    for i in range(0, len(embeds), chunk_size):
        chunk = embeds[i:i + chunk_size]
        payload = {
            "content": "🔔 **今日 AI 推薦職缺來囉！**" if i == 0 else "",
            "embeds": chunk
        }
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"發送 Discord 通知失敗: {e}")

