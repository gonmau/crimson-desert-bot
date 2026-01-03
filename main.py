import requests
from bs4 import BeautifulSoup
import os

def get_news(url, count=3):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:count]
        
        results = []
        for item in items:
            # 제목과 링크 추출
            title = item.title.text
            link = item.link.text
            results.append(f"• **{title}**\n  <{link}>")
        return results
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def main():
    # 1. 한국 소식 (붉은사막)
    kr_url = "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko"
    kr_news = get_news(kr_url)

    # 2. 해외 소식 (Crimson Desert) - 미국 구글 뉴스 기준
    en_url = 'https://news.google.com/rss/search?q="Crimson+Desert"&hl=en-US&gl=US&ceid=US:en'
    en_news = get_news(en_url)

    # 메시지 조립
    message_parts = ["🎮 **오늘의 붉은사막(Crimson Desert) 통합 소식** 🎮\n"]
    
    if kr_news:
        message_parts.append("🇰🇷 **국내 최신 뉴스**")
        message_parts.extend(kr_news)
    
    message_parts.append("\n-------------------\n")
    
    if en_news:
        message_parts.append("🌎 **해외 최신 뉴스 (Global)**")
        message_parts.extend(en_news)

    full_content = "\n".join(message_parts)

    # 디스크드로 전송
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        payload = {"content": full_content}
        requests.post(webhook_url, json=payload)
        print("전송 완료!")
    else:
        print("Webhook URL이 설정되지 않았습니다.")

if __name__ == "__main__":
    main()
