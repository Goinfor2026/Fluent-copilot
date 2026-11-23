---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - mhd
  - lorentz-force
  - addon-module
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 磁流体动力学（MHD）

## 摘要

User's Guide 2026 R1 Part III / Chapter 34 "Modeling Magnetohydrodynamics"（PDF pp. 3635–3658，六节）。**本页全章完成（批次 99，pp. 3635–3658）**：MHD add-on 模块分析导电流体在恒定（DC）或振荡（AC）电磁场下的行为——实现架构（感应方程/电位方程走 UDS、MHD 变量走 UDM）、模块使用（加载、两种 MHD 方法、外磁场 Patch/Import、四类壁面边界、求解控制）、使用指南、磁场定义与外磁场数据文件格式。理论见 Theory Guide "Modeling Magnetohydrodynamics"（Chapter 21，式号 21.x 由本章引用）。

## 34.1 引言（p. 3635）

- MHD = 外加电磁场与导电流体流动的相互作用；支持 **DC 与 AC 场**；外磁场可由内置函数生成或**导入用户数据文件**。
- 多相兼容：与 **DPM、VOF、Eulerian 多相**兼容，包括离散相对混合物电导率的影响。

## 34.2 实现（pp. 3635–3637）

UDF 形式的 add-on 模块，运行时加载；**磁感应方程（Theory Guide Eq 21.14/21.16）与电位方程（Eq 21.22）经 UDS 输运方程求解**；外磁场数据、电流密度、Lorentz 力、Joule 热存于 UDM；经 MHD Model GUI 与 TUI 命令设置。

- **34.2.1 方程求解**：感应方程 = 2D 解 2 个、3D 解 3 个标量方程（感应磁场矢量的笛卡尔分量）；电位方程 = 1 个标量。通量与扩散率用 `DEFINE_UDS_FLUX(mhd_flux,...)` 与 `DEFINE_DIFFUSIVITY(mhd_magnetic_diffusivity,...)`；源项用 `DEFINE_SOURCE(mhd_mag_source,...)` / `DEFINE_SOURCE(mhd_phi_source,...)`；瞬态附 `DEFINE_UDS_UNSTEADY(mhd_unsteady_source,...)`。**方程也可在固体区求解**（忽略流体速度项）；多相流只在混合物域求解。壁面边界用 `DEFINE_PROFILE(mhd_bc_...)` 实现：外边界三种——电绝缘、导电、"薄壁"（沿边界法向假设一维磁/电位扩散，需指定壁面材料与厚度）；内边界（固/固、固/液之间）用**耦合边界条件**。
- **34.2.2 MHD 变量计算**：感应电流密度矢量、感应电场矢量、Lorentz 力矢量、Joule 热存 UDM；`DEFINE_ADJUST(mhd_adjust,...)` 每迭代开始时用上一迭代的感应磁场更新。
- **34.2.3 与流动交互**：动量方程加 Lorentz 力（`DEFINE_SOURCE(mhd_mom_source,...)`）；能量方程加 Joule 热源（`DEFINE_SOURCE(mhd_energy_source,...)`）。
- **34.2.4 与 DPM 交互**：带电颗粒的 Lorentz 力经 `DEFINE_DPM_BODY_FORCE(mhd_dpm_force,...)`；`DEFINE_DPM_SOURCE(mhd_dpm_source,...)` 更新单元内离散相体积分数与体积加权电导率。
- **34.2.5 通用 UDF**：`DEFINE_INIT(mhd_init,...)`（case 初始化时设外磁场并初始化参数与变量）、`DEFINE_ADJUST(mhd_adjust,...)`。

## 34.3 模块使用（pp. 3637–3652）

### 34.3.1–34.3.2 安装与加载（pp. 3637–3639）

