---
type: project
created: 2026-10-27
updated: 2026-10-27
tags:
  - Ansys Fluent
  - CFD
  - tutorial
  - sliding-mesh
  - rotor-stator
  - 轴流压气机
sources:
  - "[[Ansys Fluent Tutorial Guide 2026 R1]]"
---

# Fluent 教程15 滑移网格

## 摘要

Tutorial Guide 2026 R1 第 15 章（PDF pp. 619–664）：用**滑移网格（sliding mesh）**对单级轴流压气机做瞬态 rotor-stator 交互分析。与 GTI 路线（教程 12/14）不同，本章演示**周期重复界面（Periodic Repeats）**连接旋转/静止区的替代做法；并完整展示滑移网格的时间步推导、时间周期性判定、时均采样与 FFT 频谱分析。

## 问题描述（15.3，p. 620）

- 转子 **16 叶 @ 37500 rpm**；静子 **32 叶**；叶数使域旋转周期化，周期角 **22.5°** → 只建 **1 转子叶 + 2 静子叶**部分几何。
- 高雷诺数 + 粗网格（两排合计仅 13856 单元）→ 采用**无粘模型（Euler 方程）**。

## 设置要点（15.4，pp. 620–636）

**准备与网格**：`axial_comp.msh.h5`；Solution、3D、双精度、**1 进程**（本教程不用并行）。Mesh Check 会因 unassigned interface zones 报错——**此阶段无需处理，定义 mesh interface 后自然消除**。单位：angular-velocity → rev/min，**pressure → atm**。

**周期区创建**（15.4.3）：4 对 wall zone 改 Rotational 周期——rotor-per-1+3、rotor-per-2+4（id 12/11）、stator-per-1+3（26/27）、stator-per-2+4（24/25）；Ctrl 多选 → 右键 Periodic... → Rotational → Create。**注意**：先选中的作 periodic zone、后选中的作 shadow zone，选择顺序可能影响结果（本例无影响）。

**模型**：Viscous 选 **Inviscid**；air 密度改 **ideal-gas**——**Fluent 自动启用 Energy 方程**（理想气体密度所需）；Time = **Transient**（允许网格运动的前提）。

**Cell Zone**（15.4.6）：`fluid-rotor` 启用 **Mesh Motion**（滑移网格用 Mesh Motion，不是 Frame Motion），轴 (0,0,1)，37500 rpm；`fluid-stator` 静止仅核对轴。

**边界与操作条件**（pp. 631–636）：
- rotor-inlet：总压 **1.0 atm**、Supersonic/Initial Gauge Pressure 0.9 atm、总温 288 K。
- stator-outlet：静压 **1.08 atm** + **Radial Equilibrium Pressure Distribution**、backflow 总温 288 K。教程提醒：出口动量/温度仅在回流时生效，应给合理下游值防回流失真。
- 壁面全默认。无粘流知识点：**壁面法向速度恒为零（与流体域是否运动无关），对无粘流即已充分，切向速度是解的一部分**。
- Operating Pressure = **0 atm**——压力边界按绝对压（atm）输入时操作压力必须为零；边界压力输入总是相对操作压力。

**Periodic Repeats 界面**（15.4.9，pp. 636–637）：
1. 先执行 TUI 命令 `define/mesh-interfaces/one-to-one-pairing? no` 禁用一对一配对，才能选 Periodic Repeats。
2. Mesh Interfaces → New → Manual Create：名 `int`、启用 **Periodic Repeats**（两区不重叠部分按周期处理）、Side 1 = rotor-interface、Side 2 = stator-interface。
3. 经验规则：两 interface zone 大小不同时**选小的作 Zone 1**；本例相近故顺序无关。
4. 重新 Mesh Check 确认此前警告消除。

## 求解与时间步推导（15.4.10，pp. 638–659）

