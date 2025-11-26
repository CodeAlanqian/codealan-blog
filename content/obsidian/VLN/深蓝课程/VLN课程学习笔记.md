---






title: VLN课程学习笔记
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- VLN
- Ubuntu
- 深蓝课程
- RL
- LLM
- Navigation
---


详解DeepSeek-R1核心强化学习算法：GRPO https://zhuanlan.zhihu.com/p/21046265072
# VLN课程学习笔记

---
- [#VLN课程学习笔记](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0)
    - [#第四章 学习范式：IL&RL](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%AC%AC%E5%9B%9B%E7%AB%A0%20%E5%AD%A6%E4%B9%A0%E8%8C%83%E5%BC%8F%EF%BC%9AIL%26RL)
        - [#部分可观测马尔可夫决策过程（POMDP）](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E9%83%A8%E5%88%86%E5%8F%AF%E8%A7%82%E6%B5%8B%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E5%86%B3%E7%AD%96%E8%BF%87%E7%A8%8B%EF%BC%88POMDP%EF%BC%89)
        - [#VLA](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23VLA)
        - [#IL vs RL](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23IL%20vs%20RL)
        - [#模仿学习](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%A8%A1%E4%BB%BF%E5%AD%A6%E4%B9%A0)
            - [#典型：seq2seq模型](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%85%B8%E5%9E%8B%EF%BC%9Aseq2seq%E6%A8%A1%E5%9E%8B)
            - [#数据增强：Speaker-Follower模型](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%95%B0%E6%8D%AE%E5%A2%9E%E5%BC%BA%EF%BC%9ASpeaker-Follower%E6%A8%A1%E5%9E%8B)
        - [#强化学习](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0)
            - [#典型：RCM模型，增强交叉模态匹配](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%85%B8%E5%9E%8B%EF%BC%9ARCM%E6%A8%A1%E5%9E%8B%EF%BC%8C%E5%A2%9E%E5%BC%BA%E4%BA%A4%E5%8F%89%E6%A8%A1%E6%80%81%E5%8C%B9%E9%85%8D)
        - [#混合方法：IL + RL](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%B7%B7%E5%90%88%E6%96%B9%E6%B3%95%EF%BC%9AIL%20%2B%20RL)
            - [#典型：VLN-R1](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%85%B8%E5%9E%8B%EF%BC%9AVLN-R1)
    - [#第五章 视觉语言预训练模型](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%AC%AC%E4%BA%94%E7%AB%A0%20%E8%A7%86%E8%A7%89%E8%AF%AD%E8%A8%80%E9%A2%84%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B)
        - [#泛化鸿沟](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%B3%9B%E5%8C%96%E9%B8%BF%E6%B2%9F)
        - [#预训练范式](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E9%A2%84%E8%AE%AD%E7%BB%83%E8%8C%83%E5%BC%8F)
            - [#自监督学习](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E8%87%AA%E7%9B%91%E7%9D%A3%E5%AD%A6%E4%B9%A0)
            - [#经典的视觉语言任务](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%BB%8F%E5%85%B8%E7%9A%84%E8%A7%86%E8%A7%89%E8%AF%AD%E8%A8%80%E4%BB%BB%E5%8A%A1)
        - [#预训练经典架构](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E9%A2%84%E8%AE%AD%E7%BB%83%E7%BB%8F%E5%85%B8%E6%9E%B6%E6%9E%84)
            - [#PREVALENT](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23PREVALENT)
            - [#AirBert](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23AirBert)
            - [#Recurrent VLN-BERT](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Recurrent%20VLN-BERT)
        - [#预训练高级架构](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E9%A2%84%E8%AE%AD%E7%BB%83%E9%AB%98%E7%BA%A7%E6%9E%B6%E6%9E%84)
            - [#BEVBERT](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23BEVBERT)
        - [#微调](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%BE%AE%E8%B0%83)
    - [#第六章 LLM与VLN的融合](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%AC%AC%E5%85%AD%E7%AB%A0%20LLM%E4%B8%8EVLN%E7%9A%84%E8%9E%8D%E5%90%88)
        - [#传统VLN性能瓶颈](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E4%BC%A0%E7%BB%9FVLN%E6%80%A7%E8%83%BD%E7%93%B6%E9%A2%88)
        - [#LLM的优势 强大的知识库](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23LLM%E7%9A%84%E4%BC%98%E5%8A%BF%20%E5%BC%BA%E5%A4%A7%E7%9A%84%E7%9F%A5%E8%AF%86%E5%BA%93)
        - [#IL&RL vs LLM](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23IL%26RL%20vs%20LLM)
        - [#LLM的优势](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23LLM%E7%9A%84%E4%BC%98%E5%8A%BF)
        - [#LLM](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23LLM)
            - [#NavGPT](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23NavGPT)
            - [#NavGPT-2](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23NavGPT-2)
            - [#March in Chat (MiC)](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23March%20in%20Chat%20%28MiC%29)
        - [#微调](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%BE%AE%E8%B0%83)
            - [#Navid框架](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Navid%E6%A1%86%E6%9E%B6)
        - [#LLM的挑战和总结](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23LLM%E7%9A%84%E6%8C%91%E6%88%98%E5%92%8C%E6%80%BB%E7%BB%93)
            - [#接地问题](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%8E%A5%E5%9C%B0%E9%97%AE%E9%A2%98)
            - [#幻觉问题](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%B9%BB%E8%A7%89%E9%97%AE%E9%A2%98)
            - [#Sim2Real Gap](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Sim2Real%20Gap)
    - [#第七章 Air VLN](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%AC%AC%E4%B8%83%E7%AB%A0%20Air%20VLN)
        - [#挑战](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%8C%91%E6%88%98)
            - [#三维路径规划与自由度控制](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E4%B8%89%E7%BB%B4%E8%B7%AF%E5%BE%84%E8%A7%84%E5%88%92%E4%B8%8E%E8%87%AA%E7%94%B1%E5%BA%A6%E6%8E%A7%E5%88%B6)
            - [#感知](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%84%9F%E7%9F%A5)
            - [#Sim2Real](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Sim2Real)
        - [#架构与模型](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%9E%B6%E6%9E%84%E4%B8%8E%E6%A8%A1%E5%9E%8B)
            - [#UAV-VLN](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23UAV-VLN)
            - [#VLFly](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23VLFly)
            - [#OpenFly](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23OpenFly)
        - [#Air VLN的生态](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Air%20VLN%E7%9A%84%E7%94%9F%E6%80%81)
            - [#AirSim](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23AirSim)
            - [#AerialVLN](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23AerialVLN)
            - [#OpenFly](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23OpenFly)
            - [#AerialVLN vs OpenFly](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23AerialVLN%20vs%20OpenFly)
    - [#第八章 机器人中的视觉语言导航应用](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E7%AC%AC%E5%85%AB%E7%AB%A0%20%E6%9C%BA%E5%99%A8%E4%BA%BA%E4%B8%AD%E7%9A%84%E8%A7%86%E8%A7%89%E8%AF%AD%E8%A8%80%E5%AF%BC%E8%88%AA%E5%BA%94%E7%94%A8)
        - [#仿真到物理世界](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E4%BB%BF%E7%9C%9F%E5%88%B0%E7%89%A9%E7%90%86%E4%B8%96%E7%95%8C)
            - [#显著的性能下降](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E6%98%BE%E8%91%97%E7%9A%84%E6%80%A7%E8%83%BD%E4%B8%8B%E9%99%8D)
            - [#鸿沟解构](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E9%B8%BF%E6%B2%9F%E8%A7%A3%E6%9E%84)
            - [#弥合鸿沟](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%BC%A5%E5%90%88%E9%B8%BF%E6%B2%9F)
        - [#前沿架构](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E5%89%8D%E6%B2%BF%E6%9E%B6%E6%9E%84)
            - [#GVNav](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23GVNav)
            - [#SmartWay](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23SmartWay)
            - [#Navid](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Navid)
            - [#Uni-Navid](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23Uni-Navid)
    - [#课程总结](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/%23%E8%AF%BE%E7%A8%8B%E6%80%BB%E7%BB%93)
---
## 第四章 学习范式：IL&RL


### 部分可观测马尔可夫决策过程（POMDP）
Policy Learning

VLN的数学框架：本质上为一个在不确定性下的序列决策问题，用部分可观测马尔可夫决策过程决定（POMDP）
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103205750.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103205954.png)

### VLA
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103210345.png)



![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103210354.png)


### IL vs RL

模仿学习 将策略问题转换为分类器/回归问题
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103210947.png)

 
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103211015.png)


VLN比较复杂，所以也很难学习到有效的策略


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103212745.png)

更高效的方法：模仿学习预训练，快速掌握基本知识 + 强化学习优化，更有鲁棒性


### 模仿学习

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103213336.png)

#### 典型：seq2seq模型

[(R2R) Vision-and-Language Navigation: Interpreting Visually-Grounded Navigation Instructions in Real Environments](https://ieeexplore.ieee.org/document/8578485)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103214622.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103214637.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103214657.png)


 #### 数据增强：Speaker-Follower模型 
 [Speaker-Follower Models for Vision-and-Language Navigation](http://arxiv.org/abs/1806.02724)
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103214804.png)


可以进行一定的增强，但是没办法超越“专家”

所以

### 强化学习


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103220256.png)


Q-learning 价值函数

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103220721.png)


奖励函数是强化学习里面唯一的学习信号


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103221333.png)

稀疏奖励：最直接，是否到达目标为正奖励，直接以目标为导向，但奖励信号 但是困难 且不一定能收敛

稠密/几何奖励：根据目标距离去给奖励，能加速学习，但是这样会忽略指令，会走捷径，如穿过某个东西后到达某地

内在/语义奖励：解决几何奖励的缺陷，是否遵循指令


#### 典型：RCM模型，增强交叉模态匹配
[Reinforced Cross-Modal Matching and Self-Supervised Imitation Learning for Vision-Language Navigation](http://arxiv.org/abs/1811.10092)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103221542.png)


内在奖励：语义（路径保真度，语义一致性挂钩）


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103222842.png)
我的路径与文字是否匹配，不展开介绍

外在奖励：实时导航奖 + 成功抵达奖

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103222212.png)

终极策略：

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103222335.png)

优势函数
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103223127.png)


损失函数最小化-总分最大化 转化
梯度-优化方向
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103223428.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103223729.png)



### 混合方法：IL + RL

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103224011.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103224130.png)

---

#### 典型：VLN-R1

[VLN-R1: Vision-Language Navigation via Reinforcement Fine-Tuning](http://arxiv.org/abs/2506.17221)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103230835.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103230902.png)

**![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103230931.png)**


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103231006.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103231028.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251103230756.png)

---

## 第五章 视觉语言预训练模型

Vision Language Pretraining


### 泛化鸿沟


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105180001.png)


### 预训练范式
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105180308.png)


#### 自监督学习
从数据本身自动生成标签
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105210936.png)


领域内与领域外预训练
领域内：类导航数据，优点任务相关性强，直接服务导航，缺点，早期数据集规模小，成本高
领域外：使用图文对（如网页图片）。优点 数据规模大 多样性高，缺点，与导航任务差异大，缺乏时序和动作信息。


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105211455.png)



#### 经典的视觉语言任务

Masked Language Model
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105211619.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105211721.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105211812.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105212017.png)

---
### 预训练经典架构

#### PREVALENT
最早提出预训练的
[Towards Learning a Generic Agent for Vision-and-Language Navigation via Pre-training](http://arxiv.org/abs/2002.10638)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105213604.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105213645.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105213817.png)


#### AirBert
[Airbert: In-domain Pretraining for Vision-and-Language Navigation](http://arxiv.org/abs/2108.09105)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215318.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215412.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215441.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215638.png)

#### Recurrent VLN-BERT
[VLN-BERT: A Recurrent Vision-and-Language BERT for Navigation](https://ieeexplore.ieee.org/document/9578351)
可以用领域外的
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105214735.png)



![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105212610.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215757.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105215907.png)

### 预训练高级架构

#### BEVBERT
[BEVBert: Multimodal Map Pre-training for Language-guided Navigation](http://arxiv.org/abs/2212.04385)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105221641.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105221847.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105222312.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105222723.png)

---

### 微调

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105222849.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105222943.png)


这种范式是基于learning的

## 第六章 LLM与VLN的融合


### 传统VLN性能瓶颈
预训练的模型也可能对常识无法理解

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105224655.png)

### LLM的优势 强大的知识库
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105224857.png)
从预测到推理的转变


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105225203.png)

### IL&RL vs LLM
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105225352.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251105225534.png)



**CLIP**


### LLM的优势

NavGPT
高级规划器

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106132231.png)

NavCoT
[NavCoT: Boosting LLM-Based Vision-and-Language Navigation via Learning Disentangled Reasoning](http://arxiv.org/abs/2403.07376)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106133013.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106133119.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106133410.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106144722.png)


### LLM
#### NavGPT
[NavGPT: Explicit Reasoning in Vision-and-Language Navigation with Large Language Models](http://arxiv.org/abs/2305.16986)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106161418.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106161645.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106162105.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106162435.png)


#### NavGPT-2
[NavGPT-2: Unleashing Navigational Reasoning Capability for Large Vision-Language Models](http://arxiv.org/abs/2407.12366)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106162612.png)


#### March in Chat (MiC)
[March in Chat: Interactive Prompting for Remote Embodied Referring Expression](http://arxiv.org/abs/2308.10141)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106162946.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163221.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163306.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163435.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163447.png)


### 微调

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163640.png)


微调策略

PEFT LoRA

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106163850.png)

#### Navid框架
[NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation](http://arxiv.org/abs/2402.15852)
2024-05-28
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106164659.png)
端到端的

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106164749.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165037.png)

重点学习NaVid框架

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165218.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165316.png)


数据集使用的是VLN-CE
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165449.png)

### LLM的挑战和总结

#### 接地问题
抽象符号与物理数据感知 非具身的
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165601.png)


#### 幻觉问题
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165801.png)

#### Sim2Real Gap
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106165857.png)

缺乏**世界模型**，只有相关性 没有因果性
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170004.png)

未来应该 探索 世界模型，而不是仅仅增加数据和微调

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170124.png)


## 第七章 Air VLN

空中的模型和思路会不一样

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170531.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170605.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170742.png)

### 挑战

#### 三维路径规划与自由度控制
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106170957.png)

#### 感知
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106171144.png)

#### Sim2Real
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106171211.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106182635.png)


### 架构与模型

#### UAV-VLN
[UAV-VLN: End-to-End Vision Language guided Navigation for UAVs](http://arxiv.org/abs/2504.21432)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106182826.png)

端到端框架 四个步骤 预定义的离散的动作空间
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106183149.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106183206.png)

#### VLFly

[Grounded Vision-Language Navigation for UAVs with Open-Vocabulary Goal Understanding](http://arxiv.org/abs/2506.10756)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106183502.png)

模块化的架构
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106183627.png)
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106183612.png)


#### OpenFly
OpenFly-Agent
[OpenFly: A Comprehensive Platform for Aerial Vision-Language Navigation](http://arxiv.org/abs/2502.18041)
基于OpenVLA
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106184432.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106184649.png)


### Air VLN的生态

#### AirSim

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106220603.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106220750.png)

#### AerialVLN
[AerialVLN: Vision-and-Language Navigation for UAVs](https://ieeexplore.ieee.org/document/10378183/)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106220930.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106221012.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106221027.png)

#### OpenFly
[OpenFly: A Comprehensive Platform for Aerial Vision-Language Navigation](http://arxiv.org/abs/2502.18041)

不仅是数据集，还有生态
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106221129.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106221856.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106222515.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106222743.png)

#### AerialVLN vs OpenFly
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251106222824.png)




## 第八章 机器人中的视觉语言导航应用


### 仿真到物理世界


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117231813070.png)

#### 显著的性能下降
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117231824414.png)


#### 鸿沟解构
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117231956295.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117232331670.png)

分层，高层推理，底层执行



#### 弥合鸿沟
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117232417050.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117232532394.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117232635387.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251117232728356.png)


### 前沿架构

主要框架案例

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121124018421.png)



#### GVNav

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121124247171.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121124421540.png)

物理高度导致的视点不匹配问题，引发连锁性的失败
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121124458231.png)

核心模块
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121125040906.png)

整体框架
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121130240782.png)

局限
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121130340837.png)

LLM有高层推理、规划和常识运用的能力

#### SmartWay

以前的缺乏高层推理能力，从错误中纠正的能力
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121131111483.png)

增强路径点预测器
DINOv2
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121131415278.png)

MLLM多模态
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121132922041.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121132952441.png)

整体框架
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133134244.png)


局限
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133228841.png)
巨大计算开销，推理延迟，推理速度不够快

#### Navid

Navid的核心思想是构建一个“基于视频的大型视觉语言模型（VLM）”，以解决VLN中长期存在的泛化难题，特别是Sim2Real的迁移问题。

是端到到的

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133558316.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133642556.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133707543.png)

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133715082.png)



![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133735048.png)


#### Uni-Navid

![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133804678.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121133923881.png)

序列到序列的生成任务
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134057444.png)


![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134131584.png)

在线视觉令牌合并机制
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134234711.png)

分层
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134341764.png)

预见性的动作规划，异步
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134415756.png)


数据
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134451404.png)

局限和未来
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134525761.png)

## 课程总结

基础奠基：任务的诞生
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134721103.png)

Learning的角度
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134806544.png)

泛化能力突破：预训练
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134848764.png)

大模型时代 LLM
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134920352.png)

空中VLN
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121134958298.png)

具身化：Sim2Real
![](/obsidian/VLN/%E6%B7%B1%E8%93%9D%E8%AF%BE%E7%A8%8B/assets/VLN%E8%AF%BE%E7%A8%8B%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/file-20251121135009036.png)


