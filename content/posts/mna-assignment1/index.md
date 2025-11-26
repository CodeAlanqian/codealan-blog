---
title: "Assignment 1 of Advanced Numerical Analysis"
date: 2025-11-26T20:00:00+08:00
lastmod: 2025-11-26T20:00:00+08:00
summary: "作业 1：用割线法与二分法求 Z(t) 的前十个正根，并分析牛顿法与割线法在双重根处的收敛阶与误差常数。"
tags:
  - 数值分析
  - 数学
math: true
draft: false
---

龚易乾 12540026  
Advanced Numerical Analysis — Assignment 1

---

## Question 1

我们考虑函数

$$
Z(t) \approx 2 \sum_{n=1}^{N} \frac{1}{\sqrt{n}} \cos\bigl(\theta(t) - t \log n\bigr), 
\qquad N = \left\lfloor \sqrt{\frac{t}{2\pi}} \right\rfloor,
$$

其中

$$
\theta(t) \approx \frac{t}{2}\log \frac{t}{2\pi} - \frac{t}{2} - \frac{\pi}{8} + \frac{1}{48t} + \frac{7}{5760\,t^3}.
$$

**Task：** 使用割线法（必要时配合二分法）求出 \(Z(t)\) 的前十个正根。

### 1.1 方法分析

#### 1.1.1 Secant Method

Newton 法是求解非线性方程 \(f(x)=0\) 的经典方法，迭代格式为

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}.
$$

割线法是 Newton 法的一种变体，不需要显式计算导数，而是利用两个初始点构造割线来近似导数，其迭代格式为

$$
x_{n+1} = x_n - f(x_n)\,\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}.
$$

对本题，我们记 \(f(t)=Z(t)\)，选择两个靠近根的初值 \(t_0,t_1\)，则迭代格式为

$$
t_{k+1} = t_k - Z(t_k)\,\frac{t_k - t_{k-1}}{Z(t_k) - Z(t_{k-1})},
$$

迭代直至达到给定精度。

#### 1.1.2 Bisection Method

二分法是另一种求根方法，思想是：若连续函数 \(f(x)\) 在区间 \([a,b]\) 上满足 \(f(a)\cdot f(b)<0\)，则根据介值定理，该区间中至少存在一个根。算法步骤为：

1. 计算中点 \(c = \frac{a+b}{2}\)；
2. 若 \(f(c)=0\)，则 \(c\) 即为根；
3. 若 \(f(c)\cdot f(a) < 0\)，则根在 \([a,c]\)，令 \(b=c\)；
4. 否则根在 \([c,b]\)，令 \(a=c\)；
5. 重复上述过程，直至区间长度小于给定阈值。

在本题中，当割线法在某些区间内收敛缓慢或不收敛时，可以回退到二分法保证收敛。

### 1.2 数值实验

下面使用 Matlab 实现上述算法。

#### Step 1：定义 \(\theta(t)\)

```matlab
theta = @(t) (t./2).*log(t./(2*pi)) - t./2 - pi/8 ...
             + 1./(48*t) + 7./(5760*t.^3);
```

#### Step 2：定义 \(Z(t)\)

```matlab
function Zt = Zeta(t)
    theta = @(t) (t./2).*log(t./(2*pi)) - t./2 - pi/8 ...
                 + 1./(48*t) + 7./(5760*t.^3);
    N = floor(sqrt(t./(2.*pi)));
    n = 1:N;
    Zt = 2.*sum( (1./sqrt(n)) .* cos(theta(t) - t.*log(n)) );
end
```

#### Step 3：在区间 \([0.05,60]\) 上计算并绘制 \(Z(t)\)

```matlab
t = 0.05:0.05:60;
Z_values = arrayfun(@Zeta, t);
```

对应的曲线如下：

![Plot of Z(t)](/MNA/ass1/fig0.png)

_Figure 1: Plot of \(Z(t)\) on \([0.05,60]\)._

#### Step 4：扫描符号变化区间，构造初始根区间

```matlab
roots_guess = [];
roots_cnt = 0;
cnt = 0;
for i = 1:60/0.05-1
    cnt = cnt + 1;
    if Z_values(i) * Z_values(i+1) < 0
        roots_cnt = roots_cnt + 1;
        roots_guess(roots_cnt) = i * 0.05;
    end
end
```

