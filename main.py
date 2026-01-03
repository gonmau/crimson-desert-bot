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
        try:
            res = requests.get(url, timeout=15)
            # 'xml' 대신 'html.parser'를 사용하여 호환성 높임
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all('item')[:3]
            for item in items:
                title = item.title.text if item.title else "제목 없음"
                link = item.link.text if item.link else ""
                combined_text += f"[{lang}] 제목: {title}\n링크: {link}\n\n"
        except Exception as e:
            print(f"{lang} 뉴스 수집 중 오류: {e}")
    
    return combined_text

def summarize_news(news_text):
    if not news_text or len(news_text.strip()) < 10:
        return "수집된 새로운 뉴스가 없습니다."
    
    prompt = f"""
    아래 뉴스 목록을 읽고 '붉은사막' 게임에 대한 핵심 내용을 한국어로 요약해줘.
    - 각 뉴스별로 번호를 매겨서 요약할 것.
    - 중요한 날짜나 이벤트가 있다면 강조할 것.
    - 한국어로 친절하게 설명할 것.

    목록:
    {news_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"요약 중 오류 발생: {e}"

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        payload = {"content": f"🤖 **AI 요약 붉은사막 소식**\n\n{content[:1800]}"}
        requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    raw_news = get_news_data()
    summary = summarize_news(raw_news)
    send_discord(summary)
