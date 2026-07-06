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
    - 新增文件站点 `file.codealan.top`：由 Nginx `http` 块监听 8445，TLS 终止后反代到本地 `127.0.0.1:8888`。  
    - 新增 `/etc/nginx/stream.conf`，启用 `stream` 层 SNI 分流 443。  
    - 更新 `/etc/nginx/nginx.conf`，在文件末尾 `include /etc/nginx/stream.conf;`。  
  - stream 分流规则（443 TCP）：  
    ```nginx
    stream {
        map $ssl_preread_server_name $backend {
            aws.amazon.com     sui;
            codealan.top       web;
            www.codealan.top   web;
            file.codealan.top  file;
            nas.codealan.top   nas;
            default            web;
        }

        upstream web { server 127.0.0.1:8444; }
        upstream file { server 127.0.0.1:8445; }
        upstream nas { server 127.0.0.1:8446; }
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
  - 文件站点 8445 配置（同证书，可放入同一站点文件中）：  
    ```nginx
    server {
        listen 8445 ssl http2;
        listen [::]:8445 ssl http2;
        server_name file.codealan.top;
        ssl_certificate     /etc/nginx/ssl/codealan.top/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/codealan.top/privkey.pem;

        location / {
            proxy_pass http://127.0.0.1:8888;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
  - 分流逻辑：  
    - 客户端 SNI 为 `aws.amazon.com` → 转发到 `127.0.0.1:8443`（sui）。  
    - SNI 为 `codealan.top` / `www.codealan.top` 或空/其他 → 转发到博客 8444。  
    - SNI 为 `file.codealan.top` → 转发到文件站点 8445（再反代到 `127.0.0.1:8888`）。  
    - SNI 为 `nas.codealan.top` → 转发到 NAS 站点 8446（再反代到 `127.0.0.1:5666`）。
  - 重启验证：`nginx -t` 通过，`curl -k https://127.0.0.1` 返回 200（博客），80 返回 301 到 HTTPS。  
  - 证书补充：若新增 `file.codealan.top`，需要重新签发或扩展证书包含该域名（acme.sh `--issue -d codealan.top -d www.codealan.top -d file.codealan.top`）。  

使用说明（客户端侧）  
- 博客：`https://codealan.top/` 正常访问。  
- 文件站点：`https://file.codealan.top/` 访问后由 Nginx 反代到 `http://127.0.0.1:8888`。  
- NAS 站点：`https://nas.codealan.top/` 访问后由 Nginx 反代到 `http://127.0.0.1:5666`。
- VLESS-Reality：保持 SNI=`aws.amazon.com`，连接 `43.156.100.159:443`，将流量经 stream 分流到本地 `127.0.0.1:8443` 的 sui。  

- NAS 站点 Nginx 配置建议（2026-07-06）
  - 目标：将 `nas.codealan.top` 接入现有 443 SNI 分流，后端服务端口为本机 `5666`。
  - 约定：按仓库规则，不直接写入 `/etc/nginx/...` 系统文件；以下为需要加入服务器 Nginx 配置的片段。
  - `/etc/nginx/sites-available/codealan.top` 的 80 端口 `server_name` 增加 `nas.codealan.top`，用于 ACME HTTP-01 与 HTTP 到 HTTPS 跳转：
    ```nginx
    server_name codealan.top www.codealan.top file.codealan.top nas.codealan.top;
    ```
  - 同一站点文件新增内部 HTTPS 后端。这里使用 `8446`，避免和已有博客 `8444`、文件站 `8445` 冲突：
    ```nginx
    server {
        listen 8446 ssl;
        listen [::]:8446 ssl;
        server_name nas.codealan.top;

        client_max_body_size 0;

        ssl_certificate     /etc/nginx/ssl/codealan.top/fullchain.cer;
        ssl_certificate_key /etc/nginx/ssl/codealan.top/codealan.top.key;
        ssl_protocols       TLSv1.2 TLSv1.3;
        ssl_ciphers         HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://127.0.0.1:5666;
            proxy_http_version 1.1;
            proxy_request_buffering off;

            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_read_timeout 3600s;
            proxy_send_timeout 3600s;
        }
    }
    ```
  - `/etc/nginx/stream.conf` 中增加 SNI 映射和 upstream：
    ```nginx
    map $ssl_preread_server_name $backend {
        aws.amazon.com      sui;
        codealan.top        web;
        www.codealan.top    web;
        file.codealan.top   file;
        nas.codealan.top    nas;
        default             web;
    }

    upstream nas {
        server 127.0.0.1:8446;
    }
    ```
  - 证书需包含 `nas.codealan.top`。如果当前证书不包含该域名，可重新签发/扩展证书后复制到现有路径：
    ```bash
    /home/ubuntu/.acme.sh/acme.sh --issue --force \
      -d codealan.top -d www.codealan.top -d file.codealan.top -d nas.codealan.top \
      -w /var/www/letsencrypt --server letsencrypt

    sudo cp ~/.acme.sh/codealan.top_ecc/fullchain.cer /etc/nginx/ssl/codealan.top/fullchain.cer
    sudo cp ~/.acme.sh/codealan.top_ecc/codealan.top.key /etc/nginx/ssl/codealan.top/codealan.top.key
    ```
  - 校验与重载：
    ```bash
    sudo nginx -t
    sudo systemctl reload nginx
    curl -k -I https://nas.codealan.top/
    ```

- 文件站点改为 Copyparty（2026-06-21）
  - 目标：将 `file.codealan.top` 后端从旧的 `file-transfer-go` 切换为 Docker 部署的 Copyparty，支持网页文件浏览、上传和在线播放/下载。
  - 新增文件：
    - `docker-compose.copyparty.yml`：使用 `ghcr.io/9001/copyparty-ac:latest`，容器名 `copyparty-file`，仅绑定 `127.0.0.1:8888:3923`。
    - `start_copyparty.sh`：读取 `copyparty/.env` 并执行 `docker compose --env-file ... up -d`。
    - `copyparty/.env.example`：仅提供变量模板；真实 `copyparty/.env` 被 `.gitignore` 忽略。
  - 持久化：
    - 文件目录：`copyparty/files/` → 容器 `/w`。
    - 状态目录：`copyparty/state/` → 容器 `/cfg/copyparty`。
  - 权限：
    - `-v /w::rwmda,admin`：仅 `admin` 用户可浏览、下载、上传、移动、删除；匿名用户无访问权限。
    - `--usernames`：登录时要求用户名 + 密码。
  - 反代头处理：
    - 初版只信任 `127.0.0.1/32,::1/128`，但 Nginx 访问容器时源地址表现为 Docker 网桥 `172.19.0.1`，导致 Copyparty 忽略 `X-Forwarded-Proto: https`。
    - 登录 POST 因此被误判为 `https://file.codealan.top` Origin 对 `http://file.codealan.top` 请求，触发 `rejected by cors-check`。
    - 已改为 `--xff-src lan` 并增加 `--xf-proto-fb https`，让 Copyparty 正确识别反代后的外部协议。
  - 上传分片：
    - 线上 Nginx 系统配置暂未写入 `client_max_body_size 0;`，默认请求体限制会导致 Copyparty 默认上传分片触发 `413 Request Entity Too Large`。
    - Copyparty 的 `--u2sz` 只接受整数 MiB，无法稳定降到 Nginx 默认 1MiB 以下；因此这个问题必须在 Nginx 层修复。
    - 长期方案是在 `file.codealan.top` 的 Nginx server/location 中设置 `client_max_body_size 0;` 和 `proxy_request_buffering off;`。
  - 上传性能：
    - 开启 `--turbo 2`，让 Web 客户端默认启用 turbo 上传模式。
    - 设置 `--u2j 6`，将浏览器并发上传任务从默认 2 提高到 6。
    - 设置 `--u2sz 8,16,64`，让上传 POST 分片默认 16MiB，最大 64MiB，减少小分片往返开销。
  - 切换过程：
    - 旧容器 `file-transfer-go` 占用 `0.0.0.0:8888->8080`，且无宿主机挂载；已停止但未删除，便于回滚。
    - 拉取镜像 `ghcr.io/9001/copyparty-ac:latest`，当前容器 `copyparty-file` 已启动。
  - 验证：
    - `docker ps` 显示 `copyparty-file` 运行中，端口为 `127.0.0.1:8888->3923/tcp`。
    - `curl -I http://127.0.0.1:8888/` 返回 `HTTP/1.1 200 OK`。
    - `curl -k -I https://file.codealan.top/` 返回 `HTTP/2 200`。
    - 浏览器 UA 访问 `https://file.codealan.top/` 返回 Copyparty HTML，页面标题为 `CodeAlan Files`。
  - Nginx 备注：
    - 当前站点文件已存在 `file.codealan.top` 的 8445 HTTPS 反代到 `127.0.0.1:8888`。
    - 为支持视频等大文件上传，建议在 `file.codealan.top` 的 `server` 或 `location /` 中加入：
      ```nginx
      client_max_body_size 0;
      proxy_request_buffering off;
      proxy_read_timeout 3600s;
      proxy_send_timeout 3600s;
      ```
    - 按仓库约定，本次未直接写入 `/etc/nginx/...` 系统文件。
  - 回滚：
    - 停止 Copyparty：`docker compose --env-file copyparty/.env -f docker-compose.copyparty.yml down`。
    - 恢复旧容器：`docker start file-transfer-go`。

主要命令（摘要）
- 安装 Hugo：`wget -O /tmp/hugo.tar.gz https://github.com/gohugoio/hugo/releases/download/v0.124.1/hugo_extended_0.124.1_Linux-amd64.tar.gz`，`tar -xzf /tmp/hugo.tar.gz -C /tmp/hugo && install -m 755 /tmp/hugo/hugo ~/.local/bin/hugo`
- 同步/构建/预览脚本：`chmod +x sync-from-onedrive.sh build.sh preview.sh`，`./sync-from-onedrive.sh`，`./build.sh`，`./preview.sh`
- Copyparty 文件站：`cp copyparty/.env.example copyparty/.env`，设置 `COPYPARTY_ADMIN_PASSWORD`，然后运行 `./start_copyparty.sh`
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
  - 副标题更新为：`记录 UAV / 具身智能 / VLN 的学习与实践。`（`config.yaml: params.description`）。  
  - 作者统一为 `CodeAlan`（`config.yaml: params.author`），用于 footer 与元信息。  
  - 在文章顶部日期后显示“更新于 YYYY-MM-DD”，基于 Hugo 的 `.Lastmod` 字段，仅当 `lastmod` 与 `date` 不同时显示。  
  - 顶部导航栏透明度调优至约 30%，在亮色/暗色模式下使用不同的半透明背景，同时保持模糊效果。  
  - SEO：meta description 优先取页面描述/摘要，列表页拼接分区标题与站点简介，短描述自动补全避免重复。  
  - IndexNow：新增 `static/7f54f8a7d94e4384a39ac2db05dfd452.txt`，用于 Bing 验证与快速收录。  
  - IndexNow 提交：新增 `scripts/indexnow_submit.py`，从 `public/sitemap.xml` 读取 URL 并 POST 到 `https://api.indexnow.org/IndexNow`。  

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

- 标签知识图谱（/tags/）  
  - 在标签聚合页模板 `themes/simple/layouts/_default/terms.html` 中，基于全部文章的标签统计与共现关系构建简单图数据：  
    - 统计每个标签出现次数，计算标签对在同一篇文章中同时出现的次数作为“边权”。  
    - 取出现频率较高的前若干个标签（上限 14 个）作为节点，以共现为边构建图。  
  - 在前端使用原生 SVG + 简易物理引擎绘制“标签知识图谱”：  
    - 节点按标签名分配不同颜色与大小（频率越高越大），边颜色也根据端点组合映射，使连接关系更易区分。  
    - 使用简单的力导向布局（斥力 + 弹簧 + 居中力 + 阻尼），尽量让节点分散、标签不互相遮挡。  
    - 支持桌面端鼠标拖动、移动端触控拖动（使用 `touchstart/touchmove/touchend`，并通过 `passive: false` + `preventDefault` 避免滚动冲突）。  
  - 样式定义在 `themes/simple/assets/css/main.css` 中的 `.tag-graph*` 相关类，包括卡片风格、SVG 宽度、自适应等。  

- 个人 AI 助手（DeepSeek API 代理）  
  - 需求：在博客中加入一个“个人 AI”辅助问答入口，但不能在前端暴露任何 API Key，同时能统计所有用户的文章浏览量。  
  - 后端实现：  
    - 在仓库根目录新增 `blog_server.py`（原 `ai_server.py`），使用 FastAPI + httpx 构建轻量后端服务：  
      - 暴露 `POST /api/ai/chat`，请求体为 `{"messages": [{"role": "user"/"assistant"/"system", "content": "..."}]}`。  
      - 暴露 `POST /api/views/hit?path=/xxx/`，按文章路径在本地 SQLite 数据库 `views.db` 中累加全站浏览量，并返回最新总数。  
      - 服务端优先通过环境变量 `DEEPSEEK_API_KEY` 读取 DeepSeek Key，若未配置则尝试从项目根目录 `.env` 文件中解析同名变量。  
      - `.env` 示例见 `.env.example`，真实 `.env` 文件已通过 `.gitignore` 忽略，不会进入仓库。  
      - 若找到 Key，则转发到 `https://api.deepseek.com/v1/chat/completions`。  
      - 默认使用 `deepseek-chat` 模型，参数包含 `temperature`、`max_tokens` 等，返回首个 `choices[0].message.content` 作为 `reply`。  
      - 对网络错误或 DeepSeek 返回的错误状态进行捕获，转为 HTTP 5xx/502 错误，便于前端提示。  
      - 在调用前构造了一个较详细的 `system` prompt，简要描述站点结构（学术页、备忘页、标签知识图谱等）、作者研究方向与项目背景，以及回答风格：  
        - 自动跟随用户语言（中/英）。  
        - 偏向技术、工程化和命令示例的回答方式。  
        - 不捏造未描述的私人经历，对不确定部分明确说明并给出验证建议。  
    - 启动方式示例：  
      - `pip install fastapi uvicorn httpx`  
      - 在根目录创建 `.env`，写入 `DEEPSEEK_API_KEY=your_deepseek_api_key`（或直接导出环境变量）。  
      - `python blog_server.py` 或 `uvicorn blog_server:app --host 127.0.0.1 --port 9000`。  
    - 部署建议：在 Nginx 中增加反向代理，将 `/api/` 前缀转发到本机 9000 端口，确保浏览器始终只与同源接口交互（AI 与浏览量接口共用同一路由前缀）。  
  - 为运维方便，新增 `start_backend.sh`（原 `start_ai.sh`）：  
      - 启动前会查找并优雅关闭已有的 `blog_server.py` 进程（先 `SIGTERM`，必要时 `SIGKILL`），再以 `nohup python blog_server.py >> backend.log 2>&1 &` 方式后台重启。  
      - 自动从 `.env` 中读取需要的环境变量。  
      - 日志统一写入 `backend.log`，该文件已在 `.gitignore` 中忽略。  
  - 前端集成：  
    - 在 `themes/simple/layouts/partials/ai-chat.html` 中定义浮动聊天组件：  
      - 右下角悬浮按钮（带「🤖 AI」字样），点击后弹出小型聊天面板。  
      - 面板内包含对话区、输入框与发送按钮，支持多轮对话展示。  
      - 在全局模板 `themes/simple/layouts/_default/baseof.html` 中引入该 partial，并添加前端逻辑：  
      - 维护简单的 `history` 数组保存当前会话的 role/content 列表。  
      - 发送时根据环境自动选择调用地址：  
        - 本地预览（`localhost/127.0.0.1/0.0.0.0`）时，直接请求 `http://127.0.0.1:9000/api/ai/chat`。  
        - 正式站点（`codealan.top`）时，请求 `/api/ai/chat`，由 Nginx 反向代理到本机 9000 端口。  
      - 后端允许 `http://localhost:1313` 等来源（CORS）访问，便于本地开发调试。  
      - 对响应中的 `reply` 追加到对话区，失败时在面板内显示错误提示而不打断其他功能。  
      - 支持 `Enter` 发送、`Shift+Enter` 换行，并有“思考中…”状态提示。  
    - 浏览量展示：  
      - 在文章模板 `themes/simple/layouts/_default/single.html` 中，在标题下方加入浏览量区域：`👀 <span class="view-count" data-key="{{ .RelPermalink }}">0</span> 次浏览`。  
      - 在全局脚本（`baseof.html` 底部）中新增逻辑：优先调用 `/api/views/hit?path={{ .RelPermalink }}` 更新全站累积浏览量；若调用失败，则退回到浏览器 `localStorage` 本地统计，以保证在后端不可用时仍能显示一个递增数字。  
    - 展示与样式：  
      - 在 `themes/simple/layouts/_default/baseof.html` 中实现了一个轻量级 Markdown 渲染器，用于在 AI 回复中支持：  
        - 标题（`#` 开头）、无序列表（`-` / `*`）、行内代码 `` `code` ``、代码块 ```lang```、粗体 `**text**` / `__text__`、超链接 `[text](url)` 等。  
        - 所有用户输入先进行 HTML 转义，AI 回复则按上述规则解析为安全的 HTML 片段插入气泡。  
      - 在 `themes/simple/assets/css/main.css` 中增加 `.ai-chat-*` 以及 `ai-chat-bubble` 内部元素的样式：  
        - 段落、列表、代码块与行内代码均使用与站点其他代码块一致的字体与背景，保证阅读体验统一。  
      - 在 `themes/simple/assets/css/main.css` 中增加 `.ai-chat-*` 类，统一圆角卡片、阴影、字体大小，使其与整体主题风格一致。  
      - 保证与右下角“回到顶部”按钮不重叠，在移动端下自动缩放宽度以适配窄屏。  
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
