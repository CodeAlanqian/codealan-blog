- 安装与站点搭建  
  - 安装 Hugo Extended（本地二进制 `~/.local/bin/hugo`），如需手动加入 PATH：`export PATH="$HOME/.local/bin:$PATH"`。  
  - 初始化 Hugo 站点，创建自定义轻量主题 `themes/simple`，配置 `config.yaml`；示例内容：`content/_index.md`、`content/about.md`、`content/posts/hello/index.md`。  
  - 添加脚本：`sync-from-onedrive.sh`（默认 `~/onedrive`，可用 `ONEDRIVE_PATH` 覆盖）、`build.sh`、`preview.sh`。  
  - 已运行同步脚本（提示 OneDrive 下 `content/static` 不存在，需在 OneDrive 创建后再同步）；已构建一次，产物在 `public/`。  

- Nginx 与证书（初始 HTTPS）  
  - 新建并启用 `/etc/nginx/sites-available/codealan.top`：80 仅 ACME + 301 到 HTTPS；443 提供静态站，根 `/home/ubuntu/mypage/public`，独立日志。  
  - 使用 acme.sh 申请 Let’s Encrypt（codealan.top/www.codealan.top，HTTP-01），证书与私钥位于 `/etc/nginx/ssl/codealan.top/fullchain.pem` 与 `/etc/nginx/ssl/codealan.top/privkey.pem`，并重载生效。  

- 443 端口复用与修改缘由  
  - 需求：保持 443 同时服务博客与 VLESS-Reality（sui），而不再占用额外端口。  
  - 调整：  
    - 博客 HTTPS 后端改为内部 8444（同一证书），由 Nginx `http` 块监听 8444 提供内容。  
    - 新增 `/etc/nginx/stream.conf`，启用 `stream` 层 SNI 分流 443。  
    - 更新 `/etc/nginx/nginx.conf`，在文件末尾 `include /etc/nginx/stream.conf;`。  
  - stream 分流规则（443 TCP）：  
    ```nginx
    stream {
        map $ssl_preread_server_name $backend {
            aws.amazon.com     sui;
            codealan.top       web;
            www.codealan.top   web;
            default            web;
        }

        upstream web { server 127.0.0.1:8444; }
        upstream sui { server 127.0.0.1:8443; }

        server {
            listen 443 reuseport;
            listen [::]:443 reuseport;
            proxy_pass $backend;
            ssl_preread on;
        }
    }
    ```
  - 博客后端 8444 配置（`/etc/nginx/sites-available/codealan.top`）：  
    ```nginx
    server {
        listen 80;
        listen [::]:80;
        server_name codealan.top www.codealan.top;
        location /.well-known/acme-challenge/ { alias /var/www/letsencrypt/.well-known/acme-challenge/; }
        location / { return 301 https://$host$request_uri; }
    }

    server {
        listen 8444 ssl http2;
        listen [::]:8444 ssl http2;
        server_name codealan.top www.codealan.top;
        root /home/ubuntu/mypage/public;
        ssl_certificate     /etc/nginx/ssl/codealan.top/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/codealan.top/privkey.pem;
        location / { try_files $uri $uri/ =404; }
    }
    ```
  - 分流逻辑：  
    - 客户端 SNI 为 `aws.amazon.com` → 转发到 `127.0.0.1:8443`（sui）。  
    - SNI 为 `codealan.top` / `www.codealan.top` 或空/其他 → 转发到博客 8444。  
  - 重启验证：`nginx -t` 通过，`curl -k https://127.0.0.1` 返回 200（博客），80 返回 301 到 HTTPS。  

使用说明（客户端侧）  
- 博客：`https://codealan.top/` 正常访问。  
- VLESS-Reality：保持 SNI=`aws.amazon.com`，连接 `43.156.100.159:443`，将流量经 stream 分流到本地 `127.0.0.1:8443` 的 sui。  