当满足

$$
Z(t_i)\cdot Z(t_{i+1}) < 0
$$

时，$\([t_i,t_{i+1}]\)$ 内存在根，将左端点记为初始猜测值。

#### Step 5：定义割线法函数

设定停止准则：

- $\(|Z(t_k)| \le 0.5\times 10^{-10}\)$，或
- $\(|t_k - t_{k-1}| \le 0.5\times 10^{-12}\)$，或
- 迭代步数达到上限 `max_iters`。

```matlab
function root = secantMethod(root_guess)
    tk   = root_guess;
    tk_1 = root_guess + 0.05;
    iters = 0;
    max_iters = 1000;
    while abs(Zeta(tk)) > 0.5e-10 && ...
          abs(tk - tk_1) > 0.5e-12 && ...
          iters < max_iters
        tkk = tk - Zeta(tk) * (tk - tk_1) / (Zeta(tk) - Zeta(tk_1));
        tk_1 = tk;
        tk   = tkk;
        iters = iters + 1;
    end
    root = tk;
end
```

#### Step 6：对前若干个区间使用割线法求根

```matlab
secantMethod(roots_guess(3))  % 试算第三个根附近

roots = [];
for i = 1:10
    roots(i) = secantMethod(roots_guess(i));
end
disp("前十个正数解");
roots'

figure;
plot(t, Z_values, 'b-'); hold on;
yline(0, '--k');
plot(roots, zeros(size(roots)), 'ro', 'MarkerFaceColor', 'r');
xlabel('t');
ylabel('Z(t)');
title('Z(t) Function and its First 10 Zeros');
grid on;
```

得到的零点示意图如下：

![Zeros of Z(t), initial attempt](/MNA/ass1/fig1.png)

_Figure 2: First attempt at locating zeros of \(Z(t)\) using the secant method._

实验发现第三个零点附近收敛非常慢，导致该根位置不准确。原因可能是该处函数变化过快，割线法的步长控制不稳定。因此，当割线法在给定迭代步数内未收敛时，改用二分法进行修正。

#### Step 7：收敛缓慢时切换为二分法

在割线法函数中增加二分回退逻辑：

```matlab
function root = secantMethod(root_guess)
    tk   = root_guess;
    tk_1 = root_guess + 0.05;
    iters = 0;
    max_iters = 1000;
    while abs(Zeta(tk)) > 0.5e-10 && ...
          abs(tk - tk_1) > 0.5e-12 && ...
          iters < max_iters
        tkk = tk - Zeta(tk) * (tk - tk_1) / (Zeta(tk) - Zeta(tk_1));
        tk_1 = tk;
        tk   = tkk;
        iters = iters + 1;
    end

    % 若割线法在给定步数内未收敛，则改用二分法
    if iters >= max_iters
        iters = 0;
        tk   = root_guess;
        tk_1 = root_guess + 0.05;
        while abs(Zeta(tk)) > 0.5e-10 && ...
              abs(tk - tk_1) > 0.5e-12 && ...
              iters < max_iters
            tkk = (tk + tk_1) / 2;
            if Zeta(tk) * Zeta(tkk) < 0
                tk_1 = tkk;
            else
                tk = tkk;
            end
        end
    end

    root = tk;
end
```

最终得到的前十个正根为（保留全部有效数字）：

$$
\begin{aligned}
&14.517919629691189, \quad
20.654044969540138, \quad
25.132741228718082, \quad
30.731877908507784, \\
&32.688929806788373, \quad
37.716482062402093, \quad
40.758511514743816, \quad
43.460371685046312, \\
&47.824617076177333, \quad
50.003418594753931.
\end{aligned}
$$

对应的零点示意图为：

![Final zeros of Z(t)](/MNA/ass1/fig2.png)

_Figure 3: Final plot of the zeros of \(Z(t)\) after combining secant and bisection methods._

---

## Question 2

设 \(f\) 在根 \(x^\ast\) 附近足够光滑，且方程 \(f(x)=0\) 在 \(x=x^\ast\) 处有一重根（double root）：

$$
f(x^\ast)=0,\quad f'(x^\ast)=0,\quad f''(x^\ast)\ne 0.
$$

