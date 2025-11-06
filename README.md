# 我的 Hexo 博客

基于 Hexo + Stun 主题的个人技术博客

## 快速开始

### 本地开发

```bash
# 安装依赖
npm install

# 启动本地服务器
npm run server

# 生成静态文件
npm run build

# 清除缓存
npm run clean
```

### 部署

本项目支持部署到 **GitHub Pages** 和 **Vercel** 两个平台。

📖 **详细部署教程请查看**: [部署.md](./部署.md)

**快速部署：**

- **GitHub Pages**: 推送代码后自动部署
- **Vercel**: 导入 GitHub 仓库，一键部署

## 目录结构

```
.
├── _config.yml          # Hexo 站点配置文件
├── _config.stun.yml     # Stun 主题配置文件
├── package.json         # 项目依赖配置
├── vercel.json          # Vercel 部署配置
├── .env.example         # 环境变量配置示例
├── 部署.md              # 完整部署教程
├── .github/
│   └── workflows/
│       ├── deploy.yml       # GitHub Actions 自动部署
│       └── daily-news.yml   # 每日新闻自动化 ⭐
├── scripts/             # 自动化脚本 ⭐
│   ├── fetch_news.py   # 新闻抓取脚本
│   └── ai_summary.py   # AI 总结脚本
├── docs/                # 文档 ⭐
│   └── AUTO_NEWS_GUIDE.md  # 自动化新闻配置指南
├── scaffolds/           # 文章模板
│   ├── post.md         # 文章模板
│   ├── draft.md        # 草稿模板
│   └── page.md         # 页面模板
├── source/              # 源文件目录
│   ├── _posts/         # 博客文章（Markdown）
│   ├── about/          # 关于页面
│   ├── tags/           # 标签页面
│   └── categories/     # 分类页面
└── themes/             # 主题目录
    └── stun/           # Stun 主题文件
```

## 写作指南

### 创建文章

```bash
# 创建新文章
hexo new "文章标题"

# 创建草稿
hexo new draft "草稿标题"

# 发布草稿
hexo publish draft "草稿标题"

# 创建页面
hexo new page "页面名称"
```

### 文章格式

文章使用 Markdown 格式，支持以下 Front Matter：

```markdown
---
title: 文章标题
date: 2024-01-01 12:00:00
categories: 
  - 分类名
tags:
  - 标签1
  - 标签2
description: 文章描述
---

文章内容...
```

### 本地预览

```bash
# 清除缓存
hexo clean

# 启动本地服务器
hexo server

# 访问 http://localhost:4000 预览
```

## 主题配置

当前使用 [Stun](https://github.com/liuyib/hexo-theme-stun) 主题

- **主题配置文件**: `_config.stun.yml`
- **主题文档**: https://github.com/liuyib/hexo-theme-stun
- **主题特性**: 响应式设计、夜间模式、代码高亮、SEO 优化

### 常用配置

```yaml
# 菜单配置
menu:
  home: / || fas fa-home
  archives: /archives/ || fas fa-folder-open
  categories: /categories/ || fas fa-layer-group
  tags: /tags/ || fas fa-tags
  about: /about/ || fas fa-user

# 夜间模式
night_mode:
  enable: true
```

## 站点信息

- **标题**: 知行合一,善始善终
- **副标题**: 分享技术,记录成长
- **描述**: 专注前端/后端开发
- **作者**: 大先生
- **语言**: 简体中文

## 技术栈

- **静态站点生成器**: [Hexo 7.3.0](https://hexo.io/)
- **主题**: [Stun](https://github.com/liuyib/hexo-theme-stun)
- **部署平台**: GitHub Pages / Vercel
- **版本控制**: Git / GitHub

## 部署状态

### GitHub Pages
- ✅ GitHub Actions 配置已完成
- ✅ 自动部署到 `gh-pages` 分支
- 📝 推送到 `master` 分支自动触发部署

### Vercel
- ✅ Vercel 配置文件已完成
- ✅ 支持自动部署
- 📝 导入 GitHub 仓库即可使用

## 相关链接

- 📖 [部署教程](./部署.md) - 完整的 GitHub Pages 和 Vercel 部署指南
- 📝 [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
- 🎨 [Stun 主题文档](https://github.com/liuyib/hexo-theme-stun)
- 🚀 [Vercel 文档](https://vercel.com/docs)
- 📄 [GitHub Pages 文档](https://docs.github.com/pages)

## 常见问题

### 如何开始写作？

```bash
# 创建新文章
hexo new "我的第一篇博客"

# 本地预览
hexo server

# 提交并推送（自动部署）
git add .
git commit -m "新增文章"
git push
```

### 如何修改主题样式？

编辑 `_config.stun.yml` 文件，修改主题配置，然后推送即可。

### 如何添加自定义域名？

详见 [部署.md](./部署.md) 中的"自定义域名"章节。

## 🤖 自动化功能

### 每日国际新闻自动发布 ⭐ NEW

本项目集成了**自动抓取国际新闻 + AI 总结 + 自动发布**功能：

- ✅ **多源抓取**：BBC、CNN、Reuters、Google News 等主流媒体
- ✅ **AI 智能总结**：支持通义千问（免费）、OpenAI、DeepSeek
- ✅ **全自动发布**：每天早上 9 点自动生成并发布文章
- ✅ **完全免费**：使用免费 RSS + 免费 AI 服务
- ✅ **零维护**：配置一次，自动运行

**快速开始**：

1. 申请免费 AI API Key（通义千问推荐）
2. 在 GitHub Secrets 中配置 `QWEN_API_KEY`
3. 完成！每天自动发布一篇新闻汇总

📖 **详细教程**：[自动化新闻配置指南](./docs/AUTO_NEWS_GUIDE.md)

---

## 项目改进建议

### 已完成 ✅
- [x] 完整的部署文档（GitHub Pages + Vercel）
- [x] GitHub Actions 自动部署配置
- [x] Vercel 部署配置
- [x] 项目结构说明
- [x] 写作指南
- [x] 常见问题解答
- [x] **每日国际新闻自动化系统** ⭐ NEW

### 可选增强功能 💡
- [ ] 添加评论系统（Gitalk / Valine / Waline）
- [ ] 集成搜索功能（Algolia / 本地搜索）
- [ ] 添加网站统计（Google Analytics / 百度统计）
- [ ] 配置 RSS 订阅
- [ ] 添加站点地图（SEO 优化）
- [ ] 图片懒加载优化
- [ ] 代码块复制按钮
- [ ] 文章阅读时长统计
- [ ] 文章字数统计
- [ ] 相关文章推荐

### 内容建议 📝
- [ ] 完善"关于"页面
- [ ] 添加友情链接页面
- [ ] 创建项目展示页面
- [ ] 编写第一篇技术文章
- [ ] 设置文章分类体系
- [ ] 规划标签使用规范

## License

MIT

