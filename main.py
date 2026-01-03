import requests
from bs4 import BeautifulSoup
import os

def get_news():
    # 한국과 해외 뉴스 주소
    urls = {
        "🇰🇷 국내 소식": "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko",
        "🌎 해외 소식": "https://news.google.com/rss/search?q=Crimson+Desert+game&hl=en-US&gl=US&ceid=US:en"
    }
    
    message_parts = ["🎮 **오늘의 붉은사막(Crimson Desert) 통합 뉴스** 🎮\n"]
    
    for label, url in urls.items():
        try:
            res = requests.get(url, timeout=15)
            # 파서 에러 방지를 위해 html.parser 사용
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all('item')[:3] # 각 매체별 최신 뉴스 3개씩
            
            if items:
                message_parts.append(f"**{label}**")
                for item in items:
                    title = item.title.text
                    link = item.link.text
                    message_parts.append(f"• {title}\n  <{link}>")
                message_parts.append("") # 한 줄 띄움
        except Exception as e:
            print(f"{label} 수집 중 에러: {e}")
            
    return "\n".join(message_parts)

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url and content:
        # 메시지가 너무 길면 잘림 방지
        payload = {"content": content[:1900]}
        requests.post(webhook_url, json=payload)
        print("전송 완료!")

if __name__ == "__main__":
    news_content = get_news()
    send_discord(news_content)
