import os
import time
from scrapers.scraper_104 import scrape_104
from scrapers.scraper_cake import scrape_cake
from scrapers.scraper_yourator import scrape_yourator
from ai_matcher import evaluate_job
from discord_notifier import send_discord_notification

def read_resume():
    try:
        with open('resume_summary.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("找不到 resume_summary.txt，請建立該檔案並填寫您的履歷摘要。")
        return ""

def main():
    keywords = ["AI Engineer", "Python", "軟體工程師"]
    print(f"=== 啟動每日求職爬蟲 ({', '.join(keywords)}) ===")
    
    resume_text = read_resume()
    if not resume_text:
        return
        
    all_jobs = []
    
    # 1. 抓取各平台職缺
    for keyword in keywords:
        print(f"開始搜尋關鍵字: {keyword}")
        try:
            all_jobs.extend(scrape_104(keyword=keyword, limit=3))
        except Exception as e:
            print(f"104 爬蟲失敗: {e}")
            
        try:
            all_jobs.extend(scrape_cake(keyword=keyword, limit=3))
        except Exception as e:
            print(f"Cake 爬蟲失敗: {e}")
            
        try:
            all_jobs.extend(scrape_yourator(keyword=keyword, limit=3))
        except Exception as e:
            print(f"Yourator 爬蟲失敗: {e}")
            
    print(f"總共抓取到 {len(all_jobs)} 筆職缺，準備進行 AI 評估...")

    # 2. AI 評估
    recommended_jobs = []
    for i, job in enumerate(all_jobs):
        print(f"評估中 ({i+1}/{len(all_jobs)}): {job['platform']} - {job['title']}")
        result = evaluate_job(resume_text, job['title'], job['description'])
        job['score'] = result.get('score', 0)
        job['reason'] = result.get('reason', '無')
        
        # 轉職生建議將門檻調降至 75 分，以獲取更多潛在機會
        if job['score'] >= 75:
            recommended_jobs.append(job)
            
        # 為了避免 Google API 免費版限制 (3 次 / 分鐘)，每次評估完休息 22 秒
        time.sleep(22)

    # 3. 發送 Discord 通知
    if recommended_jobs:
        print(f"評估完成，共有 {len(recommended_jobs)} 筆符合條件，準備發送 Discord 通知...")
        send_discord_notification(recommended_jobs)
        print("發送完成！")
    else:
        print("今日沒有分數超過 70 的推薦職缺。")

if __name__ == "__main__":
    main()
