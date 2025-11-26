---
title: "Assignment 2 of Advanced Numerical Analysis"
date: 2025-11-27T04:00:00+08:00
lastmod: 2025-11-27T04:10:00+08:00
summary: "作业 2：高斯消去带部分选主元、LU 分解、Gauss-Seidel 迭代与 QR 算法求特征值。"
tags:
  - 数值分析
  - 数学
math: true
draft: false
---

龚易乾 12540026  
Advanced Numerical Analysis — Assignment 2

---

## Question 1

Use Gaussian elimination with partial pivoting to solve the following linear system (use four-digit rounding arithmetic):

$$
\begin{gathered}
x_{1}+20x_{2}-x_{3}+0.001x_{4}=0 \\\
2x_{1}-5x_{2}+30x_{3}-0.1x_{4}=1 \\\
5x_{1}+x_{2}-100x_{3}-10x_{4}=0 \\\
2x_{1}-100x_{2}-x_{3}+x_{4}=0.
\end{gathered}
$$

矩阵形式为

<div class="math">
$$
A =
\begin{bmatrix}
1 & 20 & -1 & 0.001 \\\ 2 & -5 & 30 & -0.1 \\\ 5 & 1 & -100 & -10 \\\ 2 & -100 & -1 & 1
\end{bmatrix}, \qquad
b =
\begin{bmatrix}
0 \\\\ 1 \\\\ 0 \\\\ 0
\end{bmatrix}.
$$
</div>

增广矩阵为

<div class="math">
$$
[A\,|\,b] =
\begin{bmatrix}
1 & 20 & -1 & 0.001 & 0 \\\ 2 & -5 & 30 & -0.1 & 1 \\\ 5 & 1 & -100 & -10 & 0 \\\ 2 & -100 & -1 & 1 & 0
\end{bmatrix}.
$$
</div>

### 部分选主元高斯消去思路

对于每一列：

1. 在当前列自当前行到最后一行中，找到绝对值最大的元素作为主元；  
2. 交换当前行与主元所在行；  
3. 利用当前主元对下面各行做消元，将主元下方元素消为 0。

Matlab 代码实现如下。

#### 定义系数矩阵和右端向量

```matlab
%% Define A and b
A = [1, 20, -1, 0.001;
     2, -5, 30, -0.1;
     5, 1, -100, -10;
     2, -100, -1, 1; ];
b = [0;1;0;0];
```

#### Gaussian elimination with partial pivoting

```matlab
function x = Guass_elimination_pivot(A, b)
Ab = [A b];            % Augmented matrix
N = size(Ab,1);        % number of rows
for p = 1:N-1
    temp = Ab(p,p);
    idx  = p;          % find pivot row
    for r = p+1:N
        if abs(Ab(r,p)) > temp
            idx  = r;
            temp = Ab(r,p);
        end
    end

    % exchange row p and row idx
    AA = Ab(p,p:N+1);          % store original row
    Ab(p,p:N+1)   = Ab(idx,p:N+1);
    Ab(idx,p:N+1) = AA;

    % Gaussian elimination
    for r = p+1:N
        idxc = p+1:N+1;
        Ab(r,idxc) = Ab(r,idxc) - Ab(p,idxc) * (Ab(r,p)/Ab(p,p));
        Ab(r,p)    = 0;
    end
end
end
```

消元后得到上三角增广矩阵

<div class="math">
$$
[U\,|\,c] \approx
\begin{bmatrix}
5.0000 & 1.0000   & -100.0000 & -10.0000 & 0 \\\ 0 & -100.4000 & 39.0000 & 5.0000   & 0 \\\ 0 & 0 & 67.9024  & 3.6311   & 1.0000 \\\ 0 & 0 & 0 & 1.5597   & -0.3931
\end{bmatrix}.
$$
</div>

#### 上三角回代

```matlab
function x = upper_triangle_solver(U, b)
N = size(U,1);
x = zeros(N,1);
for n = N:-1:1
    temp = 0;
    for t = 1:N-n
        if N-n ~= 0
            temp = temp + x(n+t) * U(n,n+t);
        end
    end
    temp = b(n) - temp;
    x(n) = temp / U(n,n);
end
end
```

最终得到线性方程组的解：

<div class="math">
$$
x \approx
\begin{bmatrix}
0.0604 \\\\ -0.0016 \\\\ 0.0282 \\\\ -0.2520
\end{bmatrix}.
$$
</div>

详细代码见附录 \ref{sec:appendix-q1}。

---

## Question 2

Use LU factorization to solve the following linear system:

