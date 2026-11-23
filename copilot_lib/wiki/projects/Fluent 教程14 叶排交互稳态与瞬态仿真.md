---
type: project
created: 2026-10-27
updated: 2026-10-27
tags:
  - Ansys Fluent
  - CFD
  - tutorial
  - mixing-plane
  - pitch-scale
  - 叶排交互
  - 压气机
sources:
  - "[[Ansys Fluent Tutorial Guide 2026 R1]]"
---

# Fluent 教程14 叶排交互稳态与瞬态仿真

## 摘要

Tutorial Guide 2026 R1 第 14 章（PDF pp. 573–618；p. 618 空白页）：对与第 13 章相同的 1.5 级 Hannover 压气机先做**稳态 mixing-plane** 仿真、再转**瞬态 pitch-scale（rotor-stator）**仿真，评估压气机效率，并展示两类叶排界面模型的物理差异（尾迹是否穿越界面）。

## 问题描述（14.3，pp. 573–574）

- IGV 26 叶、转子 23 叶（17100 RPM）、静子 30 通道；入口总压 60000 Pa；出口 60500 Pa（正文称 gauge total pressure，边界条件实际按静压 Gauge Pressure 60500 Pa + 径向平衡设置，见下）。
- 网格 `hannover_1.5Stage.msh.h5`；Solution 模式、3D、双精度、4 进程；angular-velocity 单位设 rev/min。

## 稳态 Mixing Plane 模型（14.4.3–14.4.10，pp. 576–602）

**模型与材料**：开启 **Energy 方程**（效率计算需要温度）；k-omega SST（选型理由同第 12 章：预测叶轮机械分离）；air 改为 **ideal-gas**。Operating Pressure = 0 Pa。

**Cell Zone 与边界条件**（pp. 578–585）：
- `b-rotor1`：Frame Motion，17100 rpm；`a-igv`、`c-stator1` 核对旋转轴。
- inlet（pressure-inlet）：Gauge Total Pressure = 60000 Pa；Supersonic/Initial Gauge Pressure = **58000 Pa**；方向 Normal to Boundary；湍流 5% / 10（默认）；总温 **288.15 K**。
- outlet（pressure-outlet）：Gauge Pressure = 60500 Pa；Backflow = From Neighbouring Cell；**启用 Radial Equilibrium Pressure Distribution 与 Average Pressure Specification**；backflow 总温 300 K。
- `rotor1-shroud`：**Moving Wall → Absolute + Rotational**——转子有叶尖间隙、外机匣在绝对系静止，而默认壁面随附着流体域旋转，必须改（与教程 12 的 inblock-shroud 同理）。
- 三排各自创建**旋转周期边界**（Conformal、Rotational）：periodic_igv、periodic_rotor、periodic_stator。
- Turbo 界面三个：`rotor1-tipgap-int`（tip-r1-side1 ↔ tip-r1-side2，叶尖间隙自成界面）；`mpm1`（igv↔r1）与 `mpm2`（r1↔s1），均 General Turbo Interface + **Mixing Plane**。
- Turbo Topology `topo1`：hub/shroud/Theta Periodic/Inlet/Outlet/Blade 各边界逐一指定面。

**求解与报告**（pp. 589–597）：
- Methods 保留默认 **Coupled**。
- 面积加权平均报告定义：ave_po_in / ave_po_out（总压）、ave_to_in / ave_to_out（总温）、mfr_1psg_out（静子出口单通道质量流量）。
- 表达式报告定义（原文变量名照录）：
  - `p-ratio` = `{ave_po_out}/{ave_po_in}`
  - `mfr_out_360` = `{mfr_1psg_out}*30`
  - `iso_efficency` = `(({ave_to_in}*({p-ratio}**(0.4/1.4)-1))/({ave_to_out}-{ave_to_in}))*100`——等熵效率，**γ 硬编码为 1.4**（0.4/1.4）。
- 收敛判据：Residuals 高级选项——Scale + **Compute Local Scale**，Reporting Option = **local scaling**，判据 Absolute。
- 初始化：Hybrid + Absolute + Use Specified Initial Pressure on Inlets；Time Scale Factor 10、**100** 迭代；以压比/出口流量/效率三条曲线走平判断收敛。

