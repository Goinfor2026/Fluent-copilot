---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - Ansys Fluent
  - task-pages
  - gui-reference
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 任务页参考（Task Page Reference Guide）

## 摘要

User's Guide 2026 R1 Part III / Chapter 51 "Task Page Reference Guide"（PDF pp. 4889 起，21 节：51.1 Meshing、51.2 Setup、51.3 General、51.4 Models、51.5 Materials、51.6 Cell Zone Conditions、51.7 Boundary Conditions、51.8 Overset Interfaces、51.9 Dynamic Mesh、51.10 Reference Values、51.11 Solution、51.12 Solution Methods、51.13 Solution Controls、51.14 Solution Initialization、51.15 Calculation Activities、51.16 Run Calculation、51.17 Results、51.18 Graphics and Animations、51.19 Plots、51.20 Reports、51.21 Parameters and Customization 任务页）。**摄取状态：章内进行中——批次 135 完成段 1（pp. 4889–4902：51.1–51.3）；51.4–51.21 待后续批次。**

本页为任务页控件参考索引；深层操作语义见既有专题页（[[Fluent 网格读取与操作]]、[[Fluent 图形显示]]、[[Fluent 单位制]] 等）。

## 51.1–51.2 Meshing 与 Setup 任务页（p. 4889）

各仅一句介绍：Meshing 任务页引导求解 CFD 仿真涉及的最常见网格任务；Setup 任务页引导建立 CFD 仿真的主要任务。

## 51.3 General 任务页（pp. 4890–4902）

General 面板设一般性问题设置（网格/求解器）；**读入 case 或 mesh 文件后才可用**——求解器类型、操作条件（重力加速度）、单位设置等。**Important：CFD Pro 能力级别下功能受限。**

- **Mesh 组**：**Scale...**（开 Scale Mesh 对话框）；**Check**——校验网格有效性：体积统计、网格拓扑与周期边界信息、simple x 计数器核验、轴对称案例节点位置对轴核验（详见 Checking the Mesh，p. 1290；**建议读入后立即检查**）；**Report Quality**——控制台打印网格质量量（最小正交质量、最大长宽比等；详见 Mesh Quality，p. 1187）；**Display...**（开 Mesh Display 对话框）。
- **Solver 组**：**Type**——Pressure-Based（压力基 Navier-Stokes，默认）/ Density-Based（密度基耦合）；**Velocity Formulation**——Absolute（默认）/ Relative（仅压力基）；**Time**——Steady / Transient；**2D Space**（仅 2D 求解器）——Planar / **Axisymmetric**（绕轴轴对称——改解 2D 轴对称形式控制方程；**须把旋转轴 zone 类型改为 axis**，见 Changing Cell and Boundary Zone Types，p. 1349）/ **Axisymmetric Swirl**（含周向速度分量——轴对称旋流，见 p. 1815）。
- **Gravity** + **Gravitational Acceleration**（X/Y(/Z) 分量，Z 仅 3D；浮力驱动流见 p. 1438；仅 Gravity 开启时出现）；**Units...**（开 Set Units 对话框）。

### 51.3.1 Scale Mesh 对话框（pp. 4892–4894）

网格单位转 SI 或自定义缩放（详见 Scaling the Mesh，p. 1332）。**Domain Extents**（X/Y/Zmin–Max，只读信息）；**Scaling**：Convert Units + **Mesh Was Created In**（m/cm/mm/in/ft——自动设缩放因子，如英寸 0.0254 m/in）；Specify Scaling Factors（逐坐标手输）；**Scaling Factors** X/Y(/Z)；**Scale**（节点坐标乘因子）/ **Unscale**（除以因子）；**View Length Unit In**——域范围显示单位（同时联动 Set Units 对话框的长度单位）。

### 51.3.2 Mesh Display 对话框（pp. 4894–4899）

控制 zone/surface/分区边界网格显示（详见 Displaying the Mesh，p. 4082）；亦经 Results → Graphics → Mesh → **New...** 打开。**注意两版本**：工具栏网格按钮打开的是"全局"/**非持久**版（无 Name 字段、不随 case 保存）；**推荐用持久版**（New... 创建、保存定义、可复用于场景等）。控件：**Mesh Name**（默认 `mesh-<id>`；仅持久定义）；**Options**——Nodes / Edges / Faces / **Partitions**（分区边界）/ **Overset**（只显示求解单元；`define/overset-interfaces/options/render-receptor-cells? yes` 时也显示 receptor 单元）/ **Gap**（只显示 gap 模型允许流动的单元——须已建 gap 定义，见 p. 1279）；**Shrink Factor**（面/单元收缩显示，p. 4104）；**Edge Type**——All / Feature（轮廓显示中的特征线，p. 4103）/ Outline；**Feature Angle**（仅 Feature 时；特征细节量）；**Transparency**（仅全局版）；**Surfaces** 列表 + **New Surface** 下拉（Point / Line-Rake / Plane / Quadric / Iso-Surface / Iso-Clip / Structural Point 各建面对话框）；**Outline**（全选/反选轮廓边界）与 **Interior**（全选/反选内部面）；**Adjacency**（Adjacency 对话框，p. 5607——找与所选 cell zone 相邻的 face zone）；**Coloring**——**By Type**（按 zone 类型自动着色，色表在 Zone Type Color and Material Assignment 对话框，p. 5908）；**By Surface**（按 zone ID；可经 Surface Rendering Properties 对话框，p. 5861 固定指定面颜色/材质；**Ctrl+Shift+O 随机化网格颜色——图形窗口须先获得焦点**）；**By Association**（仅 Model Topology）四式——By Topological Body / By Topological Face（最"随机"观感）/ By Physics Volume / By Physics Boundary；**Uniform**（手动定边/面颜色 + Material + Edit 开 Material Editor，p. 5751）；**Colors.../Display**（仅全局版——Colors 开 Mesh Colors 对话框）；**Save/Display**（持久版——显示并保存定义）。

### 51.3.3 Set Units 对话框（pp. 4899–4901）

为任意量设单位制（详见 Unit Systems，p. 1055）。**Quantities** 全量列表；**Units** 该量可用单位（选中即生效）；**Factor/Offset**（所选单位到 SI 的换算因子/偏移，只读）；**Set All to** 四标准制——**default**（似 si 但角度用度）/ **si** / **british**（English Engineering）/ **cgs**；**New...**（开 Define Unit）；**List**（控制台打印所有量当前单位）。

### 51.3.4 Define Unit 对话框（p. 4901）

自定义某量的单位（自 Set Units 打开；用法见 Defining a New Unit，p. 1057）。**Quantity**（只读，由 Set Units 选定）；**Unit**（新单位名）；**Factor**；**Offset**。

### 51.3.5 Mesh Colors 对话框（pp. 4901–4902）

控制网格绘制颜色（自"全局"版 Mesh Display 打开；详见 Modifying the Mesh Colors，p. 4087）。**Options**——Color by Type（按 zone 类型）/ Color by Surface（按 zone ID；Ctrl+Shift+O 随机化告诫同上）；**Types**（zone 类型列表）；**Colors**（所选类型颜色）；**Sample**；**Reset Colors**（恢复默认）。

## 证据与适用条件

- 来源：Ansys Fluent User's Guide 2026 R1，Chapter 51（自 p. 4889），批次 135 段 1（pp. 4889–4902），SHA-256 校验一致；段 2 起（51.4–51.21）待后续批次。
- 本页为参考指南性质：控件名照录、页码交叉引用保留原指向；深层语义以各专题页与原文为准；CFD Pro 功能限制为 2026 R1 描述。