<div class="math">
$$
\begin{bmatrix}
2 & -1 & 0 & 0 & 0 \\\ -1 & 2 & -1 & 0 & 0 \\\ 0 & -1 & 2 & -1 & 0 \\\ 0 & 0 & -1 & 2 & -1 \\\ 0 & 0 & 0 & -1 & 2
\end{bmatrix}
 x =
\begin{bmatrix}
1 \\\\ 0 \\\\ 0 \\\\ 0 \\\\ 1
\end{bmatrix}.
$$
</div>

LU 分解的基本思想是将矩阵 \(A\) 分解为下三角矩阵 \(L\) 与上三角矩阵 \(U\) 的乘积：

$$
A = LU.
$$

然后通过两步求解系统：

1. 先解 \(Ly = b\)（前代）；  
2. 再解 \(Ux = y\)（回代）。

对给定的五对角结构矩阵，可以得到

<div class="math">
$$
L =
\begin{bmatrix}
1 & 0 & 0 & 0 & 0 \\\ -\tfrac{1}{2} & 1 & 0 & 0 & 0 \\\ 0 & -\tfrac{2}{3} & 1 & 0 & 0 \\\ 0 & 0 & -\tfrac{3}{4} & 1 & 0 \\\ 0 & 0 & 0 & -\tfrac{4}{5} & 1
\end{bmatrix},
\qquad
U =
\begin{bmatrix}
2 & -1 & 0 & 0 & 0 \\\ 0 & \tfrac{3}{2} & -1 & 0 & 0 \\\ 0 & 0 & \tfrac{4}{3} & -1 & 0 \\\ 0 & 0 & 0 & \tfrac{5}{4} & -1 \\\ 0 & 0 & 0 & 0 & \tfrac{6}{5}
\end{bmatrix}.
$$
</div>

### 前代：求解 \(Ly=b\)

根据下三角方程组逐步求解：

$$
\begin{aligned}
y_1 &= 1,\\\
-\tfrac{1}{2}y_1 + y_2 &= 0 \;\Rightarrow\; y_2 = \tfrac{1}{2},\\\
-\tfrac{2}{3}y_2 + y_3 &= 0 \;\Rightarrow\; y_3 = \tfrac{1}{3},\\\
-\tfrac{3}{4}y_3 + y_4 &= 0 \;\Rightarrow\; y_4 = \tfrac{1}{4},\\\
-\tfrac{4}{5}y_4 + y_5 &= 1 \;\Rightarrow\; y_5 = \tfrac{6}{5}.
\end{aligned}
$$

### 回代：求解 \(Ux=y\)

从最后一行开始回代：

$$
\begin{aligned}
\tfrac{6}{5}x_5 &= \tfrac{6}{5} \;\Rightarrow\; x_5 = 1, \\\
\tfrac{5}{4}x_4 - x_5 &= \tfrac{1}{4} \;\Rightarrow\; x_4 = 1, \\\
\tfrac{4}{3}x_3 - x_4 &= \tfrac{1}{3} \;\Rightarrow\; x_3 = 1, \\\
\tfrac{3}{2}x_2 - x_3 &= \tfrac{1}{2} \;\Rightarrow\; x_2 = 1, \\\
2x_1 - x_2 &= 1 \;\Rightarrow\; x_1 = 1.
\end{aligned}
$$

最终解向量为

<div class="math">
$$
x =
\begin{bmatrix}
1 \\\\ 1 \\\\ 1 \\\\ 1 \\\\ 1
\end{bmatrix}.
$$
</div>

LU 分解与前后代的 Matlab 代码见附录 \ref{sec:appendix-q2}。

---

## Question 3

Use Gauss–Seidel iteration to solve the following band system:

$$
\begin{aligned}
12x_{1} - 2x_{2} + x_{3} &= 5, \\\
-2x_{1} + 12x_{2} - 2x_{3} + x_{4} &= 5, \\\
x_{1} - 2x_{2} + 12x_{3} - 2x_{4} + x_{5} &= 5, \\\
x_{2} - 2x_{3} + 12x_{4} - 2x_{5} + x_{6} &= 5, \\\
&\vdots \\\
x_{46} - 2x_{47} + 12x_{48} - 2x_{49} + x_{50} &= 5, \\\
x_{47} - 2x_{48} + 12x_{49} - 2x_{50} &= 5, \\\
x_{48} - 2x_{49} + 12x_{50} &= 5.
\end{aligned}
$$

该矩阵只在主对角线以及相邻两条对角线上有非零元素，是一个带状矩阵。采用 Gauss–Seidel 迭代格式：

$$
x_i^{(k+1)} =
\frac{b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)}
          - \sum_{j=i+1}^{n} a_{ij} x_j^{(k)}}{a_{ii}},
\quad i=1,\dots,n.
$$

### Matlab 实现（构造矩阵与主迭代）