`addons/mhd`（UDF 库 + 预编译 Scheme 库）；**须先有有效 case**。两种加载：ribbon **MHD Model...**（加载后 Enable MHD 自动勾选）或 TUI `define/models/addon-module` → 模块号 **1**；加载完成提示 `Addon Module: mhd...loaded!`。**加载成功即自动完成基础设置**：默认 MHD 方法、分配并命名 UDS/UDM、全部 UDF 挂钩（初始化/adjust/通量/非稳定项/源项/动量与能量附加源）、内外边界默认 MHD 边界条件、默认模型参数；case 设置了 DPM 时 DPM 相关函数一并设置。
- 设置**随 case 文件保存，且模块按绝对路径保存**——**安装位置或 case 文件位置改变后 case 将无法加载模块**。需卸载旧库：UDF Library Manager（Parameters & Customization → User Defined Functions → Manage...）卸载后重新加载；此前保存的模型设置与参数保留。

### 34.3.3 模型设置（pp. 3639–3650）

入口：Setup → Models → MHD Model → Edit 或 TUI `define/models/mhd-model`。五类任务：

- **启用**：勾 Enable MHD（对话框展开）。
- **选 MHD 方法**（Table 34.1）：**Magnetic Induction**——分配 2 或 3 个 UDS（B_x/B_y/B_z，单位 **Tesla**）；**Electrical Potential**——1 个 UDS（Phi，单位 **Volt**）。
- **外磁场（External Field B0 选项卡）**：B0 Input Options 二选——
  - **Patch**：给计算域打上常量（DC Field）和/或时变（AC Field）场；AC 场表达为时间（Frequency）与空间（波长、传播方向、初始相位偏移）的函数；B0 Component 下设分量；可指定 **Moving Field**（**正弦或方波**波形，定义见 34.5）。
  - **Import**：B0 Data File Name 输入磁场数据文件（可用第三方程序如 MAGNA 生成；格式见 34.6）；**B0 Data Media** 按生成数据时的假设设 Non-Conducting 或 Conducting（对应 Magnetic Induction Method 的 Case 1/Case 2）；Field Type 由数据文件决定——单独选 DC 或 AC 时该选择无关紧要；**同时勾选 DC 与 AC 表示从数据文件导入两种场并叠加**（数据文件须含两个数据段）；**Apply External Field...** 打开对话框对所选 zone/register 区域施加；**Reset External Field** 把外磁场变量清零。
- **边界条件（Boundary Condition 选项卡）**：**所有 MHD 边界条件必须在此选项卡设置——不支持任何形式的自定义边界条件（参数、表达式等）**。
  - Cell zones：只能改材料及属性（Edit Material——电导率可 constant/分段线性/分段多项式/多项式/UDF；**磁导率只能常数**）。
  - 壁面四类：**Insulating Wall**（无电流穿过）、**Conducting Wall**（理想导体）、**Coupled Wall**（解 MHD 方程的固/固或固/液界面）、**Thin Wall**（**仅 Magnetic Induction 法**；有限电导率的外部壁面——选材料并给壁厚）。Electrical Potential 法的导电壁以 **Voltage 或 Current Density** 指定。
- **求解控制（Solution Control 选项卡）**：**Initialize MHD** 与（启用 DPM 时）**Initialize DPM** 按钮；**Solve MHD Equation** 开关（开时可选 **Include Lorentz Force** 与/或 **Include Joule Heating** 进动量与能量方程）；MHD 方程欠松弛因子；**B0 Scale Factor**——对外部 DC/AC 场数据施加缩放因子调节场强。

### 34.3.4 求解与后处理（pp. 3650–3652）

