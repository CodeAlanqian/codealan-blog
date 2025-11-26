# 博客系统与 OneDrive 同步方案

## 目标
- 在本地 `~/mypage` 搭建 Hugo 静态博客，主题简洁（推荐 PaperMod）。
- 内容与资源从 OneDrive/Obsidian 拉取，无需 git。
- 本地构建输出 `public/`，可用任意静态服务器发布。

## 需要的信息
- OneDrive 本地路径与 Obsidian 笔记/资源所在子目录（例如 `/home/ubuntu/OneDrive/Vault`）。
- 选择同步方式：
  - rsync 复制：周期性从 OneDrive 拉到 `content`/`static`。
  - 或使用符号链接：`content`/`static` 指向 OneDrive 对应目录。

## 目录规划（本地站点）
- Hugo 根：`~/mypage`
- 内容：`content/posts/<slug>/index.md`（同目录可放图片）。
- 静态资源：`static/images/`（或与文章同目录）。
- 构建输出：`public/`。

## 配置与前提
- 安装 Hugo（本机已有即可）。
- 主题：添加 PaperMod（或其他简洁主题）。
- 统一 front matter（YAML）：`title`, `date`, `tags`, `summary`, 可选 `cover`。
- 代码高亮、RSS、sitemap 在配置中开启。

## 脚本计划
- `sync-from-onedrive.sh`: 将 OneDrive 笔记/资源同步到 Hugo `content`/`static`（rsync）。
- `build.sh`: `hugo --minify` 生成静态站。
- `preview.sh`: `hugo server -D` 本地预览。
- （可选）systemd/cron 定时执行 sync + build。

## 执行步骤
1) 初始化 Hugo 站点，添加主题（PaperMod），编写 `config`。
2) 根据提供的 OneDrive 路径设置同步（rsync 或符号链接）。
3) 添加示例文章/About/标签页，验证样式与 Obsidian 兼容。
4) 运行 `hugo server` 预览；`hugo --minify` 生成 `public/`。
5) 部署方式：将 `public/` 上传/同步到目标静态目录或服务器。