```matlab
N = 50;
A = zeros(N,N);
b = 5*ones(N,1);
x = zeros(N,1);

% construct the band matrix A
for i = 1:N
    A(i,i) = 12;

    if i >= 2
        A(i-1,i) = -2;
        A(i,i-1) = -2;
    end

    if i >= 3
        A(i-2,i) = 1;
        A(i,i-2) = 1;
    end
end

tol      = 1e-9;
max_iter = 1000;

for k = 1:max_iter
    x_old = x;
    for i = 1:N
        % A(i,i+1:N)*x(i+1:N) 使用新迭代值
        temp1 = A(i,i+1:N) * x(i+1:N);
        % A(i,1:i-1)*x_old(1:i-1) 使用上一轮值
        temp2 = A(i,1:i-1) * x_old(1:i-1);
        x(i)  = (b(i) - temp1 - temp2) / A(i,i);
    end
    if sqrt((sum(x) - sum(x_old))^2) < tol
        break;
    end
end
```

数值结果收敛到一个接近常数 \(0.5\) 的向量，在两端略有边界效应。示意为

$$
x \approx
\begin{pmatrix}
0.4638 & 0.5373 & 0.5090 & 0.4982 & 0.4989 & 0.5000 & \cdots & 0.4989 & 0.4982 & 0.5090 & 0.5373 & 0.4638
\end{pmatrix}^{\!\top}.
$$

详细代码见附录 \ref{sec:appendix-q3}。

---

## Question 4

Write a program to find all the eigenvalues of the following matrix:

<div class="math">
$$
A =
\begin{bmatrix}
1 & 2 & -1 \\\ 1 & 0 & 1 \\\ 4 & -4 & 5
\end{bmatrix}.
$$
</div>

理论上，特征值可以通过特征多项式求解：

$$
\det(A - \lambda I) = 0.
$$

计算

<div class="math">
$$
A - \lambda I =
\begin{bmatrix}
1-\lambda & 2 & -1 \\\ 1 & -\lambda & 1 \\\ 4 & -4 & 5-\lambda
\end{bmatrix}.
$$
</div>

利用三阶行列式展开：

<div class="math">
$$
\det(A - \lambda I)
= (1-\lambda)
\begin{vmatrix}
-\lambda & 1\\ -4 & 5-\lambda
\end{vmatrix}
-2
\begin{vmatrix}
1 & 1 \\ 4 & 5-\lambda
\end{vmatrix}
-1
\begin{vmatrix}
1 & -\lambda \\ 4 & -4
\end{vmatrix}.
$$
</div>

化简得到

$$
\det(A - \lambda I)
= (1-\lambda)(\lambda-2)(\lambda-3).
$$

因此特征值为

$$
\lambda_1 = 1,\quad
\lambda_2 = 2,\quad
\lambda_3 = 3.
$$

在实现上，不使用内置 `eig`，而是通过 **QR 迭代** 计算全部特征值：  
对初始矩阵 \(A_0=A\)，重复进行

$$
A_k = Q_k R_k,\qquad
A_{k+1} = R_k Q_k,
$$

其中 \(A_k = Q_k R_k\) 为 Householder QR 分解。当 \(A_k\) 收敛为上三角矩阵时，其对角线即为特征值。  
Matlab 实现（含 Householder QR）见附录 \ref{sec:appendix-q4}。

---

## Appendix

### Appendix A: Code of Question 1
\label{sec:appendix-q1}

```matlab
clc; clear; close all;
%% Define A and b
A = [1, 20, -1, 0.001;
     2, -5, 30, -0.1;
     5, 1, -100, -10;
     2, -100, -1, 1; ];
b = [0;1;0;0];

%% Solve the equation using Gaussian elimination
x = Guass_elimination_pivot(A, b)

x_matlab = A\b
x - x_matlab

%% function
function x = Guass_elimination_pivot(A, b)
Ab = [A b]; % Augmented matrix
N = size(Ab,1);
for p = 1:N-1
    temp = Ab(p,p);
    idx  = p;
    for r = p+1:N
        if abs(Ab(r,p)) > temp
            idx  = r;
            temp = Ab(r,p);
        end
    end

    % exchange row p and row idx
    AA = Ab(p,p:N+1);
    Ab(p,p:N+1)   = Ab(idx,p:N+1);
    Ab(idx,p:N+1) = AA;

    % Gaussian elimination
    for r = p+1:N
        idxc = p+1:N+1;
        Ab(r,idxc) = Ab(r,idxc) - Ab(p,idxc) * (Ab(r,p)/Ab(p,p));
        Ab(r,p)    = 0;
    end
end
Ab
x = upper_triangle_solver(Ab(1:N,1:N), Ab(:,N+1));
end

%% upper triangle solver
function x = upper_triangle_solver(U, b)
N = size(U,1);
x = zeros(N,1);
for n = N:-1:1
    temp = 0;
    for t = 1:N-n
        if N-n ~= 0
            temp = temp + x(n+t) * U(n,n+t);
        end
    end
    temp = b(n) - temp;
    x(n) = temp / U(n,n);
end
end
```

