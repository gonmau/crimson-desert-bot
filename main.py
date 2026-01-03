import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai

# 1. Gemini AI 설정
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
            # 타임아웃을 설정하여 무한 대기 방지
            res = requests.get(url, timeout=15)
            # lxml 오류를 방지하기 위해 기본 html.parser 사용
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all('item')[:3]
            
            for item in items:
                title = item.title.text if item.title else "제목 없음"
                # 불필요한 태그나 공백 제거
                combined_text += f"[{lang}] {title}\n"
        except Exception as e:
            print(f"{lang} 뉴스 수집 중 오류: {e}")
    
    return combined_text

def summarize_news(news_text):
    if not news_text or len(news_text.strip()) < 10:
        return "수집된 새로운 뉴스가 없습니다."
    
    prompt = f"""
    당신은 게임 전문 기자입니다. 아래 뉴스 목록을 읽고 '붉은사막' 게임에 대한 핵심 내용을 한국어로 요약해주세요.
    - 각 뉴스별로 번호를 매겨 핵심만 요약할 것.
    - 중요한 날짜나 이벤트가 있다면 강조할 것.
    - 뉴스 목록:
    {news_text}
    """
    
    # 계정 상태에 따라 다른 모델 경로를 3번 시도합니다.
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-1.5-flash-latest']
    
    for model_name in model_names:
        try:
            print(f"시도 중인 모델: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"{model_name} 호출 실패: {e}")
            continue
            
    return "모든 AI 모델 호출에 실패했습니다. API 키의 모델 권한을 확인해주세요."

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("디스코드 웹훅 URL이 설정되지 않았습니다.")
        return

    # 디스코드 메시지 전송 (2000자 제한 대응)
    payload = {
        "username": "붉은사막 AI 알리미",
        "content": f"🎮 **오늘의 붉은사막 소식 요약** 🎮\n\n{content[:1800]}"
    }
    
    try:
        res = requests.post(webhook_url, json=payload)
        if res.status_code == 204:
            print("디스코드 전송 성공!")
        else:
            print(f"디스코드 전송 실패: {res.status_code}")
    except Exception as e:
        print(f"전송 중 에러: {e}")

if __name__ == "__main__":
    print("작업을 시작합니다...")
    news_data = get_news_data()
    print(f"수집된 뉴스 데이터:\n{news_data}")
    
    summary_result = summarize_news(news_data)
    send_discord(summary_result)
    print("모든 작업이 완료되었습니다.")
