## 使用 AI 助手改造博客的工作流说明（指令版）

本文档用于规范「我下达命令 → 你（AI 助手）在本仓库里动手 → 自动构建 → 自动提交 → 自动推送」这一整套流程。默认场景是：本地在 Codex CLI 中运行本项目，当前分支为 `master`，远端为 `origin`。

---

### 一、我如何下达指令

1. 在项目根目录打开 Codex CLI，会话上下文指向本仓库。  
2. 直接用自然语言描述需求，尽量具体：  
   - 例：  
     - 「给博客加一个服务端浏览量统计，要求构建后不会清零」  
     - 「把 AI 代理脚本统一改名成 blog_server，并更新启动脚本、Nginx 文档说明」  
     - 「修复首页 xxx 样式问题，并更新 README」  
3. 如果涉及部署 / Nginx / 系统脚本，说明期望：  
   - 是否允许我改 shell 脚本。  
   - 是否要我给出 Nginx 片段而不是直接改系统文件。

---

### 二、AI 助手在仓库中的工作步骤

当我收到指令后，默认按如下顺序执行（除非你特别说明只想要方案、不想落地代码）：

1. **理解与勘察**  
   - 使用 `ls`、`rg`、`sed` 等命令快速浏览相关文件。  
   - 查找与本需求相关的模板、脚本、配置（例如 Hugo 模板、FastAPI 后端、Nginx 说明等）。  
   - 若已有设计文档（`README.md`、`agentdone.md` 等），先阅读相关章节。

2. **修改代码 / 配置**  
   - 使用 `apply_patch` 精准修改相关文件：  
     - 后端 Python：如 `blog_server.py`。  
     - 前端 Hugo 模板：如 `themes/simple/layouts/_default/*.html`。  
     - 脚本：如 `start_backend.sh`、`build.sh` 等。  
     - 文档：`README.md`、`agentdone.md` 等。  
   - 遵循已有风格，不引入无关重构，不修改与当前任务无关的模块。

3. **本地构建 / 校验**  
   - 若修改会影响 Hugo 页面结构或样式，运行：  
     ```bash
     ./build.sh
     ```  
     确认 Hugo 构建成功（无错误/警告）。  
   - 若修改后端（如 `blog_server.py`），在可行范围内进行简单自检：  
     - 检查语法是否正确。  
     - 确认端口与路由前缀（如 `/api/`）与 Nginx 说明一致。  
   - 不会擅自启动长期常驻进程，只写出你可以运行的命令（如 `./start_backend.sh`）。

4. **更新文档**  
   - 在需求涉及的功能区域，对应更新：  
     - `README.md`：对外展示的总览文档。  
     - `agentdone.md`：细节实现和部署说明。  
     - `workflows.md`：记录这类「从命令到自动构建与提交」的工作方式。  
   - 确保文档中的命令、脚本名称、路径与最新实现一致（例如 `blog_server.py`、`start_backend.sh`、`backend.log`、`/api/` 前缀等）。

5. **Git 提交与推送（自动）**  
   - 查看当前变更：`git status`。  
   - 将与本次任务相关的文件加入暂存区：  
     ```bash
     git add <被修改的代码 / 模板 / 文档文件>
     ```  
   - 不将本地运行时产物（如 `backend.log`、`views.db`、`public/`）加入版本控制，必要时更新 `.gitignore`。  
   - 使用简洁、语义清楚的提交信息，例如：  
     ```bash
     git commit -m "feat: add server-side view counter and backend rename"
     ```  
   - 在分支为 `master` 且远端为 `origin` 的前提下，执行：  
     ```bash
     git push origin master
     ```  
   - 若你有特别的分支 / 提交流程（如使用 PR、feature 分支），需要在指令里提前说明，我会按你指定的流程操作或只给出命令建议。

---

### 三、典型一次「从指令到上线」的完整流程示例

以「实现服务端浏览量统计，并更新启动脚本、文档和构建」为例：

1. 你在对话里下达指令，大致说明：  
   - 需求：统计所有用户浏览量，构建/重启后不清零。  
   - 技术偏好：复用现有 FastAPI 后端，使用本地 SQLite。  
   - 附加要求：  
     - 重命名 `ai_server.py` → `blog_server.py`。  
     - 重命名 `start_ai.sh` → `start_backend.sh`。  
     - 更新 Nginx 说明为 `/api/` 前缀。  
     - 修改浏览量图标为新 emoji。  

2. 我在仓库中执行改造：  
   - 新增/修改 `blog_server.py`，加入：  
     - `POST /api/views/hit?path=/xxx/` 接口。  
     - SQLite 持久化 `views.db`。  
   - 更新启动脚本：`start_backend.sh`（日志写入 `backend.log`）。  
   - 修改 Hugo 模板：  
     - `themes/simple/layouts/_default/single.html`：显示 `👀 N 次浏览`。  
     - `themes/simple/layouts/_default/baseof.html`：前端 `fetch('/api/views/hit?...')` + localStorage 回退逻辑。  
   - 更新 `.gitignore`（忽略 `backend.log`、`views.db`）。  
   - 更新 `README.md`、`agentdone.md` 以及本文件 `workflows.md`。

3. 我在本地自动构建：  
   ```bash
   ./build.sh
   ```  
   确认 Hugo 构建成功。

4. 我自动完成 Git 操作：  
   ```bash
   git add .gitignore README.md agentdone.md blog_server.py start_backend.sh \
           themes/simple/layouts/_default/baseof.html \
           themes/simple/layouts/_default/single.html \
           workflows.md
   git commit -m "feat: add server-side view counter and backend rename"
   git push origin master
   ```  
   此时 GitHub 仓库已经包含所有改动。

5. 你在服务器上执行部署相关步骤（我只给出建议，不直接改系统文件）：  
   - 确认 Nginx 中 `/etc/nginx/sites-available/codealan.top` 的 8444 后端包含：  
     ```nginx
     location /api/ {
         proxy_pass http://127.0.0.1:9000;
         proxy_http_version 1.1;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
     }
     ```  
   - 重新加载 Nginx：  
     ```bash
     sudo nginx -t
     sudo systemctl reload nginx
     ```  
   - 启动后端：  
     ```bash
     chmod +x start_backend.sh
     ./start_backend.sh
     ```  
   - 如需要，再跑一次 `./build.sh` 并同步最新静态文件到服务器。

---

### 四、后续使用约定

- 若你只想让我给出「修改建议 / diff」，不希望自动 `git commit` / `git push`，请在指令开头明确写：  
  - 「这次不要自动提交和推送，只给出修改方案与 patch」。  
- 默认情况下，只要改动范围清晰且当前分支为 `master`，我会：  
  1. 直接应用修改。  
  2. 尝试本地构建（如 `./build.sh`）。  
  3. 更新文档。  
  4. 自动 `git commit` + `git push origin master`。  
- 若未来你调整了分支策略（例如使用 `dev`、`feature/*` 分支），可以在本文件追加新的约定，我会按最新约定执行。  

