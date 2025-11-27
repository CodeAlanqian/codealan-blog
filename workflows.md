## Blog backend & view counter workflow

### Overview

This document summarizes the backend and view-counter workflow that was added with the help of the AI assistant, so future maintenance is straightforward.

### Components

- `blog_server.py`  
  - FastAPI application running on `127.0.0.1:9000`.  
  - Endpoints:  
    - `POST /api/ai/chat` – DeepSeek proxy used by the floating AI assistant.  
    - `POST /api/views/hit?path=/xxx/` – increments and returns the global page-view count for the given path.  
  - Persistence:  
    - Uses a local SQLite database `views.db` in the project root.  
    - Table `views(path TEXT PRIMARY KEY, count INTEGER NOT NULL)`.  
    - All increments are guarded by a process-wide lock to avoid races.

- `start_backend.sh`  
  - Helper script to (re)start the backend.  
  - Kills existing `blog_server.py` processes (SIGTERM, then SIGKILL if needed).  
  - Loads environment variables from `.env` (including `DEEPSEEK_API_KEY`) and starts `blog_server.py` via `nohup`.  
  - Logs go to `backend.log` in the project root (ignored by Git).

- Nginx (server-side)  
  - In `/etc/nginx/sites-available/codealan.top`, the HTTPS backend on port `8444` should proxy all `/api/` routes to the backend:
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
  - This single block covers both `/api/ai/chat` and `/api/views/hit`.

- Hugo templates (frontend)
  - Article template: `themes/simple/layouts/_default/single.html`  
    - Under the title, shows:
      ```html
      <span class="icon-eye" aria-hidden="true">👀</span>
      <span class="view-count" data-key="{{ .RelPermalink }}">0</span> 次浏览 ·
      ```
    - The `data-key` attribute is the canonical key for view counting (Hugo `.RelPermalink`).
  - Global script: `themes/simple/layouts/_default/baseof.html`  
    - JS snippet finds `.view-count`, then:
      - Calls `fetch('/api/views/hit?path=' + encodeURIComponent(key), { method: 'POST' })`.  
      - On success, sets `el.textContent = data.count`.  
      - On failure or bad response, falls back to local counting via `localStorage` using the same key.

### Typical workflow

1. Start or restart backend  
   ```bash
   chmod +x start_backend.sh
   ./start_backend.sh
   ```

2. Ensure Nginx is configured and reloaded  
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

3. Build Hugo site  
   ```bash
   ./build.sh
   ```

4. Verify behavior  
   - Open any article on `https://codealan.top/`.  
   - Check that the line under the title shows `👀 N 次浏览`.  
   - Open from another browser / private window; the number should increase globally (not per-browser).  
   - Stop the backend and reload the page to see the localStorage fallback still incrementing per browser.

