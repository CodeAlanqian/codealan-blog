---



title: docker自启动
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- Docker
- Ubuntu
---
# docker自启动


## 设置docker自启动

```bash
systemctl enable docker
```



## 创建时设置自启动

```bash
docker run -d --restart=always --name 设置容器名 使用的镜像
（上面命令  --name后面两个参数根据实际情况自行修改）
 
# Docker 容器的重启策略如下：
 --restart具体参数值详细信息：
     no　　　　　　　 // 默认策略,容器退出时不重启容器；
     on-failure　　  // 在容器非正常退出时（退出状态非0）才重新启动容器；
     on-failure:3    // 在容器非正常退出时重启容器，最多重启3次；
     always　　　　  // 无论退出状态是如何，都重启容器；
     unless-stopped  // 在容器退出时总是重启容器，但是不考虑在 Docker 守护进程启动时就已经停止了的容器。
```



## 修改docker自启动

开启自启动

```bash
docker update --restart=always 容器ID或容器名
```



关闭自启动

```bash
docker update --restart=no 容器ID或容器名
```





