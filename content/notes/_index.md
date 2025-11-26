---
title: "运维备忘 & 坑点记录"
tags:
- Notes
- DevOps
---

## 一页记：常用命令速查

### Docker

- 查看容器 / 镜像  
```bash
docker ps          # 正在运行的容器
docker ps -a       # 包含已退出的容器
docker images      # 本地镜像
docker system df   # Docker 占用空间
```

- 容器生命周期  
```bash
docker run -it --rm IMAGE bash     # 交互式临时容器
docker stop NAME && docker rm NAME # 停止并删除容器
docker logs -f NAME                # 持续查看日志
```

- 清理无用资源（谨慎使用）  
```bash
docker system prune -f             # 删除无用容器/网络/构建缓存
docker image prune -a              # 删除所有悬挂/未使用镜像
```

### tmux

- 会话管理  
```bash
tmux new -s vln        # 创建新会话
tmux ls                # 列出会话
tmux attach -t vln     # 连接会话
tmux kill-session -t vln
```

- 常用快捷键（前缀默认 `Ctrl+b`）  
  - `Ctrl+b c`：新建窗口  
  - `Ctrl+b n / p`：切换下一/上一窗口  
  - `Ctrl+b "`：水平分屏  
  - `Ctrl+b %`：垂直分屏  
  - `Ctrl+b d`：脱离会话（留在后台运行）  

### Git

- 日常提交  
```bash
git status
git add path/to/file
git commit -m "message"
git push origin master
```

- 回退相关  
```bash
git log --oneline --graph --decorate
git diff HEAD~1 HEAD      # 查看上一版差异
git restore path/to/file  # 撤销工作区修改
```

> 大文件与构建产物已通过 `.gitignore` 忽略：`public/`、`static/files/`、所有 `*.pdf` 等。

### Nginx

- 配置检查与重载  
```bash
sudo nginx -t                 # 检查配置语法
sudo systemctl reload nginx   # 平滑重载
sudo systemctl restart nginx  # 重启
journalctl -u nginx -e        # 查看 Nginx 日志
```

### acme.sh（证书）

- 常用操作（以 `codealan.top` 为例）  
```bash
~/.acme.sh/acme.sh --list
~/.acme.sh/acme.sh --issue \
  -d codealan.top -d www.codealan.top \
  -w /var/www/letsencrypt
~/.acme.sh/acme.sh --renew -d codealan.top --force
```

## Bug & Pitfall 记事本

记录经常踩坑的地方，方便以后排查与帮别人解坑。

### Hugo / 静态资源

- **问题：** 提交了 `public/` 或大体积 PDF，GitHub 提示大文件警告。  
- **现状：**  
  - `.gitignore` 忽略 `public/`、`static/files/`、以及所有 `*.pdf`（`static/**`、`content/**`、`public/**`）。  
  - 历史已经重建，当前仓库只包含源码与内容。  
- **经验：**  
  - 在服务器本地构建站点：  
```bash
./build.sh
```  
  - 不要把 `public/` 和 PDF 等大文件提交到 Git。  

### Nginx / stream 分流

- **问题：** 443 端口既要给博客用，又要给 VLESS-Reality 使用。  
- **解决：**  
  - 使用 `stream` + `ssl_preread` 按 SNI 分流：`aws.amazon.com` → sui，`codealan.top` / `www.codealan.top` → 博客。  
  - 注意 `nginx.conf` 需要包含 `stream` 配置，例如：  
```nginx
include /etc/nginx/stream.conf;
```  

### Docker / GPU 环境

- **问题示例：** 容器里看不到 GPU / 驱动版本不匹配。  
- **排查点：**  
  - 宿主机是否安装正确的 NVIDIA 驱动 + `nvidia-container-toolkit`。  
  - 检查宿主机与容器中的 GPU 可见性：  
```bash
# 宿主机检查
nvidia-smi

# 容器中检查（示例）
docker run --rm --gpus all nvidia/cuda:12.2.0-base nvidia-smi
```  

### 终端与 tmux

- **问题：** tmux 中中文 / Powerline 字体错位。  
- **经验：**  
  - 终端统一使用 Nerd Font / 等宽字体。  
  - 确认 `$LANG` 与 locale 设置一致（如 `zh_CN.UTF-8`）：  
```bash
echo $LANG
locale
```  

> 之后遇到新的环境坑、兼容性问题，可以按模块继续往这个页面追加小节即可。  
