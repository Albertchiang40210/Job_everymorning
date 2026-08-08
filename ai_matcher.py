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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
    你是一個專業的職涯顧問。請根據以下求職者的「履歷摘要」與「職缺資訊」，評估此職缺與求職者的匹配程度。
    
    【求職者履歷摘要】
    {resume_text}
    
    【職缺資訊】
    職缺名稱：{job_title}
    職缺描述：{job_description}
    
    請務必以 JSON 格式回覆，格式如下：
    {{"score": 85, "reason": "因為具備 Python 技能，符合職缺需求。"}}
    score 必須是 0 到 100 的整數。
    """
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            # 這裡簡單提取 JSON 內容
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            
            # 清理 Markdown JSON 標記
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                text_response = text_response[3:-3]
                
            return json.loads(text_response.strip())
        else:
            print(f"Gemini API 請求失敗，狀態碼: {response.status_code}")
            # 落後備援機制：如果 API 壞掉或限制，改用簡單關鍵字判斷
            score = 60
            reason = "API 無法使用，使用基礎判斷。缺少關鍵技能。"
            desc = job_description.lower()
            if "python" in desc or "ai" in desc or "machine learning" in desc or "deep learning" in desc:
                score += 20
                reason = "API 降級模式：發現 Python/AI 等關鍵字，初步判定符合。"
            if "junior" in desc or "助理" in desc or "實習" in desc:
                score += 15
                reason += " 適合初階/實習等級。"
            elif "senior" in desc or "資深" in desc:
                score -= 10
            
            if score > 100: score = 100
            if score >= 90:
                reason = "[關鍵字精準命中] " + reason
            
            return {"score": score, "reason": reason}
            
    except Exception as e:
        return {"score": 0, "reason": f"例外錯誤: {str(e)}"}
