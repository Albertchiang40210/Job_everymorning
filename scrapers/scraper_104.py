from playwright.sync_api import sync_playwright
import time

def scrape_104(keyword="AI Engineer", limit=10):
    print(f"[104] 開始搜尋: {keyword} (使用 Playwright)")
    jobs = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # 前往 104 搜尋頁面
            url = f"https://www.104.com.tw/jobs/search/?keyword={keyword}&order=1&jobsource=2018indexpoc&ro=0"
            page.goto(url, wait_until="domcontentloaded")
            
            # 等待職缺列表載入
            page.wait_for_selector('article.job-list-item', timeout=10000)
            
            articles = page.query_selector_all('article.job-list-item')
            for article in articles[:limit]:
                # 抓取標題
                title_elem = article.query_selector('a.info-job__text')
                title = title_elem.inner_text().strip() if title_elem else ""
                
                # 抓取連結
                link = title_elem.get_attribute('href') if title_elem else ""
                if link and link.startswith("//"):
                    link = "https:" + link
                    
                # 抓取公司
                comp_elem = article.query_selector('ul.info-company li a')
                company = comp_elem.inner_text().strip() if comp_elem else ""
                
                # 抓取敘述
                desc_elem = article.query_selector('p.info-job__desc')
                desc = desc_elem.inner_text().strip() if desc_elem else "無敘述"
                
                if title and link:
                    jobs.append({
                        "platform": "104",
                        "title": title,
                        "company": company,
                        "link": link,
                        "description": desc[:300]
                    })
                    
            browser.close()
    except Exception as e:
        print(f"[104] 爬蟲發生錯誤: {e}")
        
    return jobs

if __name__ == "__main__":
    res = scrape_104()
    for r in res:
        print(r['title'], r['company'])
