---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags:
  - Ansys Fluent
  - fsi
  - structural-model
  - dynamic-mesh
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 流固耦合（FSI）

## 摘要

User's Guide 2026 R1 Part III / Chapter 29 "Modeling Fluid-Structure Interaction (FSI) Within Fluent"（PDF pp. 3343–3354，两节）。**本页全章完成（批次 90，pp. 3343–3354）**：Fluent 会话内完成的"intrinsic FSI"——结构方程由 Fluent 自带求解（区别于外挂求解器经 mapping/System Coupling 的 extrinsic 方式）；单向/双向 FSI 的区分、结构模型限制清单、16 步设置流程（结构模型选择、材料、Wall Structure 选项卡位移边界、动网格、瞬态时间积分、线性求解器与专家 TUI）及非一致界面用法。理论见 Theory Guide "The Structural Model for Intrinsic FSI"（式号 16.x 由本章引用）。

## 29.1 概览与限制（pp. 3343–3344）

- **单向 FSI**：只有流体力作用于结构、无固体反馈——可流固同时算，也可在流体算完后单独算结构。**双向 FSI**：固体变形反过来影响流体——**必须经动网格启用流体域网格运动**，且只能瞬态。
- 结构方程求解限制：
  - **单元类型**：2D 四边形/三角形；3D 六面体/四面体/楔形/金字塔。**不支持多面体**（仅对固体区而言）；**Fluent Meshing 生成的 hexcore 网格含少量多面体单元，不可用于结构模型**。
  - **FSI 解初始化/启动后不得更换网格**（新网格重新分区后的数据迁移在 FEA 中不支持）；流体区重新分区允许。
  - 流体与固体区必须由**双侧壁面（wall/wall-shadow 对）**分隔；域内**至少一个固体区**才能启用结构模型。
  - **不支持的动网格选项**：In-Cylinder、Six DOF、Contact Detection。
  - Intrinsic FSI 类型只能在 Dynamic Mesh Zones 对话框中选给**紧邻流体单元区一侧**的双侧壁面（以 Wall 对话框 Adjacent Cell Zone 字段为准）。
  - 与固体区相邻（或固液之间）的壁面上，位移/力**只支持 `DEFINE_WALL_NODAL_DISP`、`DEFINE_WALL_NODAL_FORCE` 与体积力 `DEFINE_SOURCE_FE`** 三种 UDF；其余（如 `DEFINE_PROFILE`）报错。**Shell Conduction 不支持**。
  - 结构模型**不兼容**：网格自适应、mesh morpher/optimizer、英制或 CGS 单位制、FMG 初始化、自适应时间步长。
  - **Workbench 环境下运行 Fluent 时结构模型不可用**。
  - **Linear Elasticity 仅当应力不超过材料屈服强度时适用**；兼容 2D Axisymmetric / Axisymmetric Swirl。
  - Structure... 后处理变量**只在固体单元区有效**——相关计算（等值线等）应只选固体区；周期边界在结构解中**按无应力（stress free）处理**，无特殊处理。

## 29.2 设置流程（pp. 3345–3353）

**所有 intrinsic FSI 算例推荐双精度。**

1. **General**：单向可稳态或瞬态，双向必须瞬态（双向仅在固体变形显著影响流动时才必要）；可开 Gravity 让结构计算计入重力。
2. **固体区**（Cell Zone Conditions → Solid）：可开 Frame Motion 定义参考框旋转速度，让结构计算计入旋转力。
3. 双向 FSI 建议先跑到**流体解收敛**再往下设结构模型。
4. **Structural Model 对话框**（Setup → Models → Structure → Edit，Figure 29.1）：
   - Model：**Linear Elasticity**（内力与节点位移线性成比例、刚度矩阵恒定）或 **Nonlinear Elasticity**（几何非线性，模拟大变形）。
   - Options：**Thermal Effects**（线性/非线性热弹性；需开启能量方程）；Newman's P2D 电池肿胀选弹性模型后 **Battery Effects 自动启用且不可关**；resolved 锂电池肿胀对应 **Li-ion Battery Effects** 同样自动启用（见 [[Fluent 电池模型]]）。
