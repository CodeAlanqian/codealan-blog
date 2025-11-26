---






title: VLN项目学习笔记
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
# VLN学习笔记


> [!quote|#5fb236]+ Test
> Hello


xhost＋



```bash
docker run -itd --gpus all \
    -v /dev/shm:/dev/shm \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd)/data:/root/VLN-CE/data \
    -e DISPLAY=$DISPLAY \
    hccz95/vlnce:main
```



test 

```bash
python run.py --exp-config vlnce_baselines/config/r2r_baselines/nonlearning.yaml --run-type eval
```



>[!quote|#5fb236]+ Reference
>
In this section, we review two types of closely related work: UAV navigation and Ground-based VLN. [(p. 15385)](zotero://open-pdf/library/items/BWJFKXVW?page=15385&annotation=ICLKE8KQ)

> [!quote]+ <span style="color:#5fb236;">Reference</span>
> In this section, we review ...
