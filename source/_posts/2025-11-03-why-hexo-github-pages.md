---
title: 我为什么选择 Hexo + GitHub Pages 部署（优缺点与踩坑全记录）
date: 2025-11-03 22:20:00
tags:
  - Hexo
  - GitHub Pages
  - 博客搭建
categories:
  - 经验总结
---

> 一句话结论：Hexo 负责「把内容变成静态站点」，GitHub Pages 负责「把静态站点免费、稳定地发布到全球」。低成本、自动化、够快、够稳，是我选它们的核心理由。

## 我为什么选 Hexo + GitHub Pages

- **免费且稳定**：
  - GitHub Pages 免费托管 + 全球 CDN，个人博客足够用。
- **写作效率高**：
  - 全 Markdown 流程，Hexo 模板化写作，跑一条命令就能生成/预览。
- **主题生态成熟**：
  - 主题多、样式好看，像 Stun/Next/Butterfly 都是成熟之选。
- **自动化发布**：
  - 结合 GitHub Actions，每次 push 自动构建并发布到 gh-pages 分支。
- **可迁移性强**：
  - 全部是静态资源，换平台（如 Vercel/Netlify）成本很低。

## 和其它方案的对比

- **WordPress**：功能强但要服务器+数据库，维护/安全/备份成本更高。
- **Notion/语雀导出**：门槛低但样式与 SEO 可控性差；长远看不如自托管稳。
- **VitePress/Docusaurus**：更适合文档站，博客主题与生态没有 Hexo 丰富。

## 我的架构与发布流程

```text
本地写作（Markdown）
  → Hexo 生成静态站点（public/）
  → 推送到 GitHub（master 源码）
  → GitHub Actions 构建
  → 部署到 gh-pages 分支
  → https://xuzhengqiang.github.io/ 上线
```

- 主题：Stun（夜间模式、导航、SEO 友好）
- 自动化：`.github/workflows/deploy.yml`（push 即发布）

## 本次搭建的踩坑与解决

1. **_config.yml 的 YAML 语法报错**  
   - 表现：`YAMLException: can not read an implicit mapping pair`  
   - 原因：`url:` 后少空格或值里有冒号未加引号。  
   - 解决：`url: https://xuzhengqiang.github.io`，确保冒号后有空格，带特殊字符时用引号。

2. **菜单链接 404（/about/ 而不是 /my-hexo-blog/about/）**  
   - 原因：仓库最初用项目页路径，`root` 未设置或设置错误。  
   - 解决：改用用户名仓库 `xuzhengqiang.github.io`，并设置：
     ```yaml
     url: https://xuzhengqiang.github.io
     root: /
     ```

3. **GitHub Pages 仍 404**  
   - 原因：删除默认文章后没有任何文章，`index.html` 不会生成。  
   - 解决：至少保留一篇文章 → 重新 `hexo g`。

4. **Actions 成功但首页仍打不开**  
   - 排查顺序：
     1) Actions 日志是否绿色；  
     2) `gh-pages` 分支是否存在 `index.html`；  
     3) Settings → Pages 是否选中 `gh-pages` + `/ (root)`；  
     4) 等待 1~3 分钟缓存生效再访问。

5. **主题子模块/嵌套仓库问题**  
   - 表现：`themes/stun` 被当作子模块（160000）  
   - 解决：`git rm --cached -r themes/stun` 后重新 `git add themes/stun` 提交。

6. **国内网络 push/部署超时**  
   - 解决：配置 Git 代理：
     ```bash
     git config --global http.proxy  http://127.0.0.1:7890
     git config --global https.proxy http://127.0.0.1:7890
     # 或使用 SSH：repo 改为 git@github.com:xxx/xxx.git
     ```

## 我的最佳实践

- **分支职责清晰**：`master` 放源码，`gh-pages` 放构建产物。
- **最少可用内容**：至少保留 1 篇文章，避免无首页。
- **固定基础配置**：`url`/`root`/`theme`/`deploy` 一次设好，后续稳定迭代。
- **自动化优先**：用 Actions 部署，避免本地网络影响。
- **备份与可迁移**：源码常规推送，随时可迁移到 Vercel/Netlify。

## 清单（给未来的我）

- [ ] `url` 与 `root` 正确
- [ ] 至少 1 篇文章
- [ ] Pages 选择 `gh-pages` + `/ (root)`
- [ ] 主题不是子模块
- [ ] 代理/SSH 配好再推送

## 结语

Hexo + GitHub Pages 对个人博客是性价比极高的组合：成本近乎为零、自动化强、维护简单。把精力留给内容本身，才是持续输出的关键。希望这份记录能帮到后来者，也提醒未来的我少踩坑，多写作。

