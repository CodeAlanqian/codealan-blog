---






title: Project 2 Habitat模拟器与VLN-CE数据集
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- VLN
- Ubuntu
- 深蓝课程
- 项目
- Habitat
---
Project2 任务是复现文章，最难受的是配环境，这里我把可能会遇到的大坑做一些提示。
但是环境的坑，千人千面，遇到问题，随时在群里交流。

# 任务1 Habitat模拟器的安装与基础操作

## 说明

为适配VLN-CE的依赖，我们采用老版本[habitat-sim v0.1.7](https://github.com/facebookresearch/habitat-sim/tree/v0.1.7)，最新版本的安装与使用请自行参考[官方仓库](https://github.com/facebookresearch/habitat-sim)。

## 任务步骤

1.通过conda安装habitat-sim

```bash
conda create -n vlnce python=3.7 -y
# 注： 这里如果同学们一直有安装困难，可以尝试python 3.8，兼容性更好

conda activate vlnce

conda install -c aihabitat -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ habitat-sim=0.1.7 headless -y

# 注： 如果这里同学们安装完发现headless出问题， 可以尝试以下方式：
# conda install -c aihabitat -c conda-forge habitat-sim=0.1.7=py3.8_headless_bullet_linux_856d4b08c1a2632626bf0d205bf46471a99502b7
```
如果安装 habitat-sim 太慢或者失败，可以尝试使用 mamba 来提速:
```bash
conda create -n vlnce python=3.7 -y

conda activate vlnce

conda install mamba -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ -y
mamba install -c aihabitat -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ habitat-sim=0.1.7 headless -y
```

测试安装是否成功:
```bash
python

&gt;&gt;&gt; import habitat_sim
```

2.下载示例场景数据
```bash
mkdir ~/habitat_sim_data
wget http://dl.fbaipublicfiles.com/habitat/habitat-test-scenes.zip
unzip habitat-test-scenes.zip -d ~/habitat_sim_data
```

3.运行测试程序
```bash
# C++
habitat-viewer ~/habitat_sim_data/data/scene_datasets/habitat-test-scenes/skokloster-castle.glb
```

# 任务2 VLN-CE数据集准备

## 任务目标

获取VLN-CE项目代码:
```bash
git clone https://github.com/xmlnudt/VLN-CE.git
```
获取Habitat Matterport3D(HM3D)场景数据:
```bash
wget http://kaldir.vc.in.tum.de/matterport/download_mp.py

python2 download_mp.py --task habitat -o VLN-CE/data/scene_datasets/mp3d/
```

HM3D场景数据官方网站:https://aihabitat.org/datasets/hm3d/

获取VLN-CE的R2R数据集:
R2R_VLNCE_V1-3.zip: https://drive.google.com/file/d/1T9SjqZWyR2PCLSXYkFckfDeIs6Un0Rjm/view
R2R_VLNCE_v1-3_preprocessed.zip: https://drive.google.com/file/d/1fo8F4NKgZDH-bPSdVU3cONAkt5EW-tyr/view
下载后解压到 `VLN-CE/data/datasets/R2R_VLNCE_V1-3 `以及`VN-CE/data/datasets/R2R_VLNCE_v1-3_preprocessed `中

也可以采用命令行的方式:
```bash
# R2R_VLNCE_v1-3
gdown https://drive.google.com/uc?id=1T9SjqZWyR2PCLSXYkFckfDeIs6Un0Rjm
# R2R_VLNCE_v1-3_preprocessed
gdown https://drive.google.com/uc?id=1fo8F4NKgZDH-bPSdVU3cONAkt5EW-tyr
```

获取预训练网络权重:
任务3中运行VLN-CE基线模型时，需要用到预训练的encoder网络权重
```bash
wget https://dl.fbaipublicfiles.com/habitat/data/baselines/v1/ddppo/ddppo-models.zip
unzip ddppo-models.zip -d VLN-CE/
```

# 任务3 VLN-CE基线模型复现

## 任务目标
运行VLN-CE的基线模型
## 说明
VLN-CE的基线模型依赖facebook的habitat-lab，因此需要先从源码安装habitat-lab，才能运行基线模型,
## 任务步骤
安装依赖
```bash
sudo apt-get install -y libgl1-mesa-dev libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

安装habitat-lab
```bash
git clone --branch 0.1.7 https://github.com/xmlnudt/habitat-lab.git
cd habitat-lab
pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
pip install --no-cache-dir -r habitat_baselines/rl/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
pip install --no-cache-dir -r habitat_baselines/rl/ddppo/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
python setup.py develop --all
```

注意:由于VLN-CE依赖的tb-nightly在tuna源中无法安装，请使用aliyun源。

安装VLN-CE依赖

```bash
cd VLN-CE

pip install -r requirements.txt
```

注:这里是大坑，同学们可以尝试把 requirements.txt 里的 tensorfiow 升级到2.2.0。 VLN-CE对于现在来说还是太老了，相信很多学生会卡在这里

这我给同学们一点参考推荐，可以把几个requirements 里的库进行适当适配:

VLN-CE/reguirements.txt:
```bash
attrs&gt;=19.1.0
dtw==1.4.0
fastdtw==0.3.4
gdown
gym&gt;=0.17.3
jsonlines
lmdb
msgpack_numpy
networkx
numpy&gt;=1.16.1
pre-commit
torch&gt;=1.6.0
torchvision==0.2.2.post3
tqdm&gt;=4.0.0
tensorflow==2.2.0
tb-nightly
yacs&gt;=0.1.5
Opencv-python&gt;=3.3.0
```


habitat-lab/requirements.txt:
```bash
attrs&gt;=19.1.0
dtw==1.4.0
fastdtw==0.3.4
gdown
gym&gt;=0.17.3
jsonlines
lmdb
msgpack_numpy
networkx
numpy&gt;=1.16.1
pre-commit
torch&gt;=1.6.0
torchvision==0.2.2.post3
tqdm&gt;=4.0.0
tensorflow==2.2.0
tb-nightly
yacs&gt;=0.1.5
Opencv-python&gt;=3.3.0
```

habitat baselines/rl/requirements.txt:
```bash
moviepy&gt;=1.0.1
torch&gt;=1.3.1
tensorflow==2.2.0
tb-nightly
```

habitat baselines/rl/ddppo/requirements.txt:
```bash
ifcfg
```

运行测试代码
```bash
cd VLN-CE

python run.py --exp-config vlnce_baselines/config/r2r_baselines/nonlearning.yaml --run-type eval
```
训练seq2seq模型
```bash
cd VLN-CE

python run.py --exp-config vlnce_baselines/config/r2r_baselines/seq2seq.yaml --run-type train
```

# 附录
---
## 附录1:基于Docker的VLN-CE基础环境
为了简化依赖的安装流程，我们基于Docker构建了Ubuntu 20.04版本的的VLN-CE基础环境镜像，考虑到镜像大小，并没有包含相关数据，需要自行下载并映射到容器中。
首先自行下载VLN-CE所需的数据至 ./data 目录下，然后运行:
```bash
docker run -v ./data:/root/VLN-CE/data hccz95/vlnce:main bash
```
进入容器之后，就可以运行测试代码
```bash
python run.py --exp-config vlnce_baselines/config/r2r_baselines/nonlearning.yaml --run-type eval
```
个人推荐VLN-CE还是自己去配环境好一些!!!!

## 附录2:目录结构
```bash
VLN-CE/
│
├── data/
│   ├── datasets/
│   |   ├── R2R_VLNCE_v1-3/
│   |   └── R2R_VLNCE_v1-3_preprocessed/
│   ├── ddppo-models/
│   |   ├── gibson-0plus-mp3d-train-val-test-blind.pth
│   |   ├── gibson-2plus-mp3d-train-val-test-se-resneXt50-rgb.pth
│   |   ├── gibson-2plus-resnet50.pth
│   |   ├── gibson-2plus-se-resneXt101-lstm1024.pth
│   |   ├── gibson-2plus-se-resneXt101.pth
│   |   ├── gibson-2plus-se-resneXt50.pth
│   |   ├── gibson-2plus-se-resneXt50-rgb.pth
│   |   ├── gibson-4plus-mp3d-train-val-test-resnet50.pth
│   |   └── gibson-4plus-resnet50.pth
│   ├── scene_datasets/
│       └── scene_datasets/
│               └── mp3d/
│                   ├── 1LXtFkjw3qL/
│                   ├── 1pXnuDYAj8r/
│                   └── ......
├── ...
|
└── README.md

habitat-lab
|
|
└── .......
```