---
title: "BibTeX 悬停预览示例"
date: 2025-11-27
lastmod: 2025-11-27
tags:
- Zotero
- Notes
- BibTeX
---

本文演示如何在博客中为论文笔记添加 BibTeX 悬停预览与一键跳转。

### 效果示例

将鼠标移动到下面这条文献标题上方，可以看到 BibTeX 气泡窗口，点击标题会跳转到对应的 arXiv 页面：

{{< bibref title="AerialVLN: Vision-and-Language Navigation for UAVs" url="https://arxiv.org/abs/2403.12345" >}}
@inproceedings{liu2023aerialvln,
  title={AerialVLN: Vision-and-Language Navigation for UAVs},
  author={Liu, A. and Others},
  booktitle={Proceedings of the 2023 IEEE International Conference on Robotics and Automation (ICRA)},
  year={2023}
}
{{< /bibref >}}

### 在论文笔记中使用

在任意 Markdown 文章（例如 Zotero 导出的论文笔记）中，直接插入上面的 `bibref` shortcode 即可复用同样的交互效果。

