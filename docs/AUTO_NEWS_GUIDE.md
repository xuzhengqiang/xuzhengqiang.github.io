# 📰 每日国际新闻自动化指南

本项目已集成**自动抓取国际新闻 + AI 总结 + 自动发布**功能，每天自动生成一篇新闻汇总文章。

---

## 🎯 功能特点

- ✅ **多源抓取**：BBC、CNN、Reuters、Google News 等国际主流媒体
- ✅ **AI 总结**：支持通义千问（免费）、OpenAI、DeepSeek
- ✅ **自动发布**：GitHub Actions 定时运行，自动推送到博客
- ✅ **完全免费**：使用 RSS + 免费 AI 服务，零成本运行
- ✅ **每日更新**：每天早上 9 点（北京时间）自动生成

---

## 🚀 快速开始（5 分钟配置）

### 步骤 1：申请免费 AI API Key

#### 方案 A：通义千问（推荐，最简单）

1. 访问：https://dashscope.aliyun.com/
2. 登录阿里云账号（手机号注册）
3. 开通"灵积"服务（免费）
4. 创建 API Key
5. 复制 API Key（格式：`sk-xxxxxxxx`）

**免费额度**：100 万 tokens/月（够用几个月）

---

#### 方案 B：DeepSeek（便宜，效果好）

1. 访问：https://platform.deepseek.com/
2. 注册账号
3. 充值 $5（够用半年）
4. 创建 API Key

**费用**：$0.001/1K tokens（每天约 $0.005）

---

#### 方案 C：OpenAI（如果你有的话）

如果你已经有 OpenAI API Key，可以直接使用。

---

### 步骤 2：配置 GitHub Secrets

1. 打开你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下密钥：

| Name | Value | 说明 |
|------|-------|------|
| `QWEN_API_KEY` | `sk-你的千问密钥` | 通义千问 API Key |
| `AI_PROVIDER` | `qwen` | 使用哪个 AI（qwen/openai/deepseek） |

**可选配置**（如果你有其他 API Key）：

| Name | Value | 说明 |
|------|-------|------|
| `OPENAI_API_KEY` | `sk-你的OpenAI密钥` | OpenAI API Key（可选） |
| `DEEPSEEK_API_KEY` | `sk-你的DeepSeek密钥` | DeepSeek API Key（可选） |
| `NEWS_API_KEY` | `你的NewsAPI密钥` | NewsAPI Key（可选，用于补充） |

---

### 步骤 3：手动触发测试

1. 打开 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Daily News Summary** 工作流
4. 点击右侧 **Run workflow** → **Run workflow**
5. 等待 2-3 分钟，查看运行结果

如果成功，你会在 `source/_posts/` 目录看到今天的新闻文章！

---

### 步骤 4：自动运行

配置完成后，工作流会**每天早上 9 点（北京时间）**自动运行，无需任何操作。

---

## 📋 配置说明

### 新闻源配置

默认抓取以下新闻源（完全免费）：

- **BBC World**：https://feeds.bbci.co.uk/news/world/rss.xml
- **CNN World**：http://rss.cnn.com/rss/edition_world.rss
- **Reuters**：路透社官方 RSS
- **Google News**：谷歌新闻聚合
- **The Guardian**：卫报世界新闻

**修改新闻源**：编辑 `scripts/fetch_news.py` 文件中的 `RSS_SOURCES` 配置。

---

### AI 服务配置

支持 3 种 AI 服务：

| AI 服务 | 成本 | 效果 | 速度 | 推荐指数 |
|---------|------|------|------|---------|
| **通义千问** | 免费 | ⭐⭐⭐⭐ | 快 | ⭐⭐⭐⭐⭐ |
| **DeepSeek** | $0.001/1K | ⭐⭐⭐⭐⭐ | 快 | ⭐⭐⭐⭐ |
| **OpenAI** | $0.002/1K | ⭐⭐⭐⭐⭐ | 中 | ⭐⭐⭐ |

**切换 AI 服务**：修改 GitHub Secrets 中的 `AI_PROVIDER` 值。

---

### 运行时间配置

默认运行时间：**每天早上 9:00（北京时间）**

**修改运行时间**：编辑 `.github/workflows/daily-news.yml` 文件：