- **初始化**：case 初始化时全部 UDS/UDM 置零；外磁场数据由 External Field B0 选项卡设置。**Initialize MHD** 按钮用于把 MHD 效应加到已全/部分收敛的流场上、或计算中途改参数时——只清 MHD 标量变量与大部分内存位置，**外磁场数据的内存保留**。
- **迭代**：常从已收敛流场起步——感应方程本身易收敛，URF 可 0.8–0.9（极强磁场需更小）；**电位方程收敛慢，URF 不可设 1**；动量与能量方程加了源项后 URF 一般要调小。收敛困难时用 **B0 Scale Factor 渐进**：多次重启、从小缩放系数起步逐步增大到目标场强。
- **后处理**：标准设施——等值线从变量列表选 MHD 变量；矢量（Table 34.2）：**Induced-Field**（Tesla）、**External-Field**（Tesla）、**Current-Density**、**Electric-Field**（V/m）、**Lorentz-Force**。UDM 不直接后处理（用对应变量）；CFD-Post 经 .cdat 导出。

### 34.3.5 限制（p. 3652）

- 模块假设流体足够导电（Maxwell 方程中**电荷密度与位移电流项可忽略**）；弱导电流体该假设可能不成立。
- 电磁材料属性**只有常数各向同性模型**；多相体积分数不依赖温度、组分浓度或场强——足够强的磁场会使常数磁导率假设失效。
- **必须直接指定外加磁场——不支持以施加电流的方式间接指定**。
- AC 场按**较低频率设计，需显式解析每个周期**；高频模拟因时间步过小代价可能过高——**未实现时间平均方法**。

## 34.4 使用指南（pp. 3653–3655）

安装目录结构：`addons/mhd` 下有 `lib`（Scheme 界面代码 addon.bin）与具体架构目录（如 ntx86，内含 2d/2ddp/3d/3ddp 及其 _host/_node 子目录）。使用概览十步：启动（2D/3D/双精度/并行皆可）→ 读网格或 case（**新网格须做 mesh check 与 scale**）→ 加载模块（模块号 1）→ 启用模型 → 选方法 → 施加外磁场 → 设边界条件 → 设求解控制（URF 0.8–0.9、缩放因子渐进、Initialize MHD）→ 运行（常从已收敛流场起步）→ 后处理。

## 34.5 磁场定义（p. 3656）

- **正弦形式**（Eq 34.1）：平均矢量 + 幅值矢量 + 传播矢量与位置矢量点积相位 + 频率 f、波长 λ、相位偏移；x/y/z 方向余弦进入传播矢量。**非移动场传播矢量为零**。
- **方波形式**（Eq 34.2）：传播矢量定义同正弦形式。

## 34.6 外磁场数据格式（pp. 3656–3657）

文本文件结构：第 1 行数据文件标识标签；第 2 行 x/y/z 方向数据点数；随后三行分别给 x/y/z 方向范围（**数据点沿各方向均匀分布**）；第 6 行 AC 场旗标与频率（**nAC=0 静态场；nAC=1 为 AC 场、Freq 单位 Hz**）。其余每行一个数据点的磁场矢量实部与虚部分量，按索引（Eq 34.3）从 1 到 N（N=nx×ny×nz）升序排列。**DC+AC 复合场**：整个文件结构对 DC 与 AC 部分各重复一次（同文件两段，分别导入存储；**两段顺序不重要**）。导入数据解释为**某一时刻外加磁场的快照**；复数形式用于容纳振荡/移动场（Eq 34.4）。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3635–3658（批次 99，2026-10-20，pypdf layout 模式提取）。
- Theory Guide Eq 21.14/21.16/21.22 与 Eq 34.1–34.4 公式体未提取，按引用记录变量与语义；Table 34.1/34.2 内容照录；34.3.4.2 中感应方程 URF 的"0.8–0.9"区间符号在文本层缺失，按指南节同数值补全。
- Figures 34.1–34.11（对话框截图）为图形元素未摄取。
- 版本敏感：add-on 模块号（1）、加载绝对路径行为、AC 低频设计以 2026 R1 为准。
- 相关页面：[[Fluent 电势场与电化学]]（电位方程背景）、[[Fluent 离散相模型（DPM）]]（带电颗粒力）。