主要命令（摘要）
- 安装 Hugo：`wget -O /tmp/hugo.tar.gz https://github.com/gohugoio/hugo/releases/download/v0.124.1/hugo_extended_0.124.1_Linux-amd64.tar.gz`，`tar -xzf /tmp/hugo.tar.gz -C /tmp/hugo && install -m 755 /tmp/hugo/hugo ~/.local/bin/hugo`
- 同步/构建/预览脚本：`chmod +x sync-from-onedrive.sh build.sh preview.sh`，`./sync-from-onedrive.sh`，`./build.sh`，`./preview.sh`
- Nginx 站点/日志：`sudo tee /etc/nginx/sites-available/codealan.top ...`，`sudo ln -sf /etc/nginx/sites-available/codealan.top /etc/nginx/sites-enabled/`
- 证书申请：`/home/ubuntu/.acme.sh/acme.sh --register-account -m codealan@qq.com --server letsencrypt`，`/home/ubuntu/.acme.sh/acme.sh --issue -d codealan.top -d www.codealan.top -w /var/www/letsencrypt`，证书复制：`sudo cp ~/.acme.sh/codealan.top_ecc/{codealan.top.key,fullchain.cer} /etc/nginx/ssl/codealan.top/`
- Nginx 检查/重载：`sudo nginx -t`，`sudo systemctl reload nginx`（或 restart）
- Stream 分流：`sudo tee /etc/nginx/stream.conf ...`，`sudo tee /etc/nginx/nginx.conf ...`（增加 `include /etc/nginx/stream.conf;`），`sudo systemctl restart nginx`

---

## Hugo 主题与前端功能改动汇总

- 代码展示与交互  
  - 自定义 `code-block` 包装 `<pre>`，统一样式、复制按钮、滚动条，所有代码块默认完全展开显示（不再折叠长代码）。  
  - 使用 Hugo Chroma + GitHub 风格高亮，支持浅色/深色不同配色。  

- 文章阅读体验  
  - 文章顶部加入阅读进度条（根据 `.post` 高度实时更新）。  
  - 使用 `.TableOfContents` 生成目录，桌面端浮动在页面右侧并随滚动高亮当前小节；移动端显示在正文前。  
  - 文章标题下显示“约 X 分钟阅读 · Y 字”（基于 `.ReadingTime` 和 `.WordCount`）。  
  - 在文章底部增加上一篇/下一篇导航，以及“复制本页链接”按钮。  
  - 浏览量（本地统计）：在标题下方显示“👁 N 次浏览”，按文章路径用 `localStorage` 记录。  

- 图片与数学公式  
  - 为正文图片增加点击放大（lightbox）效果，支持点击空白或 Esc 关闭。  
  - 图片统一添加 `loading="lazy"`（通过模板 `replaceRE`），减轻首屏压力。  
  - KaTeX 按需加载：在 front matter 设置 `math: true` 的文章才加载 KaTeX 资源并渲染公式，添加了示例文章 `content/posts/math-demo/`。  

- 首页与导航  
  - 首页个人简介下新增标签筛选区：  
    - 首页展示的文章集合限定为 `posts` + `obsidian`。  
    - 顶部标签条改为跳转至对应标签页 `/tags/<tag>/`。  
  - 顶部导航栏改为半透明磨砂（浅色/深色分别使用 `rgba(..., 0.3)` 背景），保持 `position: sticky`。  
  - 在非首页右侧添加返回按钮：桌面端显示“← 返回”，移动端仅显示箭头以节省空间。  
  - 设置浏览器图标：使用 `static/avatar.png` 作为 favicon。  

- 标签、归档与搜索  
  - 标签总览页（`/tags/`）：`terms.html` 显示所有标签及文章数量。  
  - 单标签页（`/tags/<tag>/`）：`taxonomy.html` 显示该标签下所有文章和总数。  
  - 归档页（`/archives/`）：按年份分组列出 `posts` + `obsidian` 文章，显示日期与标题时间轴。  
  - 搜索页（`/search/`）：  
    - 在模板中嵌入所有文章（`posts` + `obsidian`）的标题、摘要、标签与日期数据。  
    - 前端使用多关键词模糊搜索（标题权重最高，其次标签、摘要），按相关度与时间排序。  
    - 默认显示最近文章，清空搜索时恢复列表，结果区域有轻微渐变过渡。  