```yaml
schedule:
  # UTC 时间（北京时间 = UTC + 8）
  - cron: '0 1 * * *'  # 早上 9:00
  # - cron: '0 13 * * *'  # 晚上 9:00
```

---

## 📊 文章格式

自动生成的文章包含：

1. **标题**：国际新闻热点 YYYY-MM-DD
2. **分类**：国际新闻
3. **标签**：每日新闻、AI总结、国际动态
4. **内容**：
   - AI 精选的 5-8 条重要新闻
   - 每条新闻简洁概括（50-80 字）
   - 原文链接
   - 新闻来源说明

---

## 🔧 高级配置

### 1. 修改文章数量

编辑 `scripts/fetch_news.py`：

```python
for entry in feed.entries[:5]:  # 改成你想要的数量
```

---

### 2. 添加新的 RSS 源

编辑 `scripts/fetch_news.py`，在 `RSS_SOURCES` 中添加：

```python
{
    'name': '你的新闻源名称',
    'url': 'RSS地址',
    'enabled': True
}
```

---

### 3. 自定义 AI 提示词

编辑 `scripts/ai_summary.py`，修改 `prompt` 变量：

```python
prompt = f"""你的自定义提示词...

原始新闻：
{news_text}
"""
```

---

### 4. 修改文章模板

编辑 `scripts/ai_summary.py` 中的 `generate_hexo_post` 函数。

---

## ❓ 常见问题

### Q1: 为什么文章没有生成？

**检查步骤**：
1. GitHub Actions 是否运行成功？（查看 Actions 页面）
2. API Key 是否正确配置？（检查 Secrets）
3. 查看运行日志，找到具体错误

---

### Q2: AI 总结失败怎么办？

如果 AI 总结失败，脚本会自动使用**备用方案**：
- 直接格式化新闻列表
- 不影响文章生成和发布

---

### Q3: 如何临时暂停自动发布？

**方法 1**：禁用工作流
1. 打开 GitHub 仓库
2. Actions → Daily News Summary
3. 点击右上角 "..." → Disable workflow

**方法 2**：注释掉定时配置
编辑 `.github/workflows/daily-news.yml`：

```yaml
# schedule:
#   - cron: '0 1 * * *'
```

---

### Q4: 成本多少？

**完全免费方案**（推荐）：
- RSS 抓取：免费
- 通义千问：免费（100万 tokens/月）
- GitHub Actions：免费
- **总成本**：$0/月 ✅

**付费方案**（更好效果）：
- DeepSeek：约 $0.15/月
- OpenAI：约 $1.5/月

---

### Q5: 如何手动生成文章？

**方法 1**：GitHub Actions 手动触发
1. Actions → Daily News Summary
2. Run workflow

**方法 2**：本地运行
```bash
# 安装依赖
pip install feedparser requests dashscope

# 运行脚本
python scripts/fetch_news.py
python scripts/ai_summary.py

# 查看生成的文章
cat source/_posts/$(date +%Y-%m-%d)-daily-international-news.md
```

---

## 📈 效果预览

生成的文章示例：

```markdown
---
title: 国际新闻热点 2025-01-15
date: 2025-01-15 09:00:00
categories:
  - 国际新闻
tags:
  - 每日新闻
  - AI总结
---

## 1. 美联储维持利率不变...

## 2. 欧盟通过新AI监管法案...

...
```

---

## 🎉 完成！

配置完成后，你的博客将：
- ✅ 每天自动抓取国际新闻
- ✅ AI 智能总结重点内容
- ✅ 自动发布到博客
- ✅ 完全免费运行

**预计每月生成 30 篇高质量新闻文章** 🚀

---

## 📞 需要帮助？

如果遇到问题，欢迎联系：

- 📧 邮箱：runundersun@163.com
- 💬 微信：strive_qiang888
- 🐙 GitHub：https://github.com/xuzhengqiang

---

## 📄 相关文档

- [GitHub Actions 文档](https://docs.github.com/actions)
- [通义千问 API 文档](https://help.aliyun.com/zh/dashscope/)
- [RSS 标准说明](https://www.rssboard.org/rss-specification)
- [Hexo 文档](https://hexo.io/zh-cn/docs/)

