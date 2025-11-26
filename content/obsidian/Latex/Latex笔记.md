---



title: Latex笔记
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- Latex
- Ubuntu
---
# Latex笔记

## 支持中文编译

```latex
\usepackage{ctex}
\usepackage{anyfontsize}
```

编译模式改为XeLaTex



## 插入的图片使其紧跟文字后面

[LaTeX 中插入图片使其紧跟插入的文字之后 - CuriousZero - 博客园](https://www.cnblogs.com/shenxiaolin/p/7576373.html)

```latex
\usepackage{float}

\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{fig.png}
\caption{xxx}
\end{figure}
```



## 插入代码

[LaTeX 插入代码块 - Undefined443 - 博客园](https://www.cnblogs.com/Undefined443/p/18155226)

```latex
\usepackage{fancyvrb}
\usepackage{xcolor}  % 用到了 \color 命令

\begin{Verbatim}[numbers=left, frame=single, formatcom=\color{black}, fontsize=\small]
theta = @(t) (t./2).*log(t./(2*pi));
\end{Verbatim}
```





matlab 类型

```latex
\usepackage[dvipnames]{xcolor}  % 用到了 \color 命令
\usepackage{listings}

\lstdefinestyle{MatlabStyle}{
    language=Matlab,
    basicstyle=\small\ttfamily,
    numbers=left,
    numberstyle=\tiny,
    stepnumber=1,
    frame=single,
    rulecolor=\color{black},
    backgroundcolor=\color{gray!5},
    keywordstyle=\color{blue}\bfseries,
    commentstyle=\color{green!50!black}\itshape,
    stringstyle=\color{orange!90!black},
    breaklines=true,
    showstringspaces=false,
    captionpos=b
}


\begin{lstlisting}[style=MatlabStyle]
xxx
\end{lstlisting}
```