令误差 \(e_k = x_k - x^\ast\)。若序列 \(\{x_k\}\) 收敛到 \(x^\ast\)，并存在常数 \(C>0, p>0\)，使得

$$
\lim_{k\to\infty}\frac{|e_{k+1}|}{|e_k|^p} = C,
$$

则称 \(\{x_k\}\) 以阶数 \(p\) 收敛到 \(x^\ast\)，且 \(C\) 为渐近误差常数。

### 2.1 Taylor 展开

对 \(f(x)\) 在 \(x^\ast\) 处做 Taylor 展开，有

$$
f(x) = f(x^\ast) + f'(x^\ast)(x-x^\ast) + \frac{f''(x^\ast)}{2}(x-x^\ast)^2 + \cdots.
$$

由于 \(f(x^\ast)=0\)、\(f'(x^\ast)=0\)，得到主导项

$$
f(x) = \frac{f''(x^\ast)}{2}(x-x^\ast)^2 + \cdots.
$$

令 \(x_k = e_k + x^\ast\)，则

$$
f(x_k) = \frac{f''(x^\ast)}{2}(x_k - x^\ast)^2
       = \frac{f''(x^\ast)}{2} e_k^2.
$$

类似地，对导数 \(f'(x)\) 展开：

$$
f'(x) = f'(x^\ast) + f''(x^\ast)(x-x^\ast) + \cdots
      = f''(x^\ast)(x-x^\ast) + \cdots,
$$

于是

$$
f'(x_k) = f''(x^\ast)(x_k - x^\ast)
        = f''(x^\ast) e_k.
$$

### 2.2 Newton's Method

Newton 迭代为

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}.
$$

代入上式的近似表达：

$$
x_{k+1} 
 = x_k - \frac{\frac{f''(x^\ast)}{2} e_k^2}{f''(x^\ast) e_k}
 = x_k - \frac{1}{2} e_k.
$$

因此

$$
e_{k+1} = x_{k+1} - x^\ast
        = x_k - \frac{1}{2} e_k - x^\ast
        = e_k - \frac{1}{2} e_k
        = \frac{1}{2} e_k.
$$

于是

$$
\lim_{k\to\infty}\frac{|e_{k+1}|}{|e_k|^p}
 = \lim_{k\to\infty}\frac{\left|\frac{1}{2}e_k\right|}{|e_k|^p}
 = \frac{1}{2}\,\lim_{k\to\infty}|e_k|^{1-p}.
$$

要使极限有限且非零，需要 \(1-p=0\Rightarrow p=1\)。  
因此 Newton 法在双重根处的**收敛阶为 1**，**渐近误差常数为 \(\tfrac{1}{2}\)**。

### 2.3 Secant Method

割线法迭代为

$$
x_{k+1} = x_k - f(x_k)\,\frac{x_k - x_{k-1}}{f(x_k) - f(x_{k-1})}.
$$

利用

$$
f(x_k) = \frac{f''(x^\ast)}{2} e_k^2,\qquad
f(x_{k-1}) = \frac{f''(x^\ast)}{2} e_{k-1}^2,
$$

可得

$$
x_{k+1} = x_k - \frac{\tfrac{f''(x^\ast)}{2} e_k^2 (e_k - e_{k-1})}
                      {\tfrac{f''(x^\ast)}{2} e_k^2 - \tfrac{f''(x^\ast)}{2} e_{k-1}^2}
        = x_k - \frac{e_k^2 (e_k - e_{k-1})}{e_k^2 - e_{k-1}^2}
        = x_k - \frac{e_k^2}{e_k + e_{k-1}}.
$$

因此

$$
e_{k+1} = x_{k+1} - x^\ast
        = e_k - \frac{e_k^2}{e_k + e_{k-1}}
        = \frac{e_k e_{k-1}}{e_k + e_{k-1}}.
$$

若假设误差呈线性收敛，即 \(e_{k+1} \sim \lambda e_k\)、且 \(e_{k-1}\sim e_k/\lambda\)（\(\lambda<1\)），则有

$$
e_{k+1}
 = \frac{e_k e_{k-1}}{e_k + e_{k-1}}
 \approx \frac{e_k \cdot (e_k/\lambda)}{e_k + e_k/\lambda}
 = \frac{e_k}{1+\lambda}.
$$

于是

$$
\lambda = \frac{1}{1+\lambda}
 \quad\Rightarrow\quad
\lambda^2 + \lambda - 1 = 0.
$$

解得

$$
\lambda = \frac{-1 + \sqrt{5}}{2} \approx 0.618.
$$

从而

$$
\lim_{k\to\infty}\frac{|e_{k+1}|}{|e_k|^p}
 = \lim_{k\to\infty}\frac{\left|\frac{e_k}{1+\lambda}\right|}{|e_k|^p}
 = \frac{1}{1+\lambda}\,\lim_{k\to\infty}|e_k|^{1-p}.
$$

为使极限有限非零，需要 \(1-p=0\Rightarrow p=1\)，于是割线法在双重根处的**收敛阶为 1**，**渐近误差常数为**

$$
C = \frac{1}{1+\lambda}
  = \frac{1}{1 + \frac{-1 + \sqrt{5}}{2}}
  = \frac{2}{1+\sqrt{5}}
  \approx 0.618.
$$

---

## Appendix：Question 1 代码

```matlab
clc; clear; close all;
format long;
%% 定义 t 序列
t = 0.05:0.05:60;

%% 定义 theta 函数
theta = @(t) (t./2).*log(t./(2*pi)) - t./2 - pi/8 ...
             + 1./(48*t) + 7./(5760*t.^3);

%% 计算 Z(t), t 取值 [0.05,60], 步长 0.05, 绘制图像
Z_values = arrayfun(@Zeta, t);
figure;
plot(t, Z_values, 'b-'); hold on;
yline(0, '--k');

%% 扫描零点范围，根据 Z(a)*Z(b)<0 记录 a 到 roots_guess
roots_guess = [];
roots_cnt = 0;
cnt = 0;
for i = 1:60/0.05-1
    cnt = cnt + 1;
    if Z_values(i) * Z_values(i+1) < 0
        roots_cnt = roots_cnt + 1;
        roots_guess(roots_cnt) = i * 0.05;
    end
end

roots_guess;

%% 使用割线法求零点并展示前十个正数解
secantMethod(roots_guess(3))
roots = [];
for i = 1:10
    roots(i) = secantMethod(roots_guess(i));
end
disp("前十个正数解");
roots'

%% 绘制图像
figure;
plot(t, Z_values, 'b-'); hold on;
yline(0, '--k');
plot(roots, zeros(size(roots)), 'ro', 'MarkerFaceColor', 'r');
xlabel('t');
ylabel('Z(t)');
title('Z(t) Function and its First 10 Zeros');
grid on;

%% 定义 Zeta 函数
function Zt = Zeta(t)
    theta = @(t) (t./2).*log(t./(2*pi)) - t./2 - pi/8 ...
                 + 1./(48*t) + 7./(5760*t.^3);
    N = floor(sqrt(t./(2.*pi)));
    n = 1:N;
    Zt = 2.*sum( (1./sqrt(n)) .* cos(theta(t) - t.*log(n)) );
end

%% 割线法
% 发现第三个点使用割线法不收敛，故不收敛时改为二分法求解。
function root = secantMethod(root_guess)
    tk   = root_guess;
    tk_1 = root_guess + 0.05;
    iters = 0;
    max_iters = 1000;
    while abs(Zeta(tk)) > 0.5e-10 && ...
          abs(tk - tk_1) > 0.5e-12 && ...
          iters < max_iters
        tkk = tk - Zeta(tk) * (tk - tk_1) / (Zeta(tk) - Zeta(tk_1));
        tk_1 = tk;
        tk   = tkk;
        iters = iters + 1;
    end
    % 不收敛改为二分法
    if iters >= max_iters
        iters = 0;
        tk   = root_guess;
        tk_1 = root_guess + 0.05;
        while abs(Zeta(tk)) > 0.5e-10 && ...
              abs(tk - tk_1) > 0.5e-12 && ...
              iters < max_iters
            tkk = (tk + tk_1) / 2;
            if Zeta(tk) * Zeta(tkk) < 0
                tk_1 = tkk;
            else
                tk = tkk;
            end
        end
    end
    root = tk;
end
```
