---






title: Project 1 MP3D基线模型讲解
date: 2025-11-26
lastmod: 2025-11-26
draft: false
summary: 讲解 Project1 Task2 中 Seq2Seq 基线模型的实现细节，并分析训练指标（SR、SPL、NavError）的预期趋势与含义。
tags:
- VLN
- Ubuntu
- 深蓝课程
- 项目
- Navigation
---

我们将讲解 Project1 Task2中 Seq2Seq 基线模型的正确实现细节，并重点分析训练过程中各项指标(如 SR,SPL, NavError)的预期趋势及其含义。

# 1.核心代码实现讲解

我们这次作业主要是复现一个基于 Seq2Seq 的 VLN 模型，在环境安装部分我们在作业说明中已经有了详细的教程，同学们如果有什么问题可以在群中提问，这里我们来主要讲解一下三个关键 TODO 部分的参考实现，以及模型训练后通过些指标来分析模型训练情况

## 1.1 语言编码器(Encoder)

这里我们需要补全 `self.lstm` 的定义。
参考实现
```python
# TODO:补充 self.lstm 的定义
# 提示:根据类中的参数和 LSTM 的工作原理,合理设置 self.lstm 的参数
# 注意考虑输入输出维度、层数、是否双向以及dropout_ratio等参数
self.lstm = nn.LSTM(embedding_size, hidden_size, self.num_layers,
    batch_first=True, dropout=dropout_ratio,
    bidirectional=bidirectional)
```

这里我们使用 nn.LSTM 作为编码器,
input_size 必须是 embedding_size，因为输入是词向量。
hidden_size 决定了编码器输出的特征维度。
batch_first=True 它使输入张量的维度是 (batch, seq_len, features)，更符合直觉。
bidirectional=True 是一个关键点。双向 LSTM 能让模型在编码一个词时，同时“看到”它前面和后面的上下文，这对于理解复杂的自然语言指令(例如“走到走廊尽头再左转”)至关重要。


## 1.2 动作解码器(Decoder)与注意力机制
这里我们需要补全注意力层 self.attention layer 的定义和使用。
参考实现(定义)：
```python
# TODO:补充 self.attention layer 的定义
# 提示:根据注意力机制的原理,定义一个SoftDotAttention 类的实例
# 注意考虑隐藏层维度等因素
self.attention_layer = SoftDotAttention(hidden_size)
```

正确实现（使用）：

```python
# TODO:补充 self.attention layer 的使用方法
# 提示:根据注意力机制的原理,将解码器 LSTM 的输出传递给注意力层
# 并根据注意力权重计算加权后的上下文信息
# 注意考虑输入输出维度等因素
h_tilde, alpha = self.attention_layer(h_1_drop, ctx, ctx_mask)
logit = self.decoder2action(h_tilde)
```

这里我们需要一个注意力模块，SoftDotAttention(hidden_size)是一个标准实现，它需要知道 hidden_size 以便匹配Query 和 Key 的维度。这是注意力机制的核心。

在解码的每一步，我们将解码器当前的隐藏状态(h_1_drop)作为 Query，将编码器所有的输出(ctx)作为 Key 和Value.

注意力层计算后，返回的h tilde 是一个加权平均的上下文向量，它动态地聚焦于当前导航步骤最相关的指令词汇。最后，我们使用这个“融合了注意力”的 h_tilde 来预测下一个动作 logit = self.decoder2action(h_tilde)，而不是使用原偰窘褓卻値袆掺櫨鄆性暸焘 h_1_drop。

## 1.3 性能评估:SPL (Success weighted by Path Length)
我们最后补全 SPL 指标的计算过程。
参考实现:

```python
# TODO:补充 spl 的计算过程
# 提示: SPL的定义,判断是否成功到达目标点,并计算相应的SPL值
# 注意考虑导航准确度、轨迹长度和最短路径长度等因素
if err &lt; self.error_margin: 
    spls.append(sp/max(length,sp))  
else:  
    spls.append(0)  
```

SPL 是 VLN 中最重要的指标之一，它同时考察了成功率和效率。
首先，必须检查是否成功，即导航误差 err 是否小于容忍阈值 self.error marqin(通常是3米)。
如果失败: SPL 得分为 0。
如果成功:得分是$SPL=\frac{L_{min}}{max(L_{pred},L_{min})}$
在代码中，sp 是最短路径 $L_{min}$，length 是agent的实际路径$L_{pred}$。

# 2.训练趋势与结果分析(重点)
---
当模型代码正确时，我们在训练过程中应该观察到一组特定且有意义的指标趋势，这里我们简单分析一下这些趋势的含义.

## 2.1 核心指标分析

1.导航误差(Nav Error)是一个下降趋势。模型刚开始时是随机的，误差会很高(例如 9-10 米)。随着训练，模型学会了如何走向目标，误差会稳步下降并最终收敛(例如 6-8 米),这是模型正在学习的最直接证据。误差不下降，说明模型没有学到东西。

2.成功率 (Success Rate)是一个上升趋势。与导航误差相反，成功率(SR)会从0开始稳步上升，并最终收敛(例如seen 30-40%，unseen 20-30%),这种情况表明模型成功停止在目标3 米内的次数越来越多。

3.路径加权成功率 (SPL)同样是上升趋势，但其值永远不会超过成功率(SR)。SPL 是衡量效率的指标。在我们测试的时候，如果如果两个模型对比最终SPL在 0.3或0.38。这之间的Gap意味着有 8% 的成功轨迹是因为“绕远路”而被 SPL惩罚了

4.路径长度 (Path Length)我们目前不会太在意他是一个上升趋势或者下降趋势了，只能作为t3指标，不是很重要，一般来说路径长短现阶段已经不能反应出我们模型真实的性能，我们更需要关注的是SR和SPL这两个t1的指标。



## 2.2 泛化能力问题

这是本次项目中最重要的分析点之一，同学们可以对比一下 val seen 和 val unseen 的所有指标，下面举个例子:

`val_seen的nav_error(~6%)低于 val_unseen的nav_error(~8%)。
val_seen的success_rate(~38%)高于 val_unseen的success_rate(~22%)。
val_seen的spl(~32%)高于 val_unseen的spl(~18%)。`


这就是泛化差距，val_seen (可见场景)是模型在训练时“见过”的房子。模型在这些熟悉的房子里表现很好。而val_unseen (未见场景)是模型从未见过的全新房子。模型在这里表现显著变差，说明它很难将学到的导航知识(例如“厨房通常长什么样”)迁移到全新的环境中。那这也是显然易见的，简单的 Seq2Seq 模型泛化能力其实比较差的，但是即使目前的阶段，泛化性依然是 VLN 领域需要解决的核心问题之一
最后总结一下，如果同学们能正常复现的话，那么作业结果应该是:随着迭代次数增加，导航误差降低，成功率和 SPL上升，这种情况一般就是训练成功了，而 seen 和 unseen 指标之间会有一些差距，即泛化能力不足。
