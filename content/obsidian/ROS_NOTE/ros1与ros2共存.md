---



title: ros1与ros2共存
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- ROS_NOTE
- ROS
- Ubuntu
---
# ros1与ros2共存

* 系统环境20.04
* ros1版本 ros-noetic
* ros2版本 ros-galactic

为了省事，我们习惯将source写到.bashrc文件(若是不同的解释器如zsh，则为.zshrc文件)

```bash
sudo gedit ~/.bashrc
```

在bashrc末尾加入:

```bash
source /opt/ros/noetic/setup.bash
```

每次打开terminal时如何切换版本？

```shell
sudo gedit ~/.bashrc
```

在.bashrc末尾加入:

```bash
echo "ros noetic(1) or ros2 galactic(2)?"
read edition
if [ "$edition" -eq "1" ];then
  source /opt/ros/noetic/setup.bash
else
  source /opt/ros/galactic/setup.bash
fi
```

如果解释器为zsh，则

```shell
sudo gedit ~/.zshrc
```

在.zshrc末尾加入:

```bash
echo "ros noetic(1) or ros2 galactic(2)?"
read edition
if [ "$edition" -eq "1" ];then
  source /opt/ros/noetic/setup.zsh
else
  source /opt/ros/galactic/setup.zsh
fi
```



实现效果：

![终端效果](/obsidian/ROS_NOTE/assets/terminal.png)

输入1则选择ros-noetic

输入2则选择ros-galactic