5. **材料**：Create/Edit Materials 的 Properties 组设 **Youngs Modulus、Poisson Ratio**；热弹性另加 **Starting Temperature [K]** 与 **Thermal Expansion [1/K]**。非常数初始温度场做法：先解出固体区温度场，再 TUI `define/models/structure/expert/starting-t-re-initialization?` 提示时输入 **1** 重初始化新起始温度场（可用 Structure 类别 Starting Structure Temperature 等值线查看；重初始化后 Materials 对话框中起始温度不再可用）。三个属性均可用 `DEFINE_PROPERTY` UDF。
6. 体积体力源项 UDF：`DEFINE_SOURCE_FE`。
7. 壁面节点位移/力 UDF：`DEFINE_WALL_NODAL_DISP` / `DEFINE_WALL_NODAL_FORCE`。
8. **Wall 对话框 Structure 选项卡**（每个紧邻固体区的壁面）：X/Y/Z 每方向位移边界五选一——**Stress Free**（不受流体应力）；**Node X/Y/Z-Force**（指定节点力）；**Node X/Y/Z-Displacement**（指定位移）；**Face Pressure**（面压载荷）；**Intrinsic FSI**（位移来自流体压力载荷，**仅 wall/wall-shadow 对**可选）。节点力/位移/面压可用常量、输入参数、UDF 或**表达式**（Fluent Expressions Language）。对称面策略：用对称边界，或对称面与笛卡尔面一致时用壁面——如 XY 对称面设 x、y 位移 Stress Free + z 位移 0。**允许结构刚体运动的边界条件会导致问题病态**：Fluent 能检测并在边界条件未阻止此类运动时告警（同一固体区内的不相连区域除外），应避免。
9. **双向 FSI 动网格**：启用 Smoothing（Mesh Method 选 **Diffusion / Linearly Elastic Solid / Radial Basis Function**）；强耦合（流体与固体密度同量级或大变形）启用 **Implicit Update** 并在 Options 对话框 Implicit Update 选项卡设置；为紧邻流体区一侧的双侧壁面定义 **Intrinsic FSI 动网格区域**，不变形的边界建成 stationary 区域。
10. **瞬态时间积分**：Solution Methods 的 **Structure Transient Formulation** 下拉——**Newmark（默认）**或 **Backward Euler**。
11. 默认结果不满意时可调：
    - **线性求解器**：默认 **BCGSTAB**（速度/稳健平衡）；检测到发散时自动以 **GMRES** 回退迭代一次，控制台提示 "fe-structure" 方程被稳定化。内迭代上限默认 500，TUI `define/models/structure/controls/max-iter` 调大；BCGSTAB 持续不佳或频繁回退时改用 GMRES（最稳健、内存与耗时更高，建议 max-iter 从 **50** 起）；另有 **CG**（利用矩阵对称性可更快，但最不稳健）——切换用 `define/models/structure/controls/amg-stabilization`。
    - 瞬态数值阻尼因子（Theory Guide Eq 16.16 振幅衰减因子）：`define/models/structure/controls/numerical-damping-factor?`。
    - 显式流固耦合力：`define/models/structure/expert/explicit-fsi-force?`。
    - FSI 力计入**操作压力**：`include-pop-in-fsi-force?`；计入**黏性 FSI 力**：`include-viscous-fsi-force?`。
    - **剪切自锁（shear locking）修正**：弯曲主导变形时线性位移插值会低估位移（粗网格尤甚）；启用 **enhanced strain element** 修正（仅 2D quad、3D hex）：`define/models/structure/controls/enhanced-strain?` → yes。
    - 瞬态 **Rayleigh 阻尼**：`define/models/structure/controls/unsteady-damping-rayleigh?`；固体材料阻尼系数两参数——**Mass Proportional Damping [1/s]** 与 **Stiffness Proportional Damping [s]**。
12. x/y/z 位移残差方程收敛准则可在 Residual Monitors 修改。
13. （可选）在固体内建 **Structural Point** 面（Results → Surfaces → New → Structural Point）做监测报告；双向 FSI 中该点不固定于空间，持续代表其原始单元。配 Report Definition 监测（如 Vertex Average 位移）。
14. 初始化：标准初始化可指定初始 X/Y/Z Displacement。**结构模型启用时写 case/data 只支持 CFF（Common Fluids Format）**。
15. （可选，双向）设 Scene Animation 观察流动/固体形状随时间变化（建议收窄 min-max 范围）。
16. 运行计算。**单向 FSI 提速技巧**：先只在 Equations 中开流体方程算，再只开结构方程算；单向/双向均**建议先解稳态流动**，便于分离与 FSI 无关的收敛问题。
17. 结果：**Structure...** 类别变量——Total Displacement、X/Y/Z Displacement、应力张量 Sigma XX/YY/XY/ZZ/YZ/XZ、**von Mises Stress**（选中后处理时自动计算）；可显示矢量。注意：①确认应力未超屈服强度（线性弹性假设）；②等值线只画在固体区，但**基于表达式/custom field function 的等值线、min/max 计算、XY 图不遵循这一限制**。

## 29.2.1 非一致界面（p. 3353–3354）

- 固体区网格常与流体区独立剖分，固液界面常见非一致网格；FSI 支持**非一致界面**（假定 3D 固体侧面为四边形或三角形网格，由 Fluent 在界面处计算 intersection facets）。**仅支持流体-固体非一致界面，不支持固体-固体**。
- 步骤：读入网格 → Setup → Mesh Interfaces → New 建界面 → 启用 Structural Model（选 Linear/Nonlinear）→ 在建界面时自动生成的壁面上设 intrinsic FSI 边界条件与动网格 → 其余按正常流程。

## 证据与适用条件

- 依据 User's Guide 2026 R1 pp. 3343–3354（批次 90，2026-10-20，pypdf layout 模式提取，无需渲染核对）。
- Theory Guide Eq 16.16（数值阻尼）公式体未提取，按引用记录；Figures 29.1–29.3（对话框截图）为图形元素未摄取。
- 版本敏感：TUI 命令、默认值（BCGSTAB/内迭代 500/GMRES 50/Newmark）以 2026 R1 为准；Workbench 不可用为 2026 R1 陈述。
- 相关页面：[[Fluent 电池模型]]（Battery Effects / Li-ion Battery Effects 自动启用）、[[Fluent 滑移与动网格]]（Smoothing/Implicit Update/动网格区域细节见 Ch.14）。
