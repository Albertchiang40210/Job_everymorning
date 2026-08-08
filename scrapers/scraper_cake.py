from playwright.sync_api import sync_playwright

def scrape_cake(keyword="AI Engineer", limit=10):
    print(f"[Cake] 開始搜尋: {keyword} (使用 Playwright)")
    jobs = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = f"https://www.cakeresume.com/jobs?q={keyword}"
            page.goto(url, wait_until="domcontentloaded")
            
            # 等待職缺卡片載入，CakeResume 的卡片通常有 JobSearchItem 類別或類似結構
            # 這裡我們嘗試抓取連結包含 /companies/.../jobs/... 的 a 標籤
            page.wait_for_selector('a[href*="/jobs/"]', timeout=10000)
            
            links = page.query_selector_all('a[href*="/jobs/"]')
            
            seen_links = set()
            for link_elem in links:
                href = link_elem.get_attribute('href')
                if href and '/companies/' in href and href not in seen_links:
                    seen_links.add(href)
                    
                    title = link_elem.inner_text().strip()
                    # 避免抓到只有圖片的連結或整塊卡片
                    title_lines = [line for line in title.split('\n') if line.strip()]
                    job_title = title_lines[0] if title_lines else "職缺"
                    
                    full_link = "https://www.cakeresume.com" + href if href.startswith("/") else href
                    
                    jobs.append({
                        "platform": "Cake",
                        "title": job_title,
                        "company": "CakeResume 上企業",  # Cake 的結構比較難單純用語法抓公司，先給通用文字
                        "link": full_link,
                        "description": "建議點擊連結查看詳細資訊"
                    })
                    
                if len(jobs) >= limit:
                    break
                    
            browser.close()
    except Exception as e:
        print(f"[Cake] 爬蟲發生錯誤: {e}")
        
    return jobs

if __name__ == "__main__":
    res = scrape_cake()
    for r in res:
        print(r['title'])