- 目录和标题链接增强  
  - 目录右侧固定浮动时，使用 IntersectionObserver 实时高亮当前阅读小节。  
  - 为正文中的 `h2/h3/h4` 标题自动追加小型 `#` 锚点按钮，一键复制当前小节链接。  

- 404 页面与其它  
  - 自定义 404 页面：提示文案 + “返回首页”和“去搜索一下”按钮。  
  - 移动端适配：调整 `.site-header` 与 `.back-btn` 的布局和尺寸，确保返回按钮与菜单在小屏中不拥挤。  

使用提示：  
- 若某篇文章有公式，在 front matter 增加 `math: true` 即可启用 KaTeX。  
- 若不希望某张图片触发放大预览，可在 `img` 标签添加 `data-no-lightbox="true"`。  
- 搜索入口位于顶部导航“搜索”，支持按标题、标签和摘要关键字模糊检索。  

---

## 后续小改动与脚本补充

- 站点信息与视觉细节  
  - 副标题更新为：`记录具身智能、VLN 学习与开发折腾的日常。`（`config.yaml: params.description`）。  
  - 作者统一为 `CodeAlan`（`config.yaml: params.author`），用于 footer 与元信息。  
  - 在文章顶部日期后显示“更新于 YYYY-MM-DD”，基于 Hugo 的 `.Lastmod` 字段，仅当 `lastmod` 与 `date` 不同时显示。  
  - 顶部导航栏透明度调优至约 30%，在亮色/暗色模式下使用不同的半透明背景，同时保持模糊效果。  

- 标签与颜色规则  
  - 为标签元素增加 `data-tag-key` 属性（单篇与列表卡片中），用于 CSS 精细控制：  
    - `vln` → 蓝色；`ros` / `ros_note` → 绿色；`docker` → 蓝青；`rl` → 橙色；`llm` → 紫色；`obsidian` → 灰色。  
    - 后续扩展了更多标签配色：`ubuntu`、`essay`/`other`、`navigation`、`项目`/`project`、`深蓝课程`/`course`、`nextcloud`、`zotero`、`latex`、`habitat` 等。  
  - 所有文章保证至少有一个 tag：  
    - `scripts/fix_tags_vln.py`：确保 `content/obsidian/VLN/` 下所有 VLN 文章包含 `VLN` 标签。  
    - `scripts/autotag.py`：对 `content/` 下所有 Markdown 按路径和内容自动补充语义标签（Docker/ROS/VLN/深蓝课程/项目/Zotero/Latex/Other/Essay/ideas/RL/LLM/Habitat/Nextcloud 等），保留已有 tag 并截断到最多 6 个。  

- 时间与版本信息脚本  
  - `scripts/fix_lastmod.py`：  
    - 为 `content/` 下所有 Markdown 批量填充 `lastmod` 字段（若缺失），使用文件 mtime（YYYY-MM-DD）。  
    - 若 front matter 中已有 `date`，则在其后插入 `lastmod`；否则在 front matter 末尾追加。  

- PPT 式阅读模式  
  - 在文章底部增加 `PPT 式阅读` 按钮，点击后进入全屏幻灯片模式：  
    - 以 `h2/h3` 标题为分界，将正文划分为多页 slide；无标题时退化为单页。  
    - 键盘：`→/PageDown/Space` 下一页，`←/PageUp` 上一页，`Esc` 或“退出”按钮关闭。  
  - 样式：  
    - 亮色模式下使用浅色卡片（`var(--card)` + `var(--border)`），深色模式下恢复暗色背景。  
    - 移动端对 PPT overlay 做了适配：允许垂直滚动、缩小边距、调整底部操作区布局，保证小屏上可用。  

- 代码块语言标签  
  - 在前端 JS 中解析 `.code-block pre code` 的 `data-lang` 或 `language-xxx` class，为每个代码块自动插入左上角语言徽标（Python/Bash/C++ 等），样式由 `.code-lang` 控制。  

- 回到顶部按钮  
  - 在全局模板中添加右下角悬浮的 “↑” 按钮（`#backTopBtn`）：  
    - 滚动超过约 320px 自动淡入显示；点击使用平滑滚动回到页面顶部。  
    - 移动端缩小尺寸并调整位置，避免遮挡内容。  

