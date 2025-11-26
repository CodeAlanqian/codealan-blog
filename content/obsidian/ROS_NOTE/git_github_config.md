---



title: git_github_config
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- ROS_NOTE
- Git
- RL
- ROS
- Ubuntu
---
# 配置git 和 github

## 安装

```
sudo apt-get install git
```

## 配置本地

此用户名和邮箱是git提交代码时用来显示你身份和联系方式的，并不是github用户名和邮箱

```
git config --global user.name "YOUR_NAME"

git config --global user.email "YOUR_EMAIL"
```

example

```
git config --global user.name "CodeAlan"

git config --global user.email "2546379375@qq.com"

```

检查配置信息

```
git config --global --list

press q to quit
```

## git push/pull 鉴权失败

当你想要git push/pull时，会要你输入**Username for 'https://github.com': 和****password**

username是注册时设置的用户名

在这里登录github并不是使用注册时设置的密码

tips:输入password时页面不会有任何反应

需要做的事情是：

打开github.com->Settings->Developer settings -> Persional access tokens(PAT) -> generate new token

将token复制，保存下来，token相当于你的密码

重新git push/pull 输入username 和 token

## Https配置免密登录

每次git push/pull时都要输入username password

在shell中输入

```
git config --global credential.helper store
 
git pull /git push
```

输入username password，后续就不用再次输入

这一步会在用户目录下生成文件.git-credential记录用户名密码的信息

## SSH配置免密登录

shell中输入下列指令，生成公钥

```
ssh-keygen -t rsa -C "YOUR_EMAIL"
```

此时输出的内容会显示公钥的保存目录，默认是/home/用户名/.ssh/id_rsa.pub

打开github.com -> Settings -> SSH and GPG keys -> New SSH key


title：随便取


Keytype：默认


Key：将ssh对应目录下**id_rsa.pub**中内容粘贴进去
最后，**Add SSH key**

回到shell检查配置是否成功：

```
ssh -T git@github.com
```

出现successfully就成功了

```
Hi <USERNAME>! You've successfully authenticated, but GitHub does not provide shell access.

```

## Https和 SSH 的区别

Https可以随意克隆github上的项目，而不管是谁的；而SSH 则是你必须是你要克隆的项目的拥有者或管理员，且需要先添加 SSH key ，否则无法克隆。https url 在push的时候是需要验证用户名和密码的；而 SSH 在push的时候，是不需要输入用户名的，如果配置SSH key的时候设置了密码，则需要输入密码的，否则直接是不需要输入密码的。