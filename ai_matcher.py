import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def evaluate_job(resume_text: str, job_title: str, job_description: str) -> dict:
    """
    使用 Gemini REST API 評估職缺是否適合。
    回傳字典： {"score": 85, "reason": "簡單說明..."}
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("未設定 GEMINI_API_KEY，將跳過 AI 評估。")
        return {"score": 0, "reason": "No API Key"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/deep-research-preview-04-2026:generateContent?key={api_key}"
    
    prompt = f"""
    你是一個專業的職涯顧問。請根據以下求職者的「履歷摘要」與「職缺資訊」，評估此職缺與求職者的匹配程度。
    
    【求職者履歷摘要】
    {resume_text}
    
    【職缺標題】
    {job_title}
    
    【職缺內容】
    {job_description}
    
    請以 JSON 格式回傳，包含以下兩個欄位：
    - "score": 匹配分數 (整數 0 到 100，越高越匹配)
    - "reason": 給求職者的簡短推薦理由 (繁體中文，限制在 50 字以內，說明為什麼適合或不適合)
    
    注意：只回傳 JSON，不要包含其他文字或 Markdown 標籤 (如 ```json)。
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            try:
                text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                # 移除可能存在的 markdown json 標籤
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                
                result = json.loads(text.strip())
                return {
                    "score": int(result.get("score", 0)),
                    "reason": result.get("reason", "解析失敗")
                }
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(f"AI 回應格式錯誤: {e}")
                return {"score": 0, "reason": "AI 回應無法解析"}
        else:
            print(f"Gemini API 請求失敗，狀態碼: {response.status_code}, {response.text}")
            return {"score": 0, "reason": f"API 錯誤: {response.status_code}"}
            
    except Exception as e:
        print(f"AI 評估時發生例外錯誤: {e}")
        return {"score": 0, "reason": f"例外錯誤: {str(e)}"}