- PDF 处理与示例  
  - 将站内 PDF 放在 `static/files/` 下，由 Hugo 映射为 `/files/...` 路径；修复示例文章中本地 PDF 链接，从 `/static/files/...` 改为 `/files/Attention%20Is%20All%20You%20Need.pdf`。  
  - 新增占位文件 `static/files/example.pdf` 与示例文章 `content/posts/pdf-demo/index.md`，说明如何正确引用站内 PDF。  
  - 在前端 JS 中对正文内以 `.pdf` 结尾的链接自动添加 `target="_blank" rel="noreferrer noopener"` 和 `pdf-link` 样式（右侧 PDF 徽标）。  
  - 自定义 `layouts/_default/_markup/render-link.html`，屏蔽 Zotero 导入的本地 `file://` 链接，避免构建时 URL 解析错误，并在 title 中提示“本地文件链接已在网页中禁用”。  

- 专栏（series）实验与回滚  
  - 曾短暂引入 `series` taxonomy 及 VLN 专栏：  
    - 使用 `scripts/fix_series_vln.py` 为 VLN 文件添加 `series: ["VLN课程"]`。  
    - 在单篇文章底部显示专栏目录块。  
  - 现已按需求完全回滚：  
  - `scripts/remove_series.py` 用于从所有 Markdown front matter 中移除 `series` 块。  
  - `config.yaml` 中去除 `series` taxonomy，模板中删除专栏相关展示。  

---

## 导航、搜索与学术页的后续调整

- 顶部导航与搜索  
  - 将主菜单中的“搜索”文本项替换为放大镜图标按钮，位于主题切换按钮之后，点击仍跳转 `/search/`。  
  - 为搜索图标添加统一的外框与悬浮样式，风格与主题切换按钮一致（圆角 + 边框 + hover 浮起）。  
  - 保持键盘快捷键 `/` 聚焦搜索输入框或跳转搜索页不变。  

- 移动端导航优化  
  - 多轮调优移动端 `.site-header` 的 `padding`、`gap` 与字体大小：  
    - 收窄导航栏高度（减小上下内边距）。  
    - 放大品牌标题与导航项字体，使小屏阅读更清晰。  
  - 统一移动端顶部三个控件的视觉大小：返回按钮箭头、主题切换图标、搜索图标在手机上大小一致（通过 font-size 与 span 选择器控制）。  
  - 最终保留“始终展开”的移动端菜单布局（未启用折叠菜单），保证简单直接。  

- 学术页与路由调整  
  - 将原来的 `关于` 页改造为“学术主页”，内容以学术信息为主：  
    - 英文部分：Academic Profile（基本信息、研究兴趣、Preprints & Publications 占位、教育经历、项目与实践、Ongoing Directions、Contact）。  
    - 中文部分：学术简介、研究兴趣、教育经历、项目与实践、正在进行的方向、联系方式。  
  - 在学术页顶部加入头像卡片（`/gyq.jpg`），作为学术 Profile 的视觉中心。  
  - 路由调整：  
    - 内容文件为 `content/academic/_index.md`，front matter 中声明 `url: "/academic/"`。  
    - `config.yaml` 菜单中“学术”指向 `/academic/`（不再使用 `/about/`）。  

- B 站代表视频区  
  - 在学术页底部新增“📺 我的 B 站代表视频”分区，并在标题前加分隔线 `---`。  
  - 嵌入 5 个 B 站播放器 `<iframe>`，统一样式：  
    - `width: 100%; height: 450px; margin-bottom: 1rem;`  
    - `frameborder="0"`, `border="0"`, `allowfullscreen="true"`, 并显式加入 `autoplay=0`。  

- 代码折叠行为更新  
  - 移除前端对长代码块自动折叠与“展开全部代码 / 收起代码”按钮的逻辑。  
  - 当前所有代码块始终完全展开，仅保留语言徽标和复制按钮，提高可复制性与可读性。  

- 搜索结果标签一致性  
  - 搜索页模板 `themes/simple/layouts/search/list.html` 中的标签输出添加 `data-tag-key` 属性，与列表/文章页统一。  
  - 搜索结果中的标签颜色规则与主站标签完全一致。  

