#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 新闻总结脚本
支持通义千问（免费）、OpenAI、DeepSeek
"""

import json
import os
from datetime import datetime
from typing import List, Dict


def load_news() -> List[Dict]:
    """加载抓取的新闻"""
    with open('temp/raw_news.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['articles']


def summarize_with_qwen(articles: List[Dict]) -> str:
    """使用通义千问进行总结（免费，推荐）"""
    try:
        import dashscope
        from dashscope import Generation
        
        api_key = os.getenv('QWEN_API_KEY')
        if not api_key:
            raise ValueError("未配置 QWEN_API_KEY")
        
        dashscope.api_key = api_key
        
        # 准备新闻内容
        news_text = "\n\n".join([
            f"【{i+1}】标题：{article['title']}\n"
            f"来源：{article['source']}\n"
            f"简介：{article['summary'][:200]}..."
            for i, article in enumerate(articles[:10])
        ])
        
        prompt = f"""请以专业新闻编辑的角度，用中文总结今天的国际新闻热点。

要求：
1. 从以下新闻中选出 5-8 条最重要、最有影响力的新闻
2. 每条新闻用简洁的语言概括（50-80字）
3. 保持客观中立的报道风格
4. 按重要性排序
5. 格式：## 标题\n\n内容\n\n---

原始新闻：

{news_text}

请开始总结："""
        
        print("🤖 正在使用通义千问 AI 总结...")
        
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt
        )
        
        if response.status_code == 200:
            summary = response.output.text
            print("✅ AI 总结完成")
            return summary
        else:
            raise Exception(f"API 返回错误: {response.message}")
    
    except Exception as e:
        print(f"❌ 通义千问总结失败: {str(e)}")
        return None


def summarize_with_openai(articles: List[Dict]) -> str:
    """使用 OpenAI 进行总结"""
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("未配置 OPENAI_API_KEY")
        
        openai.api_key = api_key
        
        news_text = "\n\n".join([
            f"[{i+1}] {article['title']}\n{article['summary'][:200]}"
            for i, article in enumerate(articles[:10])
        ])
        
        prompt = f"""请用中文总结今天的国际新闻热点，选出 5-8 条最重要的新闻，每条 50-80 字概括。

原始新闻：
{news_text}"""
        
        print("🤖 正在使用 OpenAI 总结...")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        summary = response['choices'][0]['message']['content']
        print("✅ AI 总结完成")
        return summary
    
    except Exception as e:
        print(f"❌ OpenAI 总结失败: {str(e)}")
        return None


def summarize_with_deepseek(articles: List[Dict]) -> str:
    """使用 DeepSeek 进行总结"""
    try:
        import openai
        
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("未配置 DEEPSEEK_API_KEY")
        
        # DeepSeek 使用 OpenAI 兼容 API
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        news_text = "\n\n".join([
            f"[{i+1}] {article['title']}\n{article['summary'][:200]}"
            for i, article in enumerate(articles[:10])
        ])
        
        prompt = f"""请用中文总结今天的国际新闻热点，选出 5-8 条最重要的新闻，每条 50-80 字概括。

原始新闻：
{news_text}"""
        
        print("🤖 正在使用 DeepSeek 总结...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        
        summary = response.choices[0].message.content
        print("✅ AI 总结完成")
        return summary
    
    except Exception as e:
        print(f"❌ DeepSeek 总结失败: {str(e)}")
        return None


def create_fallback_summary(articles: List[Dict]) -> str:
    """创建备用总结（不使用 AI）"""
    print("⚠️  未配置 AI，使用简单格式化...")
    
    summary_parts = []
    for i, article in enumerate(articles[:8], 1):
        summary_parts.append(f"## {i}. {article['title']}")
        summary_parts.append(f"\n**来源**：{article['source']}")
        summary_parts.append(f"\n{article['summary'][:150]}...")
        summary_parts.append(f"\n\n[📰 阅读原文]({article['link']})")
        summary_parts.append("\n\n---\n")
    
    return "\n".join(summary_parts)


def generate_hexo_post(summary: str, articles: List[Dict]):
    """生成 Hexo 文章"""
    today = datetime.utcnow()
    date_str = today.strftime('%Y-%m-%d')
    datetime_str = today.strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成文章内容
    content = f"""---
title: 国际新闻热点 {date_str}
date: {datetime_str}
categories:
  - 国际新闻
tags:
  - 每日新闻
  - AI总结
  - 国际动态
description: 今日国际新闻热点 AI 智能总结，涵盖政治、经济、科技等领域重要新闻
---

> 📰 本文由 AI 自动生成，精选今日国际重要新闻，每日更新

## 📊 今日新闻概览

{summary}

---

## 📚 新闻来源

本文内容汇总自以下可信新闻源：

"""
    
    # 添加新闻来源列表
    sources = set()
    for article in articles:
        sources.add(article['source'])
    
    for source in sorted(sources):
        content += f"- {source}\n"
    
    content += f"""

---

## 🔗 相关链接

"""
    
    # 添加原文链接
    for i, article in enumerate(articles[:10], 1):
        if article['link']:
            content += f"{i}. [{article['title']}]({article['link']})\n"
    
    content += f"""

---

## ℹ️ 关于本文

- **生成时间**：{datetime_str} UTC
- **数据来源**：多个国际主流新闻媒体
- **总结方式**：AI 智能分析与提炼
- **更新频率**：每日自动更新

> 💡 提示：本文由自动化系统生成，旨在提供快速的新闻概览。详细内容请点击原文链接查看。

---

## 关于作者

👨‍💻 资深程序员，擅长后端/全栈交付与业务落地  
💼 接受项目外包/技术咨询  
🔧 技术栈：JavaScript / Python / Go / Redis / PHP  

📫 联系方式：  
- 邮箱：runundersun@163.com  
- 微信：strive_qiang888  
- GitHub：https://github.com/xuzhengqiang  

> 如果这篇文章对你有帮助，欢迎点赞、收藏、关注！有任何问题或项目合作，随时联系我 😊
"""
    
    # 保存文章
    os.makedirs('source/_posts', exist_ok=True)
    filename = f'source/_posts/{date_str}-daily-international-news.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 文章已生成: {filename}")
    return filename


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("✨ 开始 AI 总结...")
    print("=" * 60)
    
    # 加载新闻
    articles = load_news()
    print(f"📚 已加载 {len(articles)} 条新闻")
    
    if not articles:
        print("❌ 没有新闻可以总结")
        return
    
    # 根据配置选择 AI 服务
    ai_provider = os.getenv('AI_PROVIDER', 'qwen').lower()
    
    summary = None
    
    if ai_provider == 'qwen':
        summary = summarize_with_qwen(articles)
    elif ai_provider == 'openai':
        summary = summarize_with_openai(articles)
    elif ai_provider == 'deepseek':
        summary = summarize_with_deepseek(articles)
    
    # 如果 AI 总结失败，使用备用方案
    if not summary:
        print("\n⚠️  AI 总结失败，使用备用方案...")
        summary = create_fallback_summary(articles)
    
    # 生成 Hexo 文章
    filename = generate_hexo_post(summary, articles)
    
    print("\n" + "=" * 60)
    print("🎉 全部完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()

