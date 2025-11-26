---



title: 修复zsh下ros2无法tab补全问题
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- ROS_NOTE
- Ubuntu
- ROS
---
# zsh中ros2 tab自动补全
环境：

* Ubuntu20.04
* ros-galactic


以galactic为例

```bash
sudo nano /opt/ros/galactic/share/rosidl_cli/environment/rosidl-argcomplete.zsh 
```

将下行注释掉

```bash
autoload -U +X compinit && compinit
```

![argcomplete](/obsidian/ROS_NOTE/assets/argcomplete.png)

```bash
#autoload -U +X compinit && compinit
```

# colcon自动补全

将下列命令加入 ~/.zshrc 末尾

```bash
eval "$(register-python-argcomplete3 colcon)"
```

最后重新source一下配置

```bash
source ~/.zshrc
```
