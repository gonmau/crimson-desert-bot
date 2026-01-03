import requests
from bs4 import BeautifulSoup
import os

def get_crimson_desert_news():
    # 붉은사막 키워드로 뉴스 가져오기
    url = "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')[:5]
    
    news_list = []
    for item in items:
        title = item.title.text
        link = item.link.text
        news_list.append(f"**{title}**\n<{link}>") # 디스코드는 <>로 감싸면 미리보기를 깔끔하게 처리함
    
    return "\n\n".join(news_list)

def send_discord_message(content):
    # GitHub Secrets에 저장한 WEBHOOK_URL 사용
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    
    payload = {
        "username": "붉은사막 알리미",
        "avatar_url": "https://i.imgur.com/4S9S6S6.png", # 봇 프로필 이미지 (선택)
        "content": f"🎮 **오늘의 붉은사막 소식입니다!** 🎮\n\n{content}"
    }
    
    # 디스코드로 전송
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("디스코드 전송 성공!")
    else:
        print(f"전송 실패: {response.status_code}")

if __name__ == "__main__":
    news_content = get_crimson_desert_news()
    if news_content:
        send_discord_message(news_content)
