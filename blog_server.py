import os
from pathlib import Path
from typing import List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import threading


def _load_deepseek_key() -> Optional[str]:
    """
    按顺序加载 DeepSeek API Key：
    1. 优先使用环境变量 DEEPSEEK_API_KEY
    2. 否则尝试读取项目根目录的 .env 文件中的 DEEPSEEK_API_KEY
    """
    env_key = os.environ.get("DEEPSEEK_API_KEY")
    if env_key:
        return env_key

    # 简单解析 .env：每行 KEY=VALUE，忽略注释和空行
    root = Path(__file__).resolve().parent
    env_path = root / ".env"
    if not env_path.exists():
        return None

    value = None
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, v = line.split("=", 1)
            key = key.strip()
            if key == "DEEPSEEK_API_KEY":
                value = v.strip().strip('"').strip("'")
                break
    except OSError:
        return None

    if value:
        # 也写入当前进程环境，方便后续复用
        os.environ.setdefault("DEEPSEEK_API_KEY", value)
    return value

app = FastAPI(title="CodeAlan Blog Backend")

# 可按需要调整允许的来源；默认允许同源 + 本地开发
origins = [
    "http://localhost",
    "http://localhost:1313",
    "https://codealan.top",
    "https://www.codealan.top",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatReply(BaseModel):
    reply: str


class ViewHitResponse(BaseModel):
    path: str
    count: int


class LikeResponse(BaseModel):
    path: str
    count: int


class StatItem(BaseModel):
    path: str
    count: int


_DB_LOCK = threading.Lock()
_DB_PATH = Path(__file__).resolve().parent / "views.db"


def _init_db() -> None:
    """
    初始化（或确保存在）SQLite 数据库和统计表。
    """
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS views (
                    path TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS likes (
                    path TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()


def _increment_view(path: str) -> int:
    """
    将指定 path 的浏览量 +1，并返回最新总数。
    """
    if not path:
        path = "/"
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute("SELECT count FROM views WHERE path = ?", (path,))
            row = cur.fetchone()
            if row is None:
                count = 1
                cur.execute(
                    "INSERT INTO views (path, count) VALUES (?, ?)", (path, count)
                )
            else:
                count = int(row[0]) + 1
                cur.execute(
                    "UPDATE views SET count = ? WHERE path = ?", (count, path)
                )
            conn.commit()
            return count
        finally:
            conn.close()


def _increment_like(path: str) -> int:
    """
    将指定 path 的“点赞”次数 +1，并返回最新总数。
    """
    if not path:
        path = "/"
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute("SELECT count FROM likes WHERE path = ?", (path,))
            row = cur.fetchone()
            if row is None:
                count = 1
                cur.execute(
                    "INSERT INTO likes (path, count) VALUES (?, ?)", (path, count)
                )
            else:
                count = int(row[0]) + 1
                cur.execute(
                    "UPDATE likes SET count = ? WHERE path = ?", (count, path)
                )
            conn.commit()
            return count
        finally:
            conn.close()


def _get_like_count(path: str) -> int:
    """
    返回指定 path 的点赞总数（不存在则为 0）。
    """
    if not path:
        path = "/"
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute("SELECT count FROM likes WHERE path = ?", (path,))
            row = cur.fetchone()
            return int(row[0]) if row is not None else 0
        finally:
            conn.close()


@app.on_event("startup")
def _on_startup() -> None:
    _init_db()


@app.post("/api/ai/chat", response_model=ChatReply)
async def chat(req: ChatRequest) -> ChatReply:
    """
    简单的个人 AI 代理：
    - 前端只需要给出 messages（user/assistant 轮次）
    - 在服务端使用 DEEPSEEK_API_KEY 调用 DeepSeek Chat API
    """
    api_key = _load_deepseek_key()
    if not api_key:
        raise HTTPException(status_code=500, detail="DEEPSEEK_API_KEY is not configured")

    if not req.messages:
        raise HTTPException(status_code=400, detail="messages must not be empty")

    # 在最前面插入一个固定的 system prompt，强化“个人 AI 助手”的站点上下文
    system_prompt = """
You are the personal AI assistant for the technical and academic blog of Yiqian Gong (龚易乾, CodeAlan) at https://codealan.top.

High-level context:
- The site is a Hugo-based static blog with a custom theme, focused on embodied AI, Vision-Language Navigation (VLN), robotics, ROS, Docker, Ubuntu, RL, LLM, and engineering practice.
- The homepage lists posts; there are tag pages (with a tag knowledge graph), an academic page at /academic/, an operations notes page at /notes/, archives, and a search page.
- Many notes are synchronized from Obsidian (content under /obsidian/), with code blocks, PDF links, and technical snippets.
- The academic page summarizes the author’s background: SUSTech National Excellence Engineer Institute (Electronic Information master), research on VLN and embodied AI, undergraduate projects on multi-sensor fusion SLAM for UAVs, RoboMaster VANGUARD team (vision, auto-aim, ballistic solver, sentinel navigation), Intelligent Car competitions (ROS outdoor vehicle race), and related honors/awards. It also embeds representative Bilibili videos and links to an open-source ballistic solver project on GitHub.
- The notes (/notes/) contain “one-page” frequently used commands (Docker, tmux, Git, Nginx, acme.sh, etc.) and a Bug & Pitfall notebook for environment issues and deployment quirks.
- The UI includes: code blocks with language labels and copy buttons, a PPT-style reading mode for articles, a tag knowledge graph (force-directed SVG) on the tag index page, and this personal AI assistant as a floating widget.

Behavior guidelines:
- Always answer in the same language as the user (Chinese or English).
- Keep answers technically accurate, concise, and structured (bullet points or step-by-step when helpful).
- Be especially helpful for:
  - Explaining concepts related to VLN, embodied AI, robotics, RL, LLM, ROS, Docker, Ubuntu, and development workflows.
  - Designing or improving blog content/structure, tags, and navigation.
  - Summarizing or reorganizing knowledge similar to what would appear in technical notes, academic profiles, or command cheat sheets.
  - Suggesting practical commands/configurations for tools like Docker, tmux, Git, Nginx, acme.sh, ROS, Hugo, and Linux shells.
- You do NOT have real-time access to the blog’s file system, database, or analytics; reason generically based on the described structure and typical content.
- Do not invent specific unpublished posts, personal experiences, or private data beyond what is described above. If the user asks about something that is not clearly specified, say you are not sure and offer general advice instead.
- When uncertain, explicitly say so and suggest how the user could verify or experiment (e.g., checking Hugo docs, running a small test, or inspecting Nginx/Hugo configs).
    """.strip()

    messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m.role, "content": m.content}
        for m in req.messages
    ]

    # DeepSeek API：兼容 OpenAI /v1/chat/completions 风格
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=40.0) as client:
            resp = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        # 将 DeepSeek 的错误信息透出一部分，便于调试
        detail = f"DeepSeek API error: {e.response.status_code}"
        raise HTTPException(status_code=502, detail=detail)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"DeepSeek API request failed: {e}")  # type: ignore[str-format]

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="Unexpected response from DeepSeek API")

    return ChatReply(reply=content)


