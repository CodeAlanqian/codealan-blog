---






title: Project 3 REVERIE数据集与DUET模型
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- VLN
- Ubuntu
- 深蓝课程
- 项目
- Navigation
---
# Project 3: REVERIE数据集与DUET模型

## 总体目标

- 深入理解 **REVERlE (Remote Embodied Visual Referring Expression in Real Indoor Environments)**数据集结构及路径可视化方法。

- 掌握并复现 **DUET(Dual-scale Graph Transformer)**模型，理解其在多模态指令导航与目标定位中的工作机制。

REVERlE 发音 [ˈrevəri]

## 任务1 REVERIE数据集

### 数据集介绍

REVERIE 数据集是一个面向真实室内环境的远程县身视觉指代表达任务的基准，旨在评估具身智能体在真实室内环境中执行自然语言引导任务的能力。与传统视觉语言导航 (VLN)任务不同，REVERIE 不仅要求智能体理解指令并完成导航，还需在抵达目标区域后识别并定位目标物体。这一任务综合考察了智能体的语言理解、空间推理、视觉识别与跨模态融合能力，是典型的“导航+视觉指代表达”联合任务。该任务要求智能体:

- 根据自然语言指令在室内三维环境中导航
- 定位并识别目标物体。



### 数据集下载



进入[数据集下载链接](https://www.dropbox.com/scl/fo/4iaw2ii2z2iupu0yn4tqh/AJutXWSGTtjBFYXnxr-4YQw?rlkey=88khaszmvhybxleyv0a9bulyn&e=1&dl=0)，完整数据解压后约20+GB，可以只下载REVERIE部分约2.4GB。



预训练模型 **lxmert** 下载

```bash
mkdir -p datasets/pretrained
wget https://nlp.cs.unc.edu/data/model_LXRT.pth -P datasets/pretrained
```



### 路径可视化

在实际使用过程中，我们可能需要对数据集中的路径或者模型输出的路径进行可视化，这里介绍一种Matterport3DSimulator中自带的可视化方法。

1.下载代码

```bash
git clone https://github.com/xmlnudt/show_trajectories.git

cd show_trajectories
```



2.准备场景数据

将project1中下载的场景数据，，复制或者链接到 `./matterport_mesh` 目录下，以场景 `1LXtFkjw3qL` 为例，数据保存在`./matterport_mesh/v1/scans/1LXtFkjw3qL` 。



3.准备需要可视化的路径



将需要可视化的每条路径，保存为单个json文件，放入`./trajectories` 目录下，格式如下:



```bash
{
    "instr_id": "4784_1",
    "scan": "ac26ZMwG7aT",
    "path": [
        "9cc9a6f97b09469e92ada5d6795d125c",
        "35dde286a5324af49d540f7dd0bc3b74",
        "f1c9fe4b49c443e891b6ef6b41ec25bc",
        "d2bf18703fd645bcb077523c3c200c30",
        "49f26e22f7514331b35d76bc1b8bb9f5",
        "6e5f25022c4d4dbf9a7f35bd77cbf296",
        "6574e941f0be49afa9fd447b99b2e783"
    ]
}
```



4.路径预处理

将数据进行格式转换，方便可视化脚本使用。

```bash
cd show_trajectories

python process.py
```



5.启动可视化服务

```bash
cd show_trajectories

python -m http.server
```



6.打开浏览器，进http://localhost:8000/connectivity.html

![img](https://publicqn.shenlanxueyuan.com/files/course/2025/10-25/11592914d329971897.png)



## 任务2 DUET模型复现

DUET(Dual-scale Graph Transformer)模型提出了“全局粗尺度+ 局部细尺度”的双尺度图结构，以同时捕获导航规划与视觉语言理解两个方面。DUET在执行过程中构建一个“在线柘扑地图”以表示全局环境结构(粗尺度)，并在每个当前视点对局部观测(如相邻可行动作)的语言与视觉特征进行编码(细尺度)。这种设计既支持智能体对未知环境中长期路径规划，又强化了对当前视图与语言指令的精细对齐。



### 安装Matterport3DSimulator

参考Project 1中所述步骤，千万不要忘记将build目录加入环境变量:

```bash
# 请根据你本机的Matterport3DSimulator目录来设置

export PYTHONPATH=Matterport3DSimulator/build:$PYTHONPATH
```



### 安装DUET所需依赖

```bash
conda create --name vlnduet python=3.8.5
conda activate vlnduet
pip install --only-binary=:all: \
    jsonlines==2.0.0 \
    tqdm==4.62.0 \
    easydict==1.9 \
    Shapely==1.7.1 \
    h5py==2.10.0 \
    torch==1.13 \
    networkx==2.5.1 \
    numpy==1.20.3 \
    tensorboardX==2.4.1 \
    transformers==4.30.0 \
    protobuf==3.20 \
    opencv-python \
    pandas
```

此时，还是注意根据下载的场景数据，修改Matterport3DSimulator项目中的 `scans.txt` 。



### 运行训练脚本

```bash
cd pretrain_src

bash run_reverie_obj.py

```

如果训练时间过长，或者内存/显存不足，可以修改`pretrain_src/config/reverie_obj_pretrain.json`中的`num_train_steps`、`train_batch_size`等训练参数

训练输出如下：

![img](https://publicqn.shenlanxueyuan.com/files/course/2025/10-25/120442aec961200822.png)



### 参数调整

如果需要调整训练参数，可以修改 `pretrain_src/config/reverie_obj_pretrain.json` 配置文件

```bash
{
    "model_config": "",
    "checkpoint": null,
    "output_dir": "",
    "mrc_mask_prob": 0.15,
    "itm_neg_imgs": 5,
    "nearby_vp_steps": null,
    "max_objects": 20,
    "max_txt_len": 200,
    "train_batch_size": 4,
    "val_batch_size": 4,
    "gradient_accumulation_steps": 1,
    "learning_rate": 5e-05,
    "valid_steps": 4000,
    "log_steps": 1000,
    "num_train_steps": 100000,
    "optim": "adamw",
    "betas": [
        0.9,
        0.98
    ],
    ...
    "n_workers": 1,
    "pin_mem": true,
    "init_pretrained": "lxmert",
    ...
}

```





## 附录

### 附录1：Docker的VLN-DUET基础环境

为了简化依赖的安装流程，我们基于Docker构建了Ubuntu 20.04版本的的VLN-DUET环境镜像，不过需要自行下载REVERIE相关数据集，并自行下载并映射到容器对应的目录中。

xhost +

```bash
# 注意替换为你的REVERIE数据所在目录

docker run -it \
    -v /dev/shm:/dev/shm \
    -v ./DUET_datasets:/root/mount/VLN-DUET/datasets \
    --gpus all \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY=$DISPLAY \
    hccz95/mattersim:duet bash
```





### 附录2： 目录结构

```bash
VLN-DUET/
│
├── datasets/
│   ├── pretrained/
│   |   ├── bert-base-uncased/
│   |   └── LXMERT/
│   |       └── model_LXRT.pth
│   ├── R2R/
│   |   ├── annotations/
│   |   ├── connectivity/
│   |   ├── exprs_map/
│   |   ├── features/
│   |   └── trained_models/
│   └── REVERIE/
│       ├── annotations/
│       ├── exprs_map/
│       ├── features/
│       └── trained_models/
│
├── pretrain_src/
│   ├── config/
│   |   ├── ...
│   |   ├── reverie_obj_pretrain.json
│   |   └── ...
│   ├── ...
│   ├── run_reverie.sh
│   ├── ...
│   ├── train_reverie_obj.py
│   └── ...
│
├── ...
|
└── README.md
```



### 附录3：成果交付表

| 项目 | VLN-DUET在REVERIE上的训练结果 |对模型输出的路径在场景中进行可视化绘图 |
| 说明 | 对训练结果进行绘图 | 强烈建议对绘图代码进行扩展，甚至可以支持视频生成 |