- 标签知识图谱（/tags/）  
  - 在标签汇总页 `/tags/` 下方新增“标签知识图谱”模块：  
    - 后端收集 `posts` 与 `obsidian` 类型文章的标签，共现频率越高，连线越粗。  
    - 前端使用 SVG 实现简易力导向布局（force-directed graph）：  
      - 节点为标签，初始位置随机分布于中心附近。  
      - 标签节点之间存在斥力与连线的“弹簧”拉力，并叠加轻微的居中力与阻尼，使图逐步收敛。  
      - 节点可用鼠标拖拽，松开后布局会自动重新调整，整体观感类似 Obsidian 的知识图谱。  
    - 仅展示出现频率最高的一批标签（约 14 个），避免图过于拥挤。  

---

## Git 仓库与大文件处理

- Git 仓库初始化与远程  
  - 在 `/home/ubuntu/mypage` 目录初始化 git 仓库，配置：  
    - 用户名：`CodeAlan`  
    - 邮箱：`codealan@qq.com`  
  - 初始提交包含当前 Hugo 项目及 `public/` 构建产物。  
  - 远程仓库：`origin = https://github.com/CodeAlanqian/codealan-blog.git`，默认分支为 `master`。  

- `.gitignore` 配置  
  - 忽略 Hugo 构建锁与输出目录：  
    - `.hugo_build.lock`  
    - `public/`  
  - 忽略大文件与 PDF：  
    - `static/files/`  
    - `static/**/*.pdf`  
    - `content/**/*.pdf`  
    - `public/**/*.pdf`  
  - 目的：  
    - 防止将构建产物和课程/论文 PDF 等大文件提交到仓库。  
    - 避免触发 GitHub 对 >50MB 文件的警告。  

- 清理历史中的大文件（重建历史）  
  - 由于早期 commit 中已包含若干大 PDF（例如 VLN 课程讲义、项目 PDF 和 `public` 里的生成文件），GitHub 发出大文件警告。  
  - 为获得“干净”的历史，执行了以下步骤：  
    - 删除旧的 `.git` 目录，等价于重置本地 git 历史。  
    - 重新 `git init`、`git add .`（在新的 `.gitignore` 生效的前提下）。  
    - 创建新的 root commit：`Initial clean history import`，其中不再包含任何 `public/` 或 PDF 文件。  
  - 之后通过 `git push -f origin master` 覆盖远程 `master` 历史，GitHub 仓库的历史中不再包含大文件。  

> 当前推荐工作流：只提交源码与内容（`content/`、`layouts/`、`themes/`、脚本等），在服务器本地运行 `./build.sh` 生成 `public/` 用于 Nginx 部署；PDF 与其他大资产通过 `static/obsidian` 或外链管理，避免纳入 git 历史。  

---

## 运维备忘页（/notes/）

- 新增 `content/notes/_index.md`，作为“运维备忘 & 坑点记录”：  
  - **一页记：常用命令速查**  
    - Docker：查看容器/镜像、容器生命周期、清理无用资源等命令。  
    - tmux：会话管理、基础快捷键。  
    - Git：日常提交与简单回退操作。  
    - Nginx：配置检查、重载/重启与日志查看。  
    - acme.sh：证书列出、签发与续期示例。  
  - **Bug & Pitfall 记事本**  
    - Hugo / 静态资源：避免提交 `public/` 与大 PDF 的策略说明。  
    - Nginx / stream 分流：443 端口复用、`stream` + `ssl_preread` 使用要点。  
    - Docker / GPU 环境：`nvidia-smi` 检查与 `--gpus all` 示例。  
    - 终端 & tmux：字体与 locale 相关的显示问题记录。  

- 模板与样式  
  - 为 `notes` section 新增模板 `themes/simple/layouts/notes/list.html`：  
    - 使用与单篇文章一致的 `.post` + `.content` 布局。  
    - 同样对 `<pre>` 使用 `code-block` 包装，继承代码高亮、复制按钮等样式。  
  - 确保 `/notes/` 页面中的所有命令与配置片段都以标准 Markdown 代码块呈现，视觉与功能与普通文章保持一致。  
