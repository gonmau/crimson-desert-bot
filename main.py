import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai

# 1. Gemini AI 설정
# 환경 변수에서 API 키를 가져옵니다.
API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

def get_news_data():
    urls = {
        "국내": "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko",
        "해외": "https://news.google.com/rss/search?q=Crimson+Desert+game&hl=en-US&gl=US&ceid=US:en"
    }
    
    combined_text = ""
    for lang, url in urls.items():
        try:
            res = requests.get(url, timeout=15)
            # lxml 설치 오류를 피하기 위해 기본 html.parser 사용
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all('item')[:3]
            for item in items:
                title = item.title.text if item.title else "제목 없음"
                link = item.link.text if item.link else ""
                combined_text += f"[{lang}] {title}\n"
        except Exception as e:
            print(f"{lang} 뉴스 수집 중 오류: {e}")
    
    return combined_text

def summarize_news(news_text):
    if not news_text or len(news_text.strip()) < 10:
        return "수집된 새로운 뉴스가 없습니다."
    
    # 404 오류 해결을 위해 가장 표준적인 모델명 사용
    # 계정에 따라 'gemini-1.5-flash' 혹은 'models/gemini-1.5-flash'가 필요할 수 있음
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        아래 리스트는 게임 '붉은사막'의 최신 뉴스 제목들이야.
        이 내용들을 종합해서 한국어로 요약해줘.
        중요한 정보가 있다면 강조해주고, 뉴스들의 전반적인 분위기를 알려줘.

        뉴스 목록:
        {news_text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 첫 번째 시도 실패 시 대안 모델명으로 재시도
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"AI 요약 모델 호출 실패: {str(e)}"

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        # 디스코드 전송 데이터 구성
        data = {"content": f"🤖 **AI 요약 붉은사막 소식**\n\n{content[:1800]}"}
        requests.post(webhook_url, json=data)

if __name__ == "__main__":
    raw_news = get_news_data()
    summary = summarize_news(raw_news)
    send_discord(summary)
