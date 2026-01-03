import requests
from bs4 import BeautifulSoup
import os

def get_news():
    url = "https://news.google.com/rss/search?q=붉은사막&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')[:5]

    news_list = []
    for item in items:
        news_list.append(f"**{item.title.text}**\n<{item.link.text}>")
    return "\n\n".join(news_list)

def send_discord(content):
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    payload = {"content": f"🎮 **붉은사막 최신 소식** 🎮\n\n{content}"}
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    news = get_news()
    if news:
        send_discord(news)