**稳态后处理**（pp. 598–602）：mixing-plane 特征——上游尾迹与下游势流**在界面处被掺混（mixed out）**。用 Iso-Surface（Mesh... → **Spanwise Coordinate** = 0.5，From Zone 选对应排）建三个 mid-span 面，显示速度幅值/静压/静温云图（关 Global Range、开 Contour Lines，叠加 hub/blade 面）。

## 瞬态 Pitch-Scale 模型（14.4.11–14.4.17，pp. 602–617）

由稳态方案改造：
1. Solver 切 **Transient**。
2. **Reference Values 设为入口条件——计算熵（entropy）所需**。
3. 界面改名换型：mpm1 → `ps1`、mpm2 → `ps2`，Pitch-Change Types 由 Mixing Plane 改 **Pitch-Scale**。
4. `b-rotor1` 点 **Copy to Mesh Motion**（Frame Motion → Mesh Motion）。
5. Outlet **禁用 Average Pressure Specification**——教程明示理由：**pressure-average 选项不建议用于非定常仿真，可能产生非物理的压力反馈**。
6. Methods：Coupled + 瞬态格式 **Second Order Implicit**。
7. Report Plots：Get Data Every 改**每个时间步**；X 轴（flow time）改 **Exponential、精度 2**。
8. 运算：Time Advancement Method = **Period-Based**；转子周期 = 60/17100/23 = **0.000152555 s**（每转时间除以叶片数，即叶片通过周期）；**Time Steps per Period = 40**；Total Periods = 5；Max Iterations/Time Step = 10。结果中效率、流量、压比呈周期性波动——**叶片通过交互（blade passing interaction）所致，属预期**。另存 `hannover_1.5Stage_trs.cas/dat.h5`。

**瞬态后处理**（pp. 612–617）：瞬态中尾迹穿越界面，但因 pitch-scale 近似，尾迹云图在界面处出现**不连续**——用熵云图呈现（Temperature... → Entropy；关 Global Range/Auto Range/Clip to Range；Min = **-7**、Max = **80**）。用 **Periodic Instancing**（View → Display → Periodic Instancing）做全环重现：a-igv → igv-span=0.5 重复 **2** 次；b-rotor1 → rotor-span=0.5 重复 **23** 次（全环）；c-stator1 → stator-span=0.5 重复 **2** 次。

## 证据与适用条件

- 依据：[[Ansys Fluent Tutorial Guide 2026 R1]] Ch.14 全章（PDF pp. 573–618，2026 R1 Downloads 副本，SHA-256 `8347db…`）；p. 618 为空白页（仅页脚）。
- 版本敏感：界面类型名、Period-Based 推进与周期参数均按 2026 R1；周期 0.000152555 s 绑定 17100 rpm/23 叶，换算例需重算。
- 原文名称照录（复现需一致）：报告定义名 `iso_efficency`（缺 i），而对应 report plot 名印作 `iso_effiiciency-rplot`（双 i），两处不一致系原文排版差异；periodic_rotor 组合面名含 `sdie`（side 误拼）照录。
- 效率表达式 γ=1.4 为硬编码，仅适合理想气体空气；14.4.12 Reference Values 一节的截图内容未提取到文字，只有"设为入口条件以计算熵"的说明。
- 界面模型理论：[[Fluent 叶轮机械流动]]（mixing plane / pitch change 三类界面）；瞬态滑移网格机理：[[Fluent 滑移与动网格]]；表达式语法：[[Fluent 表达式语言]]。

## 关联页面

- [[Ansys Fluent Tutorial Guide 2026 R1]]（来源记录）
- [[Fluent 教程13 Turbo Setup 叶轮机械设置与分析]]（同一几何的工作流设置）、[[Fluent 教程12 Frozen Rotor 方法]]、[[Fluent 教程15 滑移网格]]
- [[Fluent 叶轮机械流动]]、[[Fluent 滑移与动网格]]、[[Fluent 表达式语言]]、[[Fluent 数据报告]]
