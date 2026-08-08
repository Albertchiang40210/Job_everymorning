# Daily AI Job Scraper (每日 AI 求職小幫手)

這是一個自動化的求職爬蟲專案，專為尋找理想職缺而設計。它會每天自動爬取各大求職平台，並使用 Google Gemini AI 模型，將職缺內容與求職者的個人履歷進行智能比對。只要匹配度高於 90 分，就會自動發送通知到 Discord。

## 支援的求職平台
- 104 人力銀行
- CakeResume (Cake)
- Yourator

## 功能特色
1. **全自動化執行**：透過 GitHub Actions，每天早上 8 點 (UTC 00:00) 自動在雲端執行，完全不需開啟個人電腦。
2. **AI 智能匹配**：導入 Gemini AI 模型作為職涯顧問，不僅是關鍵字比對，更能理解職缺需求與求職者經歷的適配程度。
3. **即時通知**：篩選出高分職缺後，透過 Discord Webhook 傳送職缺連結與 AI 推薦理由，打造個人的職缺快報。
4. **資安保護**：API 金鑰與 Webhook 網址皆透過 GitHub Secrets 環境變數保護，確保個人隱私與資訊安全。

## 使用技術
- Python 3.12
- Requests & BeautifulSoup4 (靜態網頁解析)
- Playwright (動態網頁處理)
- Google Generative AI SDK (Gemini AI 整合)
- GitHub Actions (CI/CD 自動化排程)