- Methods：**Coupled**；Controls：Momentum、Pressure 显式松弛 **0.5**，Temperature 亚松弛 **0.9**。
- 残差：Convergence Criterion = **relative**，各方程 Relative Criteria = **0.01**。
- 监视：surf-mon-1/2/3（入口与出口质量流量、interface 面积加权静压），各开 Report File + Report Plot + Print to Console（自动生成 -rplot/-rfile 树节点）。
- 初始化：**Compute from = rotor-inlet**、Reference Frame = Absolute。
- **时间步推导**（教程给出的完整逻辑）：单个叶片通过期分 **15** 个时间步；16 叶 → 每步转 360/16/15 = **1.5°**；37500 rpm = 2.25e5 deg/s → **Δt = 1.5/2.25e5 = 6.6667e-6 s**；一转 = 16×15 = **240 步**；Max Iterations/Time Step 默认 20。残差每步初跳升后降 2–3 个量级、相对判据在 20 步内达成，上限无需加大。
- **分段推进与改名**：跑 1 转（240 步）→ 存 `axial_comp-0240` → **把 report file 输出改名 surf-mon-1b/2b/3b.out** 再续跑，避免覆盖历史；再跑 720 步（3 转）至 960 步，检查流量/interface 压力曲线确认**时间周期性**；再改名 1c/2c/3c。
- 文件实践：**滑移网格的 case 含随时间变化的网格，存 data 必须同时存 case**；瞬态文件名可加 **`%t`** 自动追加时间步号（axial_comp-%t → axial_comp-0240.cas.h5）。
- 最后一转采样：建点 surface `point-1`（-0.02, -0.08, -0.036）于静子界面，surf-mon-4 = Vertex Average 静压；续跑 240 步并勾选 **Data Sampling for Time Statistics**（对区间内各量计算并存储均值与 RMS）→ 存 `axial_comp-1200`。

## 后处理与 FFT（15.4.11，pp. 659–664）

- Results → Plots → **FFT...**：加载 surf-mon-4-rfile.out；Plot/Modify Input Signal 勾 **Subtract Mean Value**、X 轴用 flow-time；轴格式 exponential/精度 1。
- 结论：界面压力脉动由**转子/静子叶片通过频率 10 kHz 与 20 kHz 及其高次谐波主导**（37500 rpm = 625 Hz/转 × 16 叶 = 10 kHz；×32 叶 = 20 kHz，与教程一致）。
- 时均云图：Contours of **Unsteady Statistics... → Mean Static Pressure**，Wall 面，Filled + Banded——外机匣压力剧变区清晰可见**激波**。

## 证据与适用条件

- 依据：[[Ansys Fluent Tutorial Guide 2026 R1]] Ch.15 全章（PDF pp. 619–664，2026 R1 Downloads 副本，SHA-256 `8347db…`）。
- 版本敏感：`one-to-one-pairing?` TUI 命令、Periodic Repeats 选项与 FFT 对话框布局按 2026 R1；时间步 6.6667e-6 s 绑定 16 叶/37500 rpm，换算例需按同法重推。
- 无粘（Euler）+ 粗网格是教程为演示做的简化，不代表工程精度；atm 单位下的压力输入与 0 操作压力配套使用。
- 理论背景：[[Fluent 滑移与动网格]]（滑移网格技术、时间周期解与 %t 文件名）；GTI 对照：[[Fluent 叶轮机械流动]]、[[Fluent 教程14 叶排交互稳态与瞬态仿真]]；FFT 绘图：[[Fluent 图形显示]]；报告定义：[[Fluent 数据报告]]。

## 关联页面

- [[Ansys Fluent Tutorial Guide 2026 R1]]（来源记录）
- [[Fluent 教程12 Frozen Rotor 方法]]、[[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]、[[Fluent 教程14 叶排交互稳态与瞬态仿真]]（同系列叶轮机械教程）
- [[Fluent 滑移与动网格]]、[[Fluent 叶轮机械流动]]、[[Fluent 图形显示]]、[[Fluent 数据报告]]
