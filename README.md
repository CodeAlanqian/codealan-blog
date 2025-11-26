# CodeAlan Blog

个人技术 / 学习 / 学术主页，使用 Hugo 搭建并部署在 `codealan.top` 上，主要记录具身智能、VLN、ROS、Docker 等方向的笔记与实践。

## 技术栈与结构

- 静态站点框架：Hugo Extended（主题：`themes/simple` 自研定制）。  
- 内容组织：  
  - `content/academic/_index.md`：学术主页（中英版 Profile、研究兴趣、教育经历、项目与方向、B 站代表视频）。  
  - `content/obsidian/`：从 Obsidian 同步的各类笔记（VLN / ROS_NOTE / Docker / Ubuntu / Latex / Zotero / Other 等）。  
  - `content/posts/`：常规博文与 Demo（例如 PDF 引用示例）。  
   - `content/notes/_index.md`：运维与环境备忘（常用命令速查 + Bug&Pitfall 记事本）。  
  - `content/search/_index.md`、`content/archives/_index.md`：搜索页与归档页。  
- 构建入口：  
  - `build.sh`：调用 `hugo` 生成静态文件到 `public/`。  
  - `preview.sh`：本地预览。  
  - `sync-from-onedrive.sh`：从 OneDrive 目录同步 `content/` 和 `static/`（可选）。  

## 前端功能（主题 simple）

- 阅读体验：  
  - 顶部阅读进度条、回到顶部按钮。  
  - 自动目录（TOC）和当前小节高亮。  
  - PPT 式阅读模式：将文章按 `h2/h3` 切分成幻灯片，支持键盘切换。  
  - 代码块：语言徽标、复制按钮、横向滚动、移动端适配；不再折叠长代码。  
  - PDF 链接自动加标记与新窗口打开。  
- 搜索：  
  - `/search/` 页面基于预生成 JSON 数据在前端搜索。  
  - 支持按标题 / 标签 / 摘要模糊查询，并按相关度 + 时间排序。  
- 标签与颜色：  
  - 标签统一使用 `data-tag-key`，根据领域自动上色（如 `vln` / `ros` / `docker` / `rl` / `llm` / `ubuntu` / `latex` / `habitat` 等）。  
  - 搜索结果页和文章卡片中的标签颜色保持一致。  

## 个人 AI 助手（DeepSeek 代理）

- 后端：  
  - 根目录下 `ai_server.py` 使用 FastAPI + httpx 实现一个轻量代理服务，暴露接口：`POST /api/ai/chat`。  
  - 通过环境变量 `DEEPSEEK_API_KEY` 读取 DeepSeek 的 API Key（不写入仓库，不在前端暴露）。  
  - 请求转发到 `https://api.deepseek.com/v1/chat/completions`，使用 `deepseek-chat` 模型，兼容 OpenAI 风格。  
- 前端：  
  - 在所有页面右下角提供一个「个人 AI 助手」浮动按钮，点击展开聊天面板。  
  - 面板支持多轮对话，默认向后端发送当前会话的所有 `messages`。  
  - 对于调用失败，会在面板内显示友好的错误提示，不影响页面其它功能。  
- 启动示例：  
  ```bash
  # 安装依赖（建议使用虚拟环境）
  pip install fastapi uvicorn httpx

  # 配置环境变量（请使用你自己的 Key）
  export DEEPSEEK_API_KEY="your_deepseek_api_key"

  # 启动本地代理服务
  python ai_server.py  # 默认监听 127.0.0.1:9000
  ```  
  然后在 Nginx 中将 `/api/ai/` 转发到 `127.0.0.1:9000` 即可在正式站点使用。  

## 部署与 Nginx（摘要）

> 详细部署过程参考服务器上的 Nginx 配置与 `agentdone.md`。

- Hugo 构建输出目录：`public/`。  
- Nginx 静态站点：  
  - 通过 8444 端口提供 HTTPS 后端（`root /home/ubuntu/mypage/public`）。  
  - 使用 acme.sh 申请的 Let’s Encrypt 证书（`/etc/nginx/ssl/codealan.top/`）。  
- 443 端口复用：  
  - 通过 `stream` 模块按 SNI 分流：  
    - `codealan.top` / `www.codealan.top` → 8444 (blog)。  
    - `aws.amazon.com` → 8443 (VLESS-Reality / sui)。  

## 本地开发与构建

```bash
# 安装 Hugo Extended 后
./build.sh      # 生成静态站点到 public/
./preview.sh    # 本地预览（如果有配置）
```

常见路径说明：

- 内容：`content/`  
- 静态资源：`static/`（例如 `static/obsidian/` 下的图片、附件）  
- 构建产物：`public/`（已通过 `.gitignore` 忽略，不进入仓库）  

## Git 仓库与大文件策略

- 仓库地址：`https://github.com/CodeAlanqian/codealan-blog.git`，默认分支：`master`。  
- 忽略规则：  
  - 忽略 Hugo 构建产物与锁文件：`public/`、`.hugo_build.lock`。  
  - 忽略大文件与 PDF：`static/files/`、`static/**/*.pdf`、`content/**/*.pdf`、`public/**/*.pdf`。  
- 历史清理：  
  - 早期提交曾包含 VLN 讲义、项目 PDF 以及 `public/` 下的大文件，收到 GitHub 大文件警告后，已重建 git 历史，仅保留“干净”的初始提交，并强制推送覆盖远程历史。  
  - 现在仓库只跟踪源码和内容，不再保存构建结果或大体积资产。  

## 学术主页（/academic/）

`content/academic/_index.md` 作为统一的学术主页，包含：

- English Profile：基本信息、研究兴趣、Preprints & Publications（占位）、教育经历、项目与实践、正在进行的方向、Contact。  
- 中文简介：学术简介、研究兴趣、教育经历、项目与实践、正在进行的方向、联系方式。  
- B 站代表视频：嵌入 5 个代表视频播放器。  

页尾附有一句站点说明：

> 本站记录我的技术笔记、想法与实践，写作工具是 Obsidian，发布用 Hugo。
