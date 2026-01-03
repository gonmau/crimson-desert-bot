import requests
from bs4 import BeautifulSoup
import os

def get_news():
    urls = {
        "🇰🇷 국내 소식": "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko",
        "🌎 해외 소식": "https://news.google.com/rss/search?q=Crimson+Desert+game&hl=en-US&gl=US&ceid=US:en"
    }
    
    message_parts = ["🎮 **오늘의 붉은사막(Crimson Desert) 통합 뉴스** 🎮\n"]
    
    for label, url in urls.items():
        try:
            res = requests.get(url, timeout=15)
            # RSS 읽기를 위해 html.parser 사용
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all('item')[:3] 
            
            if items:
                message_parts.append(f"**{label}**")
                for item in items:
                    title = item.title.text
                    link = item.link.text
                    message_parts.append(f"• {title}\n  <{link}>")
                message_parts.append("") 
        except Exception as e:
            print(f"{label} 수집 중 에러: {e}")
            
    return "\n".join(message_parts)

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url and content:
        payload = {"content": content[:1900]}
        requests.post(webhook_url, json=payload)
        print("디스코드 전송 완료!")
    else:
        print("설정 오류: 웹훅 URL이 없거나 보낼 내용이 없습니다.")

if __name__ == "__main__":
    news_content = get_news()
    send_discord(news_content)