### Appendix B: Code of Question 2
\label{sec:appendix-q2}

```matlab
clc; clear; close all;

A = [
2,-1,0,0,0;
-1,2,-1,0,0;
0,-1,2,-1,0;
0,0,-1,2,-1;
0,0,0,-1,2;
];

b = [1,0,0,0,1]';

[P,L,U] = PLU(A);
y = lower_triangle_solver(L,b)
x = upper_triangle_solver(U,y)
x_mat = A\b
x - x_mat

%% PLU factorization
function [P,L,U] = PLU(A)
N = size(A,1);
P = eye(N);
L = eye(N);
U = A;

for p = 1:N-1
    temp = U(p,p);
    idx  = p;
    for r = p+1:N
        if abs(U(r,p)) > temp
            idx  = r;
            temp = U(r,p);
        end
    end

    % exchange row p and row idx
    temp_U = U(p,1:N);
    temp_P = P(p,1:N);
    U(p,1:N) = U(idx,1:N);
    U(idx,1:N) = temp_U;
    P(p,1:N) = P(idx,1:N);
    P(idx,1:N) = temp_P;

    % elimination
    for r = p+1:N
        idxc = p+1:N;
        tmp = U(r,p) / U(p,p);
        U(r,idxc) = U(r,idxc) - U(p,idxc) * tmp;
        U(r,p)    = tmp;
    end
end

for r = 2:N
    L(r,1:r-1) = U(r,1:r-1);
    U(r,1:r-1) = 0;
end

P
L
U
L*U - P*A
end

%% upper triangle solver
function x = upper_triangle_solver(U, b)
N = size(U,1);
x = zeros(N,1);
for n = N:-1:1
    temp = 0;
    for t = 1:N-n
        if N-n ~= 0
            temp = temp + x(n+t) * U(n,n+t);
        end
    end
    temp = b(n) - temp;
    x(n) = temp / U(n,n);
end
end

%% lower triangle solver
function x = lower_triangle_solver(L, b)
N = size(L,1);
x = zeros(N,1);
for n = 1:N
    temp = 0;
    for t = 1:N-1
        if n ~= 1
            temp = temp + x(t) * L(n,t);
        end
    end
    temp = b(n) - temp;
    x(n) = temp / L(n,n);
end
end
```

### Appendix C: Code of Question 3
\label{sec:appendix-q3}

```matlab
clc; clear; close all;
N = 50;
A = zeros(N,N);
b = 5*ones(N,1);

for i = 1:N
    A(i,i) = 12;

    if i >= 2
        A(i-1,i) = -2;
        A(i,i-1) = -2;
    end

    if i >= 3
        A(i-2,i) = 1;
        A(i,i-2) = 1;
    end
end

x        = zeros(N,1);
tol      = 1e-9;
max_iter = 1000;

x_mat = A\b;

for k = 1:max_iter
    x_old = x;
    for i = 1:N
        temp1 = A(i,i+1:N) * x(i+1:N);
        temp2 = A(i,1:i-1) * x_old(1:i-1);
        x(i)  = (b(i) - temp1 - temp2) / A(i,i);
    end
    if sqrt((sum(x) - sum(x_old))^2) < tol
        break;
    end
end

x - x_mat
```

### Appendix D: Code of Question 4
\label{sec:appendix-q4}

```matlab
clc; clear; close all;
A = [1, 2, -1;
     1, 0, 1;
     4, -4, 5];

maxIter = 1000;
tol     = 1e-12;

Ak = A;

for k = 1:maxIter
    % QR decomposition
    [Q, R] = qr_function(Ak);

    % Form next iteration matrix
    Ak = R * Q;

    % Check convergence: off-diagonal elements → 0
    offdiag = Ak - diag(diag(Ak));
    if norm(offdiag, 'fro') < tol
        break;
    end
end

eigvals_QR = diag(Ak)

%% Householder QR
function [Q, R] = qr_function(A)
N = size(A,1);
R = A;
Q = eye(N);
for k = 1:N-1
    x = R(k:N, k);
    v = x;
    v(1) = v(1) - norm(x);
    v = v / norm(v);
    H_sub = eye(N-k+1) - 2 * v * v';
    H = eye(N);
    H(k:N, k:N) = H_sub;
    R = H * R;
    Q = Q * H;
end
end
```