@app.post("/api/views/hit", response_model=ViewHitResponse)
async def hit_view(path: str) -> ViewHitResponse:
    """
    记录某个页面被浏览一次，并返回所有用户的累计浏览量。
    - 参数 path：通常使用 Hugo 的 .RelPermalink，例如 /posts/xxx/。
    """
    count = _increment_view(path)
    return ViewHitResponse(path=path, count=count)


@app.post("/api/likes/hit", response_model=LikeResponse)
async def hit_like(path: str) -> LikeResponse:
    """
    记录某个页面收到一次「觉得有用」，返回所有用户的累计点赞次数。
    - 参数 path：通常使用 Hugo 的 .RelPermalink，例如 /posts/xxx/。
    - 前端负责使用 localStorage 限制同一浏览器重复点击。
    """
    count = _increment_like(path)
    return LikeResponse(path=path, count=count)


@app.get("/api/likes/get", response_model=LikeResponse)
async def get_like(path: str) -> LikeResponse:
    """
    获取某个页面的累计点赞次数。
    """
    count = _get_like_count(path)
    return LikeResponse(path=path, count=count)


def _get_top_stats(table: str, limit: int = 5) -> List[StatItem]:
    """
    返回指定表（views/likes）中 count 最高的若干条记录。
    """
    with _DB_LOCK:
        conn = sqlite3.connect(_DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT path, count FROM {table} ORDER BY count DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()
            return [StatItem(path=row[0], count=int(row[1])) for row in rows]
        finally:
            conn.close()


@app.get("/api/stats/top-views", response_model=List[StatItem])
async def top_views(limit: int = 5) -> List[StatItem]:
    """
    获取浏览量 Top N 的页面列表。
    """
    if limit <= 0:
        limit = 5
    return _get_top_stats("views", limit)


@app.get("/api/stats/top-likes", response_model=List[StatItem])
async def top_likes(limit: int = 5) -> List[StatItem]:
    """
    获取点赞数 Top N 的页面列表。
    """
    if limit <= 0:
        limit = 5
    return _get_top_stats("likes", limit)


if __name__ == "__main__":
    # 开发环境可直接运行：python blog_server.py
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9000)
