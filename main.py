import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai

# 1. Gemini AI 설정
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_news_data():
    urls = {
        "국내": "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko",
        "해외": "https://news.google.com/rss/search?q=Crimson+Desert+game&hl=en-US&gl=US&ceid=US:en"
    }
    
    combined_text = ""
    for lang, url in urls.items():
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'xml')
        items = soup.find_all('item')[:3] # 각 3개씩
        for item in items:
            combined_text += f"[{lang}] 제목: {item.title.text}\n링크: {item.link.text}\n\n"
    
    return combined_text

def summarize_news(news_text):
    if not news_text:
        return "새로운 뉴스가 없습니다."
    
    prompt = f"""
    아래는 게임 '붉은사막(Crimson Desert)'에 관한 최신 뉴스 목록이야.
    각 뉴스별로 핵심 내용을 한 문장으로 요약해서 번호표를 붙여서 한글로 알려줘.
    중요한 업데이트나 출시 관련 소식이 있다면 강조해줘.
    
    뉴스 목록:
    {news_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    # 디스코드 글자 수 제한(2000자)을 고려해 자르기
    payload = {"content": f"🤖 **AI 요약 붉은사막 소식**\n\n{content[:1800]}"}
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    raw_news = get_news_data()
    summary = summarize_news(raw_news)
    send_discord(summary)
