---



title: zsh&ohmyzsh
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- ROS_NOTE
- Ubuntu
- Git
- ROS
---
# zsh&ohmyzsh配置指南



## zsh



```
sudo apt install zsh
```





## ohmyzsh

```
sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
```



这里大概率会遇到DNS污染问题

解决办法：

1.访问域名查询网址:<https://ipaddress.com/>

2.查询域名ip，搜索框中输入: raw.githubusercontent.com，自由复制一个查询到的IP

3.修改 /etc/hosts 文件，命令:

```
sudo gedit /etc/hosts
```

添加内容(查询到的ip与域名)，如：

```bash
151.101.76.133 raw.githubusercontent.com 
```

保存并退出。







## 插件



### 自动补全 [zsh-autosuggestions](https://link.zhihu.com/?target=https%3A//github.com/zsh-users/zsh-autosuggestions)

```
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```



### 语法高亮 [zsh-syntax-highlighting](https://link.zhihu.com/?target=https%3A//github.com/zsh-users/zsh-syntax-highlighting)

```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```





引入插件

```
nano ~/.zshrc
或
vim ~/.zshrc
```

找到**plugins = (git)**

```
plugins=(git zsh-syntax-highlighting zsh-autosuggestions)

//或者这样
plugins=(
    git
    zsh-syntax-highlighting
    zsh-autosuggestions
)
```

使用vim的话，按**i**进入插入模式，修改完成后按**ESC**，输入 **:wq** 保存退出



使修改生效

```
source ~/.zshrc
```



## 主题

修改主题

主题列表：

[Themes · ohmyzsh/ohmyzsh Wiki (github.com)](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)



进入配置文件

```bash
nano ~/.zshrc
或
vim ~/.zshrc
```



找到`ZSH_THEME=robbyrussell`

将`robbyrussell`修改为对应主题名字即可。

例如：

```bash
ZSH_THEME="ys"
```



使修改生效

```
source ~/.zshrc
```



## 注意

由于解释器由原来的bash改成了zsh，所以以后遇到执行如`xxx.bash`的文件时，需要将bash改成zsh，`xxx.zsh`





Written by CodeAlan

Update:2023/7/4



sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key  F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE

