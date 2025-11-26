---






title: Project 4 AerialVLN模拟器与AirVLN任务
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- VLN
- Ubuntu
- 深蓝课程
- 项目
- Navigation
- Habitat
---
# AerialVLN模拟器与AirVLN任务
## 总体目标
### 1.掌握AerialVLN模拟器的安装
学会如何搭建AerialVLN模拟器。
### 2.复现AirVLN任务
准备AirVLN相关的数据集，并了解数据组成，复现AirVLN任务。

## 任务0 建立工作目录

```bash
mkdir AirVLN_ws
mkdir AirVLN_ws/ENVs
mkdir AirVLN_ws/DATA

# 后续步骤，都是在AirVLN_ws目录下运行
cd AirVLN_ws
```

>本项目需要用到UE4引擎做渲染，对算力性能要求较高，项目开发用服务器为4090显卡、32核128G内存


## 任务1 AirSim模拟器的安装
### 任务目标

1.安装AirSim插件
2.下载AirVLN场景模拟器
### 任务步骤

#### 1.通过conda安装airsim
```bash
conda create -n AirVLN python=3.8

conda activate AirVLN

pip install airsim==1.7.0
```

#### 2.下载AerialVLN模拟器(约35GB)
AerialVLN模拟器使用的是UE4引擎和AirSim插件，因此可以实现连续的空中导航和逼真的场景渲染。共包含25个不同城市的环境。
```bash
cd ./ENVs
curl -L -o ./aerialvln-simulators.zip\
  https://www.kaggle.com/api/v1/datasets/download/shuboliu/aerialvln-simulators
unzip aerialvln-simulators.zip
```
模拟器比较大，下载时间较长，如果Kaggle无法访问，可以从[百度网盘下载]([百度网盘](https://pan.baidu.com/e/verify?surl=R8xuewgEoy5Gc1l5AFhGMw))，提取码: SHAN。

#### 3.运行模拟器(以场景3为例)
```bash
cd ./ENVs/env_3/env_3/LinuxNoEditor

# 强制程序使用独显，这一步很重要！！
export DRI_PRIME=1

# 运行模拟器
./AirVLN.sh
```
正常的话，可以看到模拟器界面，并进行简单的操作。

## 任务2 复现AirVLN任务
### 任务步骤
#### 1.下载aerialvn与aerialvIn-s数据集

```bash
mkdir ./DATA/data
mkdir ./DATA/data/aerialvln
mkdir ./DATA/data/aerialvln-s

# 切换工作目录
cd ./DATA/data

# 下载并解压aerialvln数据集
curl -L -o ./aerialvln.zip\
  https://www.kaggle.com/api/v1/datasets/download/shuboliu/aerialvln
unzip ./aerialvln.zip -d aerialvln/

# 下载并解压aerialvln-s数据集
curl -L -o ./aerialvln-s.zip\
  https://www.kaggle.com/api/v1/datasets/download/shuboliu/aerialvln-s
unzip ./aerialvln-s.zip -d aerialvln-s/
```

#### 2.下载预训练模型
从[下载链接](https://dl.fbaipublicfiles.com/habitat/data/baselines/v1/ddppo/ddppo-models/gibson-2plus-resnet50.pth)获取预训练模型并放入`./DATA/data/ddppo`

```bash
mkdir ./DATA/models
mkdir ./DATA/models/ddppo-models

cd ./DATA/models/ddppo-models
wget https://dl.fbaipublicfiles.com/habitat/data/baselines/v1/ddppo/ddppo-models/gibson-2plus-resnet50.pth
```


#### 3.获取场景描述文件
从[百度网盘](https://pan.baidu.com/e/verify?surl=R8xuewgEoy5Gc1l5AFhGMw)下载(提取码: SHAN)`nav_graph` 和 `token dict` ，放入 `DATA/data/disceret/processed/ `目录下

```bash
mkdir ./DATA/data/disceret
mkdir ./DATA/data/disceret/processed
```

场景描述文件对场景中的导航点进行描述，，` token_dict` 中是导航点的位置信息， `nav_graph `中是导航点之间的邻接关系。

#### 4.获取` AirVLN` 代码并配置环境

```bash
# 在AirVLN_ws目录下执行

conda activate AirVLN

# 官方项目地址为https://github.com/AirVLN/AirVLN.git，我们在官方基础上，进行了细微的修改
git clone https://github.com/xmlnudt/AirVLN.git
cd ./AirVLN
pip install -r requirements.txt

# 根据GPU型号以及CUDA版本选择
pip install torch==1.13 torchaudio torchvision --index-url https://download.pytorch.org/whl/cu118

pip install pytorch-transformers==1.2.0
```

5.运行训练脚本
```bash
conda activate AirVLN

bash ./AirVLN/scripts/train.sh
```

## 附录
### 目录结构
```bash
AirVLN_ws/
├── AirVLN/
│   ├── Model/
│   │   └── ...
│   ├── airsim_plugin/
│   │   ├── AirVLNSimulatorClientTool.py
│   │   ├── AirVLNSimulatorServerTool.py
│   │   └── ......
│   ├── requirements.txt
│   ├── scripts/
│   │   ├── collect.sh
│   │   ├── download_dataset_aerialvln-s.sh
│   │   ├── download_dataset_aerialvln.sh
│   │   ├── eval.sh
│   │   └── train.sh
│   ├── src/
│   │   ├── common/
│   │   └── vlnce_src/
│   └── utils/
├── DATA/
│   ├── data/
│   │   ├── aerialvln/
│   │   │   ├── test.json
│   │   │   ├── train.json
│   │   │   ├── train_vocab.txt
│   │   │   ├── val_seen.json
│   │   │   └── val_unseen.json
│   │   └── aerialvln-s/
│   │       ├── test.json
│   │       ├── train.json
│   │       ├── train_vocab.txt
│   │       ├── val_seen.json
│   │       └── val_unseen.json
│   └── models/
│       └── ddppo-models/
│           └── gibson-2plus-resnet50.pth
└── ENVs
    ├── env_1/
    ├── env_2/
    └── ...

```