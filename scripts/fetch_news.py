#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国际新闻抓取脚本
支持多个 RSS 源和 NewsAPI
"""

import feedparser
import json
import os
from datetime import datetime
from typing import List, Dict

# 国际新闻 RSS 源配置
RSS_SOURCES = [
    {
        'name': 'BBC World',
        'url': 'https://feeds.bbci.co.uk/news/world/rss.xml',
        'enabled': True
    },
    {
        'name': 'CNN World',
        'url': 'http://rss.cnn.com/rss/edition_world.rss',
        'enabled': True
    },
    {
        'name': 'Reuters World',
        'url': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
        'enabled': True
    },
    {
        'name': 'Google News',
        'url': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en',
        'enabled': True
    },
    {
        'name': 'The Guardian World',
        'url': 'https://www.theguardian.com/world/rss',
        'enabled': True
    }
]


def fetch_rss_news(source: Dict) -> List[Dict]:
    """从 RSS 源抓取新闻"""
    print(f"📡 正在抓取 {source['name']}...")
    
    try:
        feed = feedparser.parse(source['url'])
        
        if not feed.entries:
            print(f"⚠️  {source['name']} 没有返回内容")
            return []
        
        articles = []
        for entry in feed.entries[:5]:  # 每个源取前 5 条
            article = {
                'title': entry.get('title', 'No title'),
                'summary': entry.get('summary', entry.get('description', '')),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'source': source['name']
            }
            articles.append(article)
        
        print(f"✅ {source['name']} 抓取成功，获得 {len(articles)} 条新闻")
        return articles
    
    except Exception as e:
        print(f"❌ {source['name']} 抓取失败: {str(e)}")
        return []


def fetch_newsapi_news() -> List[Dict]:
    """使用 NewsAPI 抓取新闻（可选，需要 API Key）"""
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("ℹ️  未配置 NEWS_API_KEY，跳过 NewsAPI")
        return []
    
    print("📡 正在从 NewsAPI 抓取...")
    
    try:
        import requests
        
        url = 'https://newsapi.org/v2/top-headlines'
        params = {
            'apiKey': api_key,
            'language': 'en',
            'pageSize': 10,
            'category': 'general'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for item in data.get('articles', [])[:5]:
            article = {
                'title': item.get('title', ''),
                'summary': item.get('description', ''),
                'link': item.get('url', ''),
                'published': item.get('publishedAt', ''),
                'source': f"NewsAPI - {item.get('source', {}).get('name', 'Unknown')}"
            }
            articles.append(article)
        
        print(f"✅ NewsAPI 抓取成功，获得 {len(articles)} 条新闻")
        return articles
    
    except Exception as e:
        print(f"❌ NewsAPI 抓取失败: {str(e)}")
        return []


def main():
    """主函数"""
    print("=" * 60)
    print("🌍 开始抓取国际新闻...")
    print("=" * 60)
    
    all_articles = []
    
    # 从 RSS 源抓取
    for source in RSS_SOURCES:
        if source['enabled']:
            articles = fetch_rss_news(source)
            all_articles.extend(articles)
    
    # 从 NewsAPI 抓取（可选）
    newsapi_articles = fetch_newsapi_news()
    all_articles.extend(newsapi_articles)
    
    # 去重（根据标题）
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title_lower = article['title'].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_articles.append(article)
    
    print("\n" + "=" * 60)
    print(f"📊 总计抓取 {len(all_articles)} 条新闻，去重后 {len(unique_articles)} 条")
    print("=" * 60)
    
    # 保存到文件
    output = {
        'timestamp': datetime.utcnow().isoformat(),
        'total': len(unique_articles),
        'articles': unique_articles
    }
    
    os.makedirs('temp', exist_ok=True)
    
    with open('temp/raw_news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 新闻已保存到 temp/raw_news.json")
    print(f"📰 准备进行 AI 总结...")


if __name__ == '__main__':
    main()

