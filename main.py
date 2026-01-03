import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def get_news(url, label):
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:3]
        
        print(f"[{label}] 검색 결과: {len(items)}개의 뉴스를 찾았습니다.") # 로그 출력
        
        results = []
        for item in items:
            title = item.title.text
            link = item.link.text
            results.append(f"• **{title}**\n  <{link}>")
        return results
    except Exception as e:
        print(f"[{label}] 에러 발생: {e}")
        return []

def main():
    # 현재 시간 (한국 시간 기준 출력을 위해 +9시간 하거나 단순 출력)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. 한국 소식
    kr_url = "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko"
    kr_news = get_news(kr_url, "한국")

    # 2. 해외 소식 (검색어 범위를 조금 더 넓혔습니다)
    en_url = "https://news.google.com/rss/search?q=Crimson+Desert+game&hl=en-US&gl=US&ceid=US:en"
    en_news = get_news(en_url, "해외")

    if not kr_news and not en_news:
        print("새로운 뉴스가 하나도 없습니다. 전송을 중단합니다.")
        return

    # 메시지 조립
    message_parts = [f"📅 **업데이트 시간: {now}**\n"]
    
    if kr_news:
        message_parts.append("🇰🇷 **국내 최신 뉴스**")
        message_parts.extend(kr_news)
    
    message_parts.append("\n" + "="*30 + "\n")
    
    if en_news:
        message_parts.append("🌎 **Global News (Crimson Desert)**")
        message_parts.extend(en_news)

    full_content = "\n".join(message_parts)

    # 디스코드 전송
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        res = requests.post(webhook_url, json={"content": full_content})
        print(f"디스코드 응답 코드: {res.status_code} (204면 성공)")
    else:
        print("WEBHOOK_URL 설정이 없습니다.")

if __name__ == "__main__":
    main()
