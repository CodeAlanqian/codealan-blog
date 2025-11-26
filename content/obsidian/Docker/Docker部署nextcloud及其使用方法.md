---



title: Docker部署nextcloud及其使用方法
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- Docker
- Security
- Ubuntu
- RL
- Git
- Nextcloud
---
# Docker部署Nextcloud及其使用方法



## Docker安装

> Docker 是一个开源的应用容器引擎，基于 [Go 语言](https://www.runoob.com/go/go-tutorial.html) 并遵从 Apache2.0 协议开源。
>
> Docker 可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。
>
> 容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）,更重要的是容器性能开销极低。
>
> ## Docker的应用场景
>
> - Web 应用的自动化打包和发布。
> - 自动化测试和持续集成、发布。
> - 在服务型环境中部署和调整数据库或其他的后台应用。
> - 从头编译或者扩展现有的 OpenShift 或 Cloud Foundry 平台来搭建自己的 PaaS 环境。
>
> ------
>
> ## Docker 的优点
>
> Docker 是一个用于开发，交付和运行应用程序的开放平台。Docker 使您能够将应用程序与基础架构分开，从而可以快速交付软件。借助 Docker，您可以与管理应用程序相同的方式来管理基础架构。通过利用 Docker 的方法来快速交付，测试和部署代码，您可以大大减少编写代码和在生产环境中运行代码之间的延迟。
>
> ### 1、快速，一致地交付您的应用程序
>
> Docker 允许开发人员使用您提供的应用程序或服务的本地容器在标准化环境中工作，从而简化了开发的生命周期。
>
> 容器非常适合持续集成和持续交付（CI / CD）工作流程，请考虑以下示例方案：
>
> - 您的开发人员在本地编写代码，并使用 Docker 容器与同事共享他们的工作。
> - 他们使用 Docker 将其应用程序推送到测试环境中，并执行自动或手动测试。
> - 当开发人员发现错误时，他们可以在开发环境中对其进行修复，然后将其重新部署到测试环境中，以进行测试和验证。
> - 测试完成后，将修补程序推送给生产环境，就像将更新的镜像推送到生产环境一样简单。
>
> ### 2、响应式部署和扩展
>
> Docker 是基于容器的平台，允许高度可移植的工作负载。Docker 容器可以在开发人员的本机上，数据中心的物理或虚拟机上，云服务上或混合环境中运行。
>
> Docker 的可移植性和轻量级的特性，还可以使您轻松地完成动态管理的工作负担，并根据业务需求指示，实时扩展或拆除应用程序和服务。
>
> ### 3、在同一硬件上运行更多工作负载
>
> Docker 轻巧快速。它为基于虚拟机管理程序的虚拟机提供了可行、经济、高效的替代方案，因此您可以利用更多的计算能力来实现业务目标。Docker 非常适合于高密度环境以及中小型部署，而您可以用更少的资源做更多的事情。
>
> --from [Docker 教程 | 菜鸟教程 (runoob.com)](https://www.runoob.com/docker/docker-tutorial.html)



Ubuntu环境下安装Docker

```bash
sudo apt-get update

sudo apt-get install ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```



启动Docker

```bash
sudo systemctl enable docker.service
sudo systemctl start docker
```



验证Docker安装成功

```bash
docker version
#有信息输出
```



## Docker-compose

> ### Compose 简介
>
> Compose 是用于定义和运行多容器 Docker 应用程序的工具。通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。
>
> 如果你还不了解 YML 文件配置，可以先阅读 [YAML 入门教程](https://www.runoob.com/w3cnote/yaml-intro.html)。
>
> Compose 使用的三个步骤：
>
> - 使用 Dockerfile 定义应用程序的环境。
> - 使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
> - 最后，执行 docker-compose up 命令来启动并运行整个应用程序。



```bash
wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O /usr/local/bin/docker-compose
```

如果这一步失败，请直接到GitHub在本地下载docker-compose可执行文件

上传至服务器的`/usr/local/bin/`文件夹，并将文件改名为`docker-compose`



添加运行权限

```bash
chmod +x /usr/local/bin/docker-compose
```

验证docker-compose命令

```bash
docker-compose -v
```





## Nextcloud的docker-compose部署方法



创建用于保存nextcloud配置和文件的目录

```bash
mkdir -p /nextcloud/nginx # 存放nginx配置
mkdir -p /nextcloud/db # 存放数据库文件
mkdir -p /nextcloud/app # 存放nextcloud程序包，以后出现问题了可以修改里面的php配置文件
```



切换到`/nextcloud/`文件夹下


```bash
cd /nextcloud/
```

创建`docker-compose.yaml`

```bash
nano docker-compose.yaml
```



输入以下内容

```yaml
version: '2'

#volumes:
  #nextcloud:
  #db:

services:
  db:
    image: mariadb:10.5
    restart: always
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
    networks:
      - nextcloud_netbridge
    volumes:
      - /nextcloud/db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=123456
      - MYSQL_PASSWORD=nextcloud
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:
    image: nextcloud
    restart: always
    ports:
      - 11000:80
    networks:
      - nextcloud_netbridge
    links:
      - db
    volumes:
      - /nextcloud/app:/var/www/html
    environment:
      - MYSQL_PASSWORD=nextcloud
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db

networks:
  nextcloud_netbridge:
    driver: bridge
    

```

如果想把端口映射改为80，可以将上面的

>  ports:
>       \- 11000:80

改为

> ports:
>       \- 80:80



最后启动集成配置

```bash
docker-compose -f /nextcloud/docker-compose.yaml up -d
```



通过`http://ip:11000`

如`http://localhost:11000`即可访问nextcloud

进入之后创建管理员账号，设置密码



## 修改Trusted domains（选做）

Nextcloud是很注重安全性的开源网盘项目。它阻止除白名单外的一切访问方式

> 官方文档是：
> Trusted domains
> All URLs used to access your Nextcloud server must be whitelisted in your **config.php** file, under the trusted_domains setting. Users are allowed to log into Nextcloud only when they point their browsers to a URL that is listed in the trusted_domains setting. You may use IP addresses and domain names. A typical configuration looks like this:
> 'trusted_domains' =>
> array (
> 0 => 'localhost',
> 1 => 'server1.example.com',
> 2 => '192.168.1.50',
> 3 => '[fe80::1:50]',
> ),



查看docker容器

```bash
docker ps -a
```

输出类似：

```bash
CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS          PORTS                                     NAMES
f392845aba1e   nextcloud      "/entrypoint.sh apac…"   18 hours ago   Up 20 minutes   0.0.0.0:11000->80/tcp, :::11000->80/tcp   nextcloud-app-1
2c614b0dca75   mariadb:10.5   "docker-entrypoint.s…"   18 hours ago   Up 18 hours     3306/tcp                                  nextcloud-db-1
```

找到nextcloud的ID

进入容器

```bash
docker exex -it <CONTAINER ID> /bin/bash

如
docker exec -it f392845aba1e /bin/bash
```

安装nano编辑器

```bash
apt update
apt install nano
```



进入config文件夹

```bash
cd config
```

修改config.php

```bash
nano config.php
```

找到`trusted_domains`写入你要添加的域名

像这样：

```php
'trusted_domains' =>
array (
0 => 'localhost',
1 => 'server1.example.com',
2 => '192.168.1.50',
3 => '[fe80::1:50]',
),
```

Ctrl + o保存，回车确定，Ctrl+x退出

最后退出容器

```bash
exit
```



重启容器，使配置生效

```bash
docker restart <CONTAINER ID>

如：
docker restart f392845aba1e
```







## 使用命令行上传

### 方法一

```bash
curl -u USER:PASSWORD -T PUSHFILEPATH  "NEXTCLOUDwebDEV"
```

USER
 你的登录nextcloud的账号

PASSWORD
 你的登录nextcloud的密码

PUSHFILEPATH
 你要上传文件的路径

NEXTCLOUDwebDEV是一个URL
 获取地址 web登录NEXTCLOUD 点击上边文件 然后点击左下角设置 会出现一个webDEV的，下边方框里的URL就是了

这是一个家目录，如果想上传到家目录下某个目录下，可以直接在URL后跟路径就行

### 方法二

写一个脚本push_nextcloud.sh（命名随意）

```bash
#!/bin/bash
USER=""
PASSWD=""
WEBDEV=""

curl -u $USER:$PASSWD -T $1  "$WEBDEV$2"
```

上传命令

```bash
bash push_nextcloud.sh pushfile path
```





## 使用命令行下载

首先在nextcloud里面把要下载的文件共享出来，得到共享链接

得到的链接一般是这样的：

```bash
http://example.com/s/5Q8A4zjJG4qgLFw
```

在末尾添加/download/文件名：

```bash
http://example.com/s/5Q8A4zjJG4qgLFw/download/Birdie.jpg
```



使用wget

```bash
wget http://example.com/s/5Q8A4zjJG4qgLFw/download/Birdie.jpg
```



使用curl

```bash
curl -O -L http://example.com/s/5Q8A4zjJG4qgLFw/download/Birdie.jpg
```





## TBD：服务器部署+绑定二级域名

TODO



## 参考资料

参考来源：

[使用docker-compose安装Nextcloud_docker-compose nextcloud_上海一亩地的博客-CSDN博客](https://blog.csdn.net/qq_43626147/article/details/124689863)

[nextcloud：linux命令行上传文件_nextcloud上传文件夹_糖℃ᶫᵒᵛᵉᵧₒᵤ的博客-CSDN博客](https://blog.csdn.net/user943200420/article/details/120067701)



Written by CodeAlan