---
type: source
title: "Ansys Fluent User's Guide 2026 R1"
created: 2026-10-15
updated: 2026-10-19
source_kind: manual
status: partially-ingested
author:
  - T. J. Baker
version: "2026 R1"
source_path: "../../raw/inbox/Ansys_Fluent_Users_Guide.pdf"
url: ""
tags:
  - Ansys Fluent
  - CFD
  - user-guide
---

# Ansys Fluent User's Guide 2026 R1

## 内容与范围

Ansys Fluent User's Guide，PDF 共 6056 页。PDF 元数据作者为 T. J. Baker；书签及正文标识版本为 Release 2026 R1。书签目录已完整提取到 [[Ansys Fluent Users Guide 2026 R1 - 目录地图]]。

主要部分（以下页码均为 PDF 阅读器物理页码）：

- Part I: Getting Started，p. 143–219
- Part II: Meshing Mode，p. 223–907
- Part III: Solution Mode，p. 909–5967
- Part IV: Web Interface，p. 5969–6056

## 已摄取内容

### 批次 1：CFD 工作流程与仿真检查清单（PDF pp. 177–184）

- [[CFD 仿真工作流与验证]]：归纳分析步骤、建模规划、求解监控、结果检查与仿真质量核查。

### 批次 2：启动参数与批处理（PDF p. 185、pp. 198–205、pp. 210–215；选定内容）

- [[Fluent 启动与批处理自动化]]：汇总部分 CLI 启动模式、Journal、PyFluent 服务入口和 Windows/Linux 批处理差异。

### 批次 3：网格质量诊断（PDF pp. 582–602）

- [[Fluent 网格质量诊断]]：整理诊断流程、直方图/局部定位及质量指标的含义与适用边界。

### 批次 4：Chapter 1 简介——架构、能力、许可证与已知限制（PDF pp. 143–176）

- [[Fluent 程序架构与能力]]：架构与双模式（pp. 145–146）、APIP 数据收集范围（pp. 147–150）、程序能力与四级许可证矩阵 Table 1.1（pp. 150–154）、第三方软件版本 Table 1.2（pp. 174–175）。
- [[Fluent 2026 R1 已知限制]]：1.3 节全部类别的限制条目转述，保留缺陷编号、命令与变通方法（pp. 155–174）。
- p. 143 为 Part I 扉页（各章起始页）；pp. 144、176 为空白/版权页，无正文。

### 批次 5：Part I / Chapter 4 — Starting and Executing Ansys Fluent（PDF pp. 185–218）

- 完成本章全范围。整合先前已摄取的 p. 185、pp. 198–205、pp. 210–215 与本轮补充的 pp. 186–197、pp. 206–209、pp. 216–218。
- [[Fluent 启动与批处理自动化]]：Launcher/工作区和精度选择、Windows/Linux 启动差异、并行/GPU/MPI 与调度器选项、启动 TUI 命令、批处理、检查点文件、清理和退出行为。
- Chapter 4 的目录范围止于 p. 218；p. 219 起为术语表，不纳入本章。

### 批次 6：Part II / Chapter 1 — Introduction to Meshing Mode（PDF pp. 225–258）

- [[Fluent 网格模式入门]]：1.1 网格化两种途径、1.2 能力清单、1.3 进入网格模式（.tgrid/.fluent、双进程构建、动态 spawn）、1.4 GUI 组件（Ribbon/Workflow/Outline View/Console/工具栏/Preferences/帮助）、1.5 TUI 总览。

### 批次 7：Part II / Chapter 1 — 1.6 Reading and Writing Files（PDF pp. 258–284）

- [[Fluent 网格模式文件读写与导入]]：mesh/case/size-field/journal/transcript/domain 文件的读写规则与格式开关（CFF 与 legacy）、外部格式导入（Prep7/cdb、CGNS、GAMBIT、HYPERMESH、NASTRAN）、CAD 导入选项与命名/单位规则、问题几何处理、保存图片格式。
- **Chapter 1 目录范围 pp. 225–284 至此完成**；p. 284 为版权页脚，无正文。

### 批次 8：Part II / Chapter 2 — Getting Started with the Fluent Guided Workflows（PDF pp. 285–300）

- [[Fluent 引导式网格工作流]]：两种预置工作流适用条件、几何前提与命名模式→边界类型映射表、限制（2020 R1 前 journal/.wft 不兼容等）、任务定制与 `%py-exec`/`(%py-console)` Python journal 接口、任务状态/编辑/分组、通配符过滤语义、`.wft` 保存加载与工作流首选项。
- Chapter 2 目录范围 pp. 285–300 至此完成。

### 批次 9：Part II / Chapter 3 — Watertight Geometry 工作流（PDF pp. 301–326，章内进行中）

- [[Fluent 水密几何网格工作流]]：3.1 工作流总限制与逐任务限制、3.2 UTL（CFD Pro 启动）、3.3 Import Geometry（单位/body labels/zone 分离/PMDB 流程）、3.4 Import BoI、3.5 Add Local Sizing（七种尺寸控制）、3.6 Generate Surface Mesh（size files、重划范围、高级选项、台阶移除、质量改进、Auto Remesh 行为）。
- **本章未完结**：3.7–3.28（PDF pp. 326–408）待下一轮同章续接，下一未读位置 p. 326（3.7 节起）。

### 批次 10：Part II / Chapter 3 完成（PDF pp. 301–408）

- 本轮补充 3.7–3.28（PDF pp. 326–408），与批次 9 合并完成全章。
- [[Fluent 水密几何网格工作流]]：周期边界、几何描述/共享拓扑、封口与流体区域、薄体网格、边界层、多区与体网格、边界/网格改进、变换/拉伸、线性 pattern、区域管理、局部细化和自定义 journal。
- 用户本次要求依目录连续处理五章：Chapter 3–7；Chapter 3 为第 1/5 章，之后依次为 Chapter 4 pp. 409–524、Chapter 5 pp. 525–538、Chapter 6 pp. 539–604、Chapter 7 pp. 605–868（目录边界；p. 869 起为 Appendix A）。

### 批次 11：Part II / Chapter 4 完成（PDF pp. 409–524）

- [[Fluent 容错网格工作流]]：容错网格全章，包括 CAD 与模型树、几何/流动类型、封口与泄漏阈值、region/尺寸控制、表面与体网格、boundary layers、overset、zone 后处理及部件替换。
- 已阅读目录范围 pp. 409–524，并更新知识页、Part II 项目页、索引、来源页和检查点。用户五章任务第 2/5 章完成。

### 批次 12：Part II / Chapter 5 完成（PDF pp. 525–538）

- [[Fluent 2D 网格工作流]]：二维 CAD 导入、区域/边界、全局与局部尺寸、MultiZone、2D shell boundary layers、表面网格、2D mesh 导出及旋转扫掠/挤出。
- 用户五章任务第 3/5 章完成。下一章 Chapter 6 pp. 539–604；其 pp. 582–602 有过往整理，本轮到达后补缺并回查。

### 批次 13：Part II / Chapter 6 完成（PDF pp. 539–604）

- [[Fluent 网格质量诊断]]：合并此前 pp. 582–602 的诊断与质量指标摘要，补充 pp. 539–581 的网格修复、显示和选择工具及 pp. 603–604 实体信息报告，按目录完成全章。
- 手册中的 sliver 阈值是工具默认值，不是通用验收标准；手工编辑并非全可撤销，实体索引可能复用。
- 用户五章任务当时为 4/5；Chapter 7 从 p. 605 续接。

### 批次 14：Part II / Chapter 7 进行中（PDF pp. 605–837）

- [[Fluent 高级网格主题]]：整理 7.1 CAD Assemblies、7.2 Size Functions and Scoped Sizing、7.3 Objects and Material Points、7.4 Object-Based Surface Meshing、7.5 Object-Based Volume Meshing、7.6 Manipulating the Boundary Mesh、7.7 Wrapping Objects、7.8 Creating a Mesh、7.9 Generating Prisms、7.10 Generating Tetrahedral Meshes、7.11 Hexcore、7.12 Polyhedral、7.13 Poly-Hexcore（Tet/Hexcore/Poly 体网格策略和限制）。
- 按目录，Chapter 7 范围为 pp. 605–868；本批次先整理至 7.13.1（p. 837），随后批次续接 7.14。

### 批次 66：Part III / Ch.19 Fluent's Virtual Blade Model 全章（PDF pp. 2427–2450），十批任务（66–75）第 1 批

- 十批连续任务（批次 66–75）第 1 批，24 页（p. 2450 为空白版权页）：19.1 引言（两类致动盘——pressure-disk 双面边界 vs Zori 动量源单层盘、BET 查表、Yang NR 配平沿革）；19.2 VBM 理论（BET 翼型堆叠、2π/N 几何平均、推力/力矩系数 C_NA-EU=1、湍流建议 k−ε/k−ω）；19.2.1–19.2.7（EDM/FDM 两模式、旋翼盘几何与 pitch/bank 旋转顺序、桨距分解 θ0+θ1c/θ1s、挥舞 β0+β1c/β1s、NR 配平 ±a 扰动数值 Jacobian 与 Damping Factor 0.7、Quadratic/Modified Prandtl 尖部损失）；19.3 网格指南（EDM 单层棱柱 1/40–1/100 盘径、FDM srf-fdisk-RotorName 创建四步、悬停远场非零质量流超定告诫）；19.4 翼型 .dat 格式（30 表/250 点上限、±180° 全迎角）；19.5–19.6 启用与 28 步配置（仅 3D 并行、不支持多相；Damping Factor 默认 0.1 推荐 0.7）；19.7–19.8 十五场变量与 Rotor_xx_Loads.csv 七类输出（读 data 不自动替换配平值的 Note）。
- 新建知识页 [[Fluent 虚拟叶片模型（VBM）]]。
- 提取边界：Eq 19.1 起公式体未提取按周边文字记录；p. 2430 湍流模型名（k−ε/k−ω）与 C_NA-EU 经 fitz 500 dpi 渲染视觉核对；Figures 19.1–19.6 为图形元素；Table 19.1–19.3 完整。
- 下一续接位置：Part III / Ch.20 Modelling with Finite-Rate Chemistry，从 p. 2451 开始。

### 批次 67：Part III / Ch.20 第 1 段——20.1 引言至 20.1.1.9 前半（PDF pp. 2451–2495），十批任务（66–75）第 2 批

- 十批连续任务（批次 66–75）第 2 批，45 页：章引言（组分上限 700/50 与 CFD-Post 多相质量分数 Note）；20.1.1.1 概览五步与 20.1.1.1.1 混合物材料概念（副本语义 Warning）；20.1.1.2 Species Model 对话框全流程（TCI 四选项及参数、Chemistry Solver 三选——Relax to Chemical Equilibrium/Stiff/CHEMKIN-CFD/None-Direct Source、Integration Parameters 加速方法、Full Multicomponent/Thermal Diffusion、Thickened Flame Model 全选项、边界/残差组分选择）；20.1.1.3 CHEMKIN 机理导入（加密机理六限制、五步导入流程、末位 bulk 组分规则、END 关键字、属性方法表、内置四机理 grimech30_50spec/Propane-NOx_highT/H2_mech/H2_NOx_mech）；20.1.1.4 混合物与组分属性（Species 对话框三类组分清单与顺序规则、Last Species、增删组分重置告诫、Reactions 对话框九步——两类反应/Arrhenius/第三体/压力依赖 lindemann-troe-sri/覆盖度/逆反应/Mixing Rate A=4.0 B=0.5、等效燃料物种 C4.17H6O2.75 与生成热、Zone 级机理与位点密度、混合物/组分属性清单、全局机理 Cp 修正 Table 20.1）；20.1.1.5 Coal Calculator（三煤流全输入与 OK 后自动动作）；20.1.1.6–20.1.1.7 组分 BC/进口扩散开关/NRBC 不兼容/源项；20.1.1.8 求解流程（两步冷流、密度欠松弛 0.5–1 与真实气体 0.1、点火 patch、刚性化学 Eq 20.8 与 Δt=1/10 最小时间尺度、密度基 0.2/0.25、EDC 先平衡后切换）；20.1.1.9 后处理变量清单（前半）。
- 新建知识页 [[Fluent 组分输运与有限速率化学]]。
- 提取边界：Eq 20.1–20.8 公式体未提取按周边文字记录；Table 20.1 列标题（CO₂/H₂O/O₂）经 fitz 400 dpi 渲染视觉核对；等效燃料分子式按分子量计算式反推；Figures 20.1–20.16 为图形元素。
- 下一续接位置：同章 p. 2496（20.1.1.9 收尾）起，至 20.1.2 Wall Surface Reactions（2497）等。

### 批次 68：Part III / Ch.20 第 2 段——20.1.1.9 收尾至 20.1.7（PDF pp. 2496–2541），十批任务（66–75）第 3 批

- 十批连续任务（批次 66–75）第 3 批，46 页：20.1.1.9 后处理变量收尾（TFM/EDC/刚性化学专属量、至少一迭代 Note）与 20.1.1.9.1 平均组分浓度；20.1.2 壁面表面反应与 CVD 全节（表面 CHEMKIN 导入与粘附系数转换、None-Explicit/F-R-E-D 的气相与表面反应类型限制、Heat of Surface Reactions/Mass Deposition Source/Diffusion Energy Source 三开关及密度基差异、低压力滑移 Shear Condition 显示重置、求解与后处理）；20.1.3 颗粒反应（限制、Diffusion-Limited/Catalyst Species、multiple surface reactions 七步、多组分颗粒五反应模型与蒸发联动、urea 液体属性 TUI）；20.1.4 电化学反应全节（概述与密度基限制、12 步设置、Butler-Volmer/Tafel 参数与 UDF、多孔双电位与壁面 Faradaic、Joule/Faradaic 热、离子迁移、双电位 zone 自动检测三依据与燃料电池示例、Water Corrosion Pre Tool——阳极铁溶解/阴极析氢 Tafel 参数数值与 CO2/强酸两环境流程）；20.1.5 无反应组分输运；20.1.6 Reacting Channel 全节（三条限制、边界组/耦合迭代/欠松弛、Group Settings/Inlet、U 形管 TUI、通道变量后处理）；20.1.7 Reactor Network（快化学 CFD + 聚合反应器详细机理、LES 时间平均场、Expert Options 全参数与自定义组成变量）。
- 扩充知识页 [[Fluent 组分输运与有限速率化学]]。
- 提取边界：Eq 20.9–20.12 公式体未提取按周边文字与数值照录（Tafel 参数符号名缺失）；CO2 环境四个均相反应方程体未提取；Figures 20.17–20.35 为图形元素。
- 下一续接位置：同章 20.2 Modeling a Composition PDF Transport Problem，从 p. 2542 开始（20.2 至约 2555，20.3 Using Chemistry Acceleration 至章尾 2570）。

### 批次 69：Part III / Ch.20 第 3 段（末段）——20.1.7.3 收尾、20.2–20.3（PDF pp. 2542–2570），Ch.20 全章完成

- 十批连续任务（批次 66–75）第 4 批，29 页（p. 2570 为空白版权页）：20.1.7.3 Reactor Network 后处理变量；20.2 Composition PDF Transport 全节（压力基限制、九步流程与既有解初值 Important、Lagrangian——默认刚性+ISAT、三种混合模型、Liquid Micro-Mixing、粒子数/局部时间步三数、Eulerian——IEM 独占、气相 Mixing Constant 2、单/多模态能量方程、边界混合分数、Equilibrate Inlet Stream、初始化、监视与稳态平均 Iterations in Average 50/Increment 0.2、非稳态分数步长、可压缩、CHT、后处理 Mean/RMSE 与 PDF 粒子轨迹、Eulerian 逐模态变量）；20.3 化学加速六方法全节（ISAT 容差体系 0.001/1e-8/1e-9/1e-4、Max Storage 100 MB、Verbosity 文件族、高效使用与清表 TUI、表读写不建议与并行规则、DMR——DRG 算法、容差 0.01、目标物种 h 起步 3 个、Expert TUI、DRG Reduced 场变量零值语义与不落盘、渐进容差策略、负载平衡选法、CA 0.02/10 K、DR——超 700 物种用途、代表物种 12 默认与选法、reduced-dimension-mixture 规则、仅配 ISAT、DCC 参数 10 K/0.05/10/0/1e-09、DAC 容差 0.001 与 co+ho2 默认目标、与 ISAT 不兼容）。
- 扩充知识页 [[Fluent 组分输运与有限速率化学]] 至全章完成。**Ch.20 全章（pp. 2451–2570）完成。**
- 提取边界：Eq 20.13（PDF 瞬时值质量加权平均）与可压缩 PDF 粒子内能式公式体未提取按周边文字记录；Figures 20.36–20.44 为图形元素。
- 下一续接位置：Part III / Ch.21 Modelling of Turbulent Combustion With Reduced Order，从 p. 2571 开始。

### 批次 70：Part III / Ch.21 第 1 段——21.1 引言至 21.1.9（PDF pp. 2571–2625），十批任务（66–75）第 5 批

- 十批连续任务（批次 66–75）第 5 批，55 页：21.1.1 使用步骤（四化学描述、单混合分数六步、查表 = Eq 8.17/8.25/8.19 积分）；21.1.2 平衡化学（绝热二维/非绝热三维查表、Compressibility Effects 与 Eq 21.1、二次流七情形与运行时 PDF 积分开销、double delta/beta PDF、经验燃料限制与分子量条件、RFL≈2× 计量分数与富燃非平衡依据）；21.1.3 火焰let（机理 ≤700 组分、Standard/CFX-RIF 导入、非稳态火焰let五输入与 Initialize Unsteady Flamelet Probability、Max Scalar Dissipation 默认 30/s、柴油机非稳态三前提、多 flamelet 起始时间、Burnt Initial Flamelet、Flamelet Fluid Zones、IC 发动机推荐 ≥2 flamelet 与 split injection ≥3、Diesel Unsteady Flamelet Reset 概率加权重建 vs Inert EGR Reset）；21.1.4 流股组成（边界组分默认清单、蒸发/脱挥温度约定、凝聚相物种密度 propdb.scm/1000 kg/m³、经验原子分数输入、液体燃料蒸发物种选最大组分、煤三方案、单/双混合分数组成两法与手册换算表、Vaporization Temperature/Burnout Ratio 2.67/Latent Heat 规则、DPM Evaporation/Devolatilization 与 Burnout 后处理、Coal Calculator 非预混版 LCV 式 21.4/21.5）；21.1.5 控制参数（NOx 物种排除与 TUI 强制纳入、Initial Fourier Number/Multiplier/收敛容差/最大积分时间、非稳态初始火焰let慢化学默认置零 17 物种+H2(l)+C(s)）；21.1.6 火焰let计算（标量耗散乘子/步进示例 1e-3→1e-2→…、AGR、保存 File→Write→Flamelet、2D Curves/3D Surfaces 后处理）；21.1.7 PDF 查表（表参数全集、Max Species 200 与密度比热全物种预算、单/双混合分数运行时差异 Important、全制表 4D/5D 与 full-tabulation TUI、经验燃料富燃失败与热值-潜热补偿、保存 File→Write→PDF、PDF Table 对话框与缩放方差 0–0.25）；21.1.8 标准 flamelet 文件关键字表与缺失物种规则（≤1e-3 才可删、同步 NUMOFSPECIES）；21.1.9 Inert 模型（Fixed H/C Ratio vs User Specified、Inert Stream 边界、patch 自动重算焓、Heywood 氧化反应式族、Inert EGR Reset 化学计量惰性化与 G-Equation 负值）。
- 新建知识页 [[Fluent 缩阶湍流燃烧模型]]。
- 提取边界：Eq 21.1–21.10 公式体未提取按周边文字记录；AGR 网格点默认值缺失；Figures 21.1–21.29 为图形元素。
- 下一续接位置：同章 21.1.10 Defining Non-Premixed Boundary Conditions，从 p. 2626 开始。

### 批次 71：Part III / Ch.21 第 2 段——21.1.9.3 尾注、21.1.10–21.1.14、21.2（PDF pp. 2626–2642），十批任务（66–75）第 6 批

- 十批连续任务（批次 66–75）第 6 批，17 页：21.1.9.3 EGR 重置焓调整尾注；21.1.10 非预混边界条件（混合分数/方差进口值约定、Inlet Diffusion、查表温度一致性）；21.1.11 物理属性（pdf-mixture 自动材料、只设输运性质且不可组分函数、WSGGM、真实气体配 Compressibility Effects）；21.1.12 求解策略（单/双混合分数、prePDF 2 不支持与 PrePDF 3+ 兼容、PDF 文件名存 case 自动找回与全路径告诫、初始化 0 值、fmean/fvar/psec/pvar 残差列、PDF 方程欠松弛 1/0.9、密度欠松弛、双混合分数 Compressibility Effects）；21.1.13 Robust Numerics（pdf_stability_marker 寄存器 + pmn_pdf_stability_marker 定义、默认停用与 TUI 激活、Preferences 永久启用）；21.1.14 后处理变量全集（Pdf/Species/Temperature/Unsteady Flamelet 四类、非稳态火焰let仅前 50 物种、绝热也可后处理温度焓）与 Inert 后处理八变量；21.2 预混燃烧全节（五限制——压力基/湍流亚音速/禁污染物模型/禁反应颗粒/G 方程仅非稳态；先选非 SA 湍流模型；绝热 Adiabatic Burnt Temperature vs 非绝热 Heat of Combustion + Unburnt Fuel Mass Fraction；Zimont 五常数、Peters TUI 与 Ewald Corrector、G 方程方差输运/代数与曲率源项默认排除、Turbulent Schmidt=Energy Prandtl、premixed-combustion 密度、c=0/1 与 patch 初始化、后处理变量与 G 方程两附加量、组分浓度自定义场函数）。
- 扩充知识页 [[Fluent 缩阶湍流燃烧模型]]。
- 提取边界：批次 71 段无新编号公式；21.2.4.1 组分浓度场函数公式体未提取按语义记录；Inert Mass Fraction 公式体未提取；Figures 21.30–21.35 为图形元素。
- 下一续接位置：同章 21.3 Modeling Partially Premixed Combustion，从 p. 2643 开始（至章尾 p. 2670）。

### 批次 72：Part III / Ch.21 第 3 段（末段）——21.3（PDF pp. 2643–2670），Ch.21 全章完成

- 十批连续任务（批次 66–75）第 7 批，28 页（p. 2670 为空白版权页）：21.3 部分预混全节——限制（FGM 仅限 c-Equation）；设置 11 步（C/G 方程的 State Relation 选择矩阵、薄火焰let vs 有限厚度、预混进口两设法与甲烷 φ=0.3 示例、prepdf-polynomial 与五种火焰速度方法、层流火焰速度超范围告诫与 Recalculate Properties）；FGM（进度变量自定义对话框、预混火焰let参数——混合分数/进度空间网格点、化学计量标量耗散默认 1000/s、AGR 默认 64/0.5/0.5 与 CHEMKIN Physical Space 12/250/0.5/0.1、网格分布编辑、扩散 FGM——无 Maximum Flamelets 参数与步长 ≈ 熄灭应变率 1/20、熄灭火焰let建模未燃-稳态间流形、Include Equilibrium Flamelet、非绝热热损失——焓级数与 Fully Premixed FGM）；查表（表参数、AGR 禁用时网格编辑与 Use Flamelet Distribution、FGM Scalar Transport——表前选标量与稳态后处理模式解法、4D/5D 表后处理与 Enthalpy Slice 语义）；FGM 标准文件关键字（PREMIX_CHI/REACTION_PROGRESS/PREMIX_YCDOT；样例另现 PREMIX_STOICH_SCADIS）；Premix 页（SBES RANS 两常数、TCI Finite-Rate/Turbulent Flame Speed、方差 transport/algebraic/hybrid 三法与推荐、Algebraic Variance Constant）；未燃属性多项式（Eq 8.129 四属性、prepdf 拟合范围六燃料/贫限–1/298–800 K/1–40 bar、20 点分段线性限外恒值、二次混合分数附加列、Non-Adiabatic Laminar Flame Speed）；拉伸层流火焰速度（需输运数据文件、热损失点 0.05 增量 <10 点、Display Strained Flamelets）；内燃机多循环（G-Equation 仅 Inert+EGR Reset 一途）；FGM Scalar Transport 后处理与 GPU 求解器三限制。**Ch.21 全章（pp. 2571–2670）完成。**
- 扩充知识页 [[Fluent 缩阶湍流燃烧模型]] 至全章完成。
- 提取边界：批次段无新编号公式（Theory Guide Eqs 8.109–8.141 未展开）；SBES hybrid 方差分区符号未提取；Figures 21.36–21.51 为图形元素。
- 下一续接位置：Part III / Ch.22 Modeling Engine Ignition，从 p. 2671 开始。

### 批次 73：Part III / Ch.22 Modeling Engine Ignition 全章（PDF pp. 2671–2684），十批任务（66–75）第 8 批

- 十批连续任务（批次 66–75）第 8 批，14 页（p. 2684 为空白版权页）：22.1 火花模型（Species Transport+Volumetric 或 Premixed C/G 方程载体、≤16 火花、Set Spark Ignition 参数——中心坐标/kernel 初始半径/起始时刻与时长/In-Cylinder 曲轴角语义与 Eq 14.30 循环联动、Energy 可选默认 0、Flame Speed Model、R14.5 case 回退与 TUI 切换）；22.2 自燃模型（Knock 与 Ignition Delay 两类、兼容矩阵——Species Transport 仅 Ignition Delay、Premixed 仅 Knock、Partially Premixed 皆可、Hardenburg 四参数与 Cetane Number、Generalized 八参数含 RPM/当量比/辛烷值指数、Douaud 五参数）；22.3 缝隙模型（crevice-model? 与 crevice-model-controls 全 TUI 参数——缸径/活塞间隙/缝隙温度/扇区角/流量系数/曲轴箱压力/泄漏壁与共享边界/环数与逐环七几何参数/n+2 初始压力、多环复制快捷法、crevice-summary 摘要、Crevice Model Sources 欠松弛 0.8、质量流失 ∝ 缸压-曲轴箱压差与峰值压力下降、crev.out 每时间步格式与 Gnuplot/Excel 读回、Fluent 读回需拆列加三行头）。
- 新建知识页 [[Fluent 发动机点火模型]]。**Ch.22 全章（pp. 2671–2684）完成。**
- 提取边界：本章无编号公式；Figures 22.1–22.10 为图形元素；TUI 交互与输出样例已照录。
- 下一续接位置：Part III / Ch.23 Modeling Pollutant Formation，从 p. 2685 开始。

### 批次 74：Part III / Ch.23 Modeling Pollutant Formation 全章（PDF pp. 2685–2724），十批任务（66–75）第 9 批

- 十批连续任务（批次 66–75）第 9 批，40 页：23.1 NOx（解耦后处理八步与预混不兼容/SNCR 前置两条 Important；Pathways 四选项与非预混 Fuel NOx 需 DPM；三燃料流构型与 N 源选择、燃料物种 5/流与 10 总、14.5 旧 case 行为；NOx Rate UDF 的 Add/Replace 与 user-defined Tmax；热力 [O]/[OH] 三法与尿素用 [OH]；燃料 NOx 的 N Intermediate/Conversion Fraction 默认 1/Partition Fractions 语义、Char N Conversion 四选与 BET 面积、Eqs 23.2–23.7；N2O quasi-steady 残差恒零告诫与 transported-simple；Reburn instantaneous-[CH] 需 CH/CH2/CH3 与 partial-equilibrium 六燃料+等效燃料 C/H 比选法；SNCR 气液两喷射法、尿素升华按单速率脱挥发、Reagent Fraction in Stream 与 nox-chemistry TUI、尿素两分解模型；湍流 PDF Mode 三选与跨污染物一致性 Important、mixture fraction 先验制表、PDF Points 10 起步增至 20–25、Tmax 四选项；求解策略 DPM Interval 0/欠松弛 1.0/残差 1e-6；后处理变量全集）；23.2 Soot（大质量分数或辐射须随主解、与预混不兼容、一步/两步仅湍流、Soot-Radiation Interaction 下不可后处理；一步模型参数与丙烷默认；两步 Tesner 仅配 eddy-dissipation、成核参数族与乙炔默认；MB/MB-Hall 适用条件与 C2H2/C6H6/C6H5/H2 前提、user-correlation 分段多项式（默认仅甲烷 290 K 有效、三段八系数、从低到高排序）、Fenimore-Jones vs Lee、[OH]/[O] 模型、氧化缩放参数恒 1 与 soot-parameters TUI、UDF 两钩子；MoM——矩数 3–6、Use Precursor 粘附系数/Specify Mechanism 成核反应、聚集模型临界直径与分形维 1.7–2.0 及高估告诫、HACA 与位点密度 cm² 单位、归一化矩；后处理变量全集）；23.3 DDC（稳态流场详细机理后处理、Original vs Pollutant Species、pollutant-mixture + Stiff Solver、平衡计算非污染物、ISAT 1e-5 + Max Storage 大内存）。
- 新建知识页 [[Fluent 污染物生成模型]]。**Ch.23 全章（pp. 2685–2724）完成。**
- 提取边界：Eq 23.1–23.9 公式体未提取按周边文字记录；两步模型 3.5e8 参数名缺失；Figures 23.1–23.14 为图形元素。
- 下一续接位置：Part III / Ch.24 Predicting Aerodynamically Generated Noise，从 p. 2725 开始。

### 批次 75：Part III / Ch.24 Predicting Aerodynamically Generated Noise 全章（PDF pp. 2725–2770），十批任务（66–75）第 10 批（收官）

- 十批连续任务（批次 66–75）第 10 批（收官），46 页（p. 2770 为空白版权页）：24.1 概览（直接法、FW-H、波动方程、宽带源四路线及适用边界）；24.2 FW-H 全节（稳态单 MRF 用法与 forward-time projection、模型常数、on-the-fly、ASD/CGNS 源数据导出（SYSNOISE 体积源/柱坐标、Simcenter 3D 文件族与旋转壁限制）、源面规则（内部面 cell zone 指定、禁包围、渗透面禁与内壁同选）、源数据保存参数、接收器与移动接收器发射时刻语义、显式求解器自适应采样 Time Step Size for Acoustic Data Export、信号读写流程与缓冲冲掉告诫、auto-pruning、Surface dpdt RMS、Acoustic Sources FFT 四页全流程（Clip Time/窗函数/存储区两模式/点探针/频带与模态变量/面平均 .xy/CGNS 频谱导出与 links、Windows 网络盘告诫）、GPU 求解器 .asdg 与四限制）；24.3 波动方程模型（适用与常密度限制、源掩模 UDF/Region 基本形状、子迭代控制与 AMG、声学独立初始化 ramping 与 DEFINE_ON_DEMAND、七个后处理场与 retain-temporary-solver-mem、Kirchhoff 远场积分——单积分面/共享接收器/.ark/仅 on-the-fly/与 FW-H 同仿真五步）；24.4 宽带噪声源（SNGR Realizations 200/Fourier Modes 50、后处理变量全集）；24.5 密度基海绵层（压力基可压瞬态、远场密度二次混合、厚度 ≥2 波长、重叠层归属规则、两个 Mesh 类后处理场）。**Ch.24 全章（pp. 2725–2770）完成。**
- 新建知识页 [[Fluent 气动噪声模型]]。**用户指定的十批连续任务（批次 66–75）全部完成（10/10）。**
- 提取边界：Eqs 24.1–24.4 公式体未提取按语义记录；Reference Acoustic Pressure/Power 默认数值与 Table 24.1 表体缺失（参考压 2e-5 Pa 经 24.2.6 节交叉确认）；Figures 24.1–24.24 为图形元素。
- 下一续接位置：Part III / Ch.25 Modeling Discrete Phase，从 p. 2771 开始。

### 批次 76：Part III / Ch.25 第 1 段——25.1–25.2（PDF pp. 2771–2818），十批任务（76–85）第 1 批

- 新十批连续任务（批次 76–85）第 1 批，48 页：25.1 引言（能力清单、与 Euler-Euler/DDPM/VOF-to-DPM 的关系）、25.1.1 三概念（Coupled/Uncoupled、Steady/Unsteady Tracking、parcel 与 DEM 中的 parcel 几何）、25.1.2 六类限制（体积分数 <10–12% 与质量载荷不限、Knudsen 连续区与 10 nm 最小粒径、连续悬浮、颗粒旋转五限、与其他模型联用——多相 Shared Memory 禁用/Eulerian 仅主相/流向周期稳态禁/预混仅惰性颗粒/粗糙网格注入限制/绝对系追踪/overset 需 High-Res、Hybrid 并行静默回退清单与 Use DPM Domain 失效情形）；25.2 十二步流程、DPM Iteration Interval 与 Update DPM Sources Every Flow Iteration、稳/瞬态颗粒处理（In-Cylinder 曲轴角注入、Clear Particles）、四种 parcel 释放方法（standard 公式 25.1/constant-number/constant-mass/constant-diameter、雾化器与 file 注入强制 standard、2D/3D parcel 几何与 APF 2/3）、追踪时机规则、Max Steps（50000/500，上限按 1e5 记录待核）与 Length Scale/Step Length Factor（Eq 25.2/25.3、经验法则、默认 5）、高分辨率追踪（subtet 分解 + 重心插值、多相属性插值自动启用、梯度插值与瞬态插值不兼容）及全部 TUI（退化 subtet 检查、quad face centroid、LWF 投影、相交容差 1e-5、边界层追踪、重心相交与采样、速度误差控制、液膜平滑参数、周期面质心、滑移界面穿越分数、重心插值九项、颗粒重定位六项）、八种拖曳律指引、物理模型 14 项（辐射限 P-1/DO、热泳、Saffman、虚拟质量、侵蚀与累积选项、蒸发压力选项、Pressure Dependent Boiling 全套与超临界、温度相关潜热、Two-Way Turbulence Coupling 适用清单、随机碰撞与 Coalescence、DEM 全设置与碰撞律/限制/数值推荐、体积位移 0.95）、UDF 钩子清单、数值（四格式与 Automated 高低阶切换、Accuracy Control、耦合热质限因子 0.3/0.1、参考系、节点平均与四种核、源项线性化及 UDF 不兼容清单、动态交互范围八叉树与三限制、空间/时间错列与随机数控制、Packing Limit Enhanced Numerics 开头）。
- 新建知识页 [[Fluent 离散相模型（DPM）]]。
- 提取边界：Eq 25.1–25.5 及 2D/3D parcel 几何系列公式体未提取按语义记录；Max Steps 上限与部分默认数值在提取文本中截断已标注；Figures 25.1–25.12 为图形元素。
- 下一续接位置：同章 p. 2819（25.2.7.8 收尾），批次 77 = 25.3 初始条件与 injection（2819–2881）。

### 批次 77：Part III / Ch.25 第 2 段——25.3（PDF pp. 2819–2881），十批任务（76–85）第 2 批

- 十批连续任务（批次 76–85）第 2 批，63 页：25.3 初始条件与 injection 全节（12 种注入类型与选择指引；5 种颗粒类型与激活 Law 表——massless/inert(1,6)/droplet(1,2,3,6)/combusting(1,4,5,6)/multicomponent(7,8) 及理想气体/体积加权密度前置；单/组（线性插值 Eq 25.7、单属性区间告诫）/四类锥（hollow 的 Dispersion Angle 与 Swirl Fraction、ring 内外半径、3D 扇区方位角与参考向量、瞬态重算与稳态只初始化一次告诫）/面（Scale Flow Rate by Face Area、Randomize 与之互斥、Face Normal Direction、Inject Wallfilm Partials 限制、RR 分布 Number of Diameters）/体（zone 或四类包围几何、三种投放量口径、DDPM 自动起点数与 Packing Limit 0.63、Estimate Parcel Count）注入点属性；五种雾化器全参数（plain-orifice/pressure-swirl/air-blast/flat-fan/effervescent）；file 注入三格式（无头 steady/12 头 steady/13 头 unsteady、一致性检查列、flow-time 升序、Start Flow-time in File 与 Repeat Interval）；condensate；RR 与对数 RR 与随机 RR（Eq 25.12 反解采样）与表格分布（三行格式、累积勾选、Interpolate Between Classes 样条）；injection 管理（List Particles/Properties、读写跨 case、Linux SLES11 可视化规避）；injection 属性 22 步（蒸发/氧化/产物物种、GPU+非绝热 FGM 限前 15 组分、多组分 Components 页与近零蒸气压技巧、Wet Combustion、Multiple Reactions 表面物种分数）；injection 级物理模型（八种拖曳律及各自适用与必填参数、六种换热系数、颗粒旋转 Dennis/Oesterle-Bui-Dinh/Tsuji/Rubinow-Keller、粗糙壁 Ra/Rq/RSm、布朗运动须 Stokes-Cunningham+能量方程、六种破碎模型 TAB/Wave/KHRT/SSD/Madabhushi/Schmehl 全参数与 Rayleigh 生长开关）；DRW 湍流扩散（Tries 非稳态锁 1、Time Scale Constant 0.15/RSM 0.3、动量质量均分影响）；自定义 Laws 与 Switching UDF；多 injection 批量修改（Modify 勾选语义、Apply 每类别、子集生效）；瞬态注入 .ttab profile（≤63 字符、可赋变量清单、3 段示例）。
- 扩充知识页 [[Fluent 离散相模型（DPM）]]。
- 提取边界：Eq 25.7–25.12 公式体未提取按语义记录；TAB y0 默认值缺失；Figures 25.13–25.38 为图形元素。
- 下一续接位置：同章 25.4 Setting Boundary Conditions，从 p. 2882 开始。

### 批次 78：Part III / Ch.25 第 3 段——25.4–25.6（PDF pp. 2882–2914），十批任务（76–85）第 3 批

- 十批连续任务（批次 76–85）第 3 批，33 页：25.4 边界条件（轨迹命运清单、八种 BC——reflect（旋转颗粒 Tsuji 模型）/trap/escape/wall-jet 适用域/wall-film/interior 限内部 zone/reinject（Use Settings From、Reinjection Only、时间延迟、DEFINE_DPM_BC）/user-defined；默认 BC 与恢复系数仅壁面可改；恢复系数按撞击角函数化；摩擦系数默认 0.2 与分段默认点 0/1/10/210 m/s；颗粒-壁撞击换热（wall-film 下直接颗粒-壁、飞溅颗粒不适用、燃烧颗粒须 Wet Combustion）；侵蚀/沉积参数——Generic/Finnie/McLaury/Oka/DNV/Shear Stress 六模型全参数与 Granular Phase Shielding、默认全启用、Oka 实验调校告诫）；25.5 侵蚀耦合动网格（准稳态方法与 Eq 25.13、前置八步、三条限制（仅稳态/专用对话框运行/恒绝对系）、设置全流程（Reference Erosion Model 五选 + UDF、壁材密度 2719 默认、Automatic Dynamic Mesh Setup 与 erosion UDF 动区、Participating Walls 选流体侧、变步长 Maximum Node Movement 10% 默认、Total Time of Erosion、Solve DPM during Flow Simulation、自动存盘与图形、Accumulated Deformation 后处理））；25.6 LWF（四子题；九条限制——仅非稳态、悬挂节点、液体假定、Rosseland/Workpile/EWF/overset、跨边界例外 trap/symmetry；设置——撞击/飞溅三模型 stanton-rutland/kuhnke/stochastic kuhnke（SCR）与 Regime Parameters、Number of Splash Drops 0 = 不飞溅、Film Stripping 单材料限制、Film Separation 三模型与临界 We/角；膜-壁换热导热默认与对流模型（部分加热面偏移、旧 case 告诫）；caloric 温度；壁温限幅器与 Leidenfrost 报告；膜冷凝触发条件与五步设置（condensate 注入、Linearized Source Terms 建议）；气侧边界层模型默认开与热解覆盖；原位数据约简（N³×M³×K 子盒合并、跨 injection 合并与最小 parcel 数 20）；液膜初始化（Film Height/速度/温度/每面最少 parcel 数/面密度取大示例））。
- 扩充知识页 [[Fluent 离散相模型（DPM）]]。
- 提取边界：Eq 25.13 公式体未提取按语义记录；Figures 25.39–25.55 为图形元素。
- 下一续接位置：同章 25.7 Setting Material Properties，从 p. 2915 开始。

### 批次 79：Part III / Ch.25 第 4 段——25.7–25.8（PDF pp. 2915–2937），十批任务（76–85）第 4 批

- 十批连续任务（批次 76–85）第 4 批，23 页：25.6.6 尾注（Initialize From Injection、Apply All Settings 立即初始化、单 parcel 置面心、Reset LWF 与 Initialize LWF）；25.7 材料属性（Tables 25.1–25.5 属性×类型×方程汇总；离散相材料四类与"建注入才有材料类型"规则、particle-mixture 组分选择；属性逐项——Binary Diffusivity 三法与压力依赖、Boiling Point 与多组分分压和沸腾语义、Combustion Model 三选、Cp/Density 的 char 组分相关选项与非预混语义、Devolatilization 四模型与最低挥发分 0.01、Heat of Pyrolysis 符号约定、Latent Heat 常数取沸点值、React. Heat Fraction 0 默认、Saturation Vapor Presssure 限幅与 RGP、Swelling Coefficient 1、Temperature Averaging Coefficient 1/3 与蒸发物种属性前置、Thermolysis 四模型与 SCR 建议、Thermophoretic talbot 默认、Vaporization Temperature 建模决策语义、Vapor-Particle-Equilibrium 三选、Vaporization/Boiling 两模型与变 Lewis/传热平均 TUI/蒸发物种 Cp 选项、Volatile Fraction 不互溶假定、发射率煤 1.0 灰 0.5 与散射 0.9 及连续相散射忽略、表面张力与黏度）；25.8 求解策略（非耦合两步 vs 耦合五步循环、全部 injections 强制与 massless 无作用、DPM Iteration Interval 0 = 不算、solve/dpm-update、随机追踪 Tries 与系综收敛、源欠松弛 Eq 25.14 默认 0.5/0.9 与 200 迭代示例、linear-growth-of-dpm-source-term 线性爬升、Reset DPM Sources 无确认清零、随机轨迹模型清单与按颗粒种子分区无关性、re-randomize 两开关与 Table 25.6 组合矩阵）。
- 扩充知识页 [[Fluent 离散相模型（DPM）]]。
- 提取边界：Eq 25.14 公式体未提取按语义记录；Figures 25.56–25.59 为图形元素。
- 下一续接位置：同章 25.9 Postprocessing，从 p. 2938 开始。

### 批次 80：Part III / Ch.25 第 5 段——25.9 前半（PDF pp. 2938–2972），十批任务（76–85）第 5 批

- 十批连续任务（批次 76–85）第 5 批，35 页：25.9.1 轨迹显示（流程与单流追踪/非稳态语义、Pulse 动画与保存、同种子同轨迹注记、轨迹风格十种与 attributes（sphere Detail 4–50、ribbon Twist By）、矢量三风格、Coarsen（稳态）与 Skip（瞬态）、XY 图）；25.9.2 追踪统计（parcel 计数非物理、tracking-statistics TUI、Track 按钮）；25.9.3 汇总报告（稳态不存 .dat/瞬态累积、Fates 表、Mass/Energy Transfer Summary、耦合稳态热平衡校核 Important、燃烧/多重表面反应/多组分报告、命运全集含非稳态追加（transformed/inserted/in fluid/in film/filmrelease）、incomplete_parallel 分区交换限 1000、再注入 Reinject/Inserted 配平语义与 BC-UDF、蒸发质量分解 calc-exchange-data-on-zone-types + dpm-extended-summary）；25.9.4 逐步报告（仅稳态、Significant Figures、Reporting Variables 与 Add Color by）；25.9.5 非稳态当前位置（Sample File Format 可作跨仿真 injection 文件、flow-time 列）；25.9.6 相间交换项 13 变量（仅耦合更新、2D 深度约定）；25.9.7 颗粒变量六表（通用表含 Law Index 1–7 与 Tracking Scheme 0–3、热质表 Spalding 数、DEM 力不存 .dat、旋转、用户定义、破碎表 Breakup Type 0–7 与 WAVE cutoff/TAB/Pilch-Erdman/Madabhushi 变量）。
- 扩充知识页 [[Fluent 离散相模型（DPM）]]。
- 提取边界：Eqs 25.15–25.22 公式体未提取按语义记录；Figures 25.60–25.66 为图形元素；Tables 25.7–25.12 提取照录。
- 下一续接位置：同章 p. 2973（Table 25.13 LWF 变量起），批次 81 = 25.9 后半 + 25.10（2973–3004，Ch.25 收官）。

### 批次 81：Part III / Ch.25 第 6 段（末段）——25.9 后半 + 25.10（PDF pp. 2973–3004），Ch.25 全章完成

- 十批连续任务（批次 76–85）第 6 批，32 页：Table 25.13 尾项；25.9.8 离散相变量（自动/均值/RMS 三档清单、Eq 25.23/25.24 事件式驻留时间加权、Node Based Averaging 使旧变量失效）；25.9.9 非稳态 DPM 统计（Data Sampling + DPM Variables、Eq 25.25–25.27、Unsteady DPM Statistics 变量清单）；25.9.10 轨迹采样（Sort Sample Files 排序语义、.dpm 文件、网格界面三文件、Append、DEFINE_DPM_OUTPUT）；25.9.11 直方图（Weight 稳态 mass-flow/非稳态 parcel-mass、Logarithmic、Percent/Histogram Mode/Diameter Statistics/Correlation/(Variable)^3/Cumulative Curve）与 25.9.11.2 数据约简（全变量同时分箱、No. of Bins 1 忽略、Create Steady from Unsteady）；25.9.12 面采样云图（Plotting Grid Interval Size 大于网格、九个命名表达式——sufficient_data_flag/signif_sauter_mean_diameter/mass_flux 等、与 DPM 变量类加权差异、限本面使用）；25.9.13 颗粒汇总（Eq 25.28、Table 25.14 D10–D43 应用域、RR 拟合误差报告）；25.9.14 侵蚀后处理（Accumulate 多遍平均、换 injection 丢弃、面量不能按 node 显示、25R2 前数据丢弃）；25.9.15 SCR 沉积风险两法（互不兼容、非预测模型定位；Level-based 四风险等级体系——结晶/二次反应 433 K+HNCO/水力 0–3/总风险平移组合、参数与 compute-level-based-risks、11 个后处理变量、调参免重跑；Weighting-based 0–1 归一——Eq 25.29 时间分数结晶/25.30 HNCO+423–523 K/速度与热流水力因子/总风险加权、自动建报告定义与场函数、Custom Field Functions 后处理变量）；25.10 并行三模式（Shared Memory 仅 Linux 与 host 内存要求、Windows 串行、多相联用禁用、18.2 串行 UDF 不兼容、Workpile 与 wall film 互斥；文件系统同路径要求与 transcript 变通；dpm-load-balancing 与 partition-method-hybrid-2domain TUI；颗粒步数加权自动负载均衡）。**Ch.25 全章（pp. 2771–3004）完成。**
- 扩充知识页 [[Fluent 离散相模型（DPM）]] 至全章完成。
- 提取边界：Eqs 25.23–25.35 公式体未提取按语义记录；Figures 25.67–25.78 为图形元素；Tables 25.13–25.14 提取照录。
- 下一续接位置：Part III / Ch.26 Modeling Macroscopic Particles，从 p. 3005 开始。

### 批次 82：Part III / Ch.26 Modeling Macroscopic Particles 全章（PDF pp. 3005–3026），十批任务（76–85）第 7 批

- 十批连续任务（批次 76–85）第 7 批，22 页（p. 3026 为空白版权页）：26.1 概览与限制（add-on UDF 套件、20–30 单元解析、Re<<1 与密度比≈1 适用域、七条限制）；26.2 加载（addons/mpm、ribbon 或 addon-module 模块号 10、自动 Scheme+UDF 库、仅 3D、默认启用）；26.3 设置 11 步（除 cemented 外瞬态）；26.4 七页设置（Particle Tracking——子步与触单元速度欠松弛、Solve Heat Transfer、颗粒不跨单元；Drag——MDR 默认/MA/Cd/Size Based MA-MDR 四律与 drag factor、多相 Drag Based On 三选；Collision——颗粒-颗粒与颗粒-壁恢复系数/摩擦/滚动摩擦/Substeps；Deposition——壁面沉积 detachment 力与法向/切向速度阈、ASCII 历史、颗粒间团聚；Injections——point/plane/packing/from-file 四类型、Cemented 颗粒与稳态须全 cemented、局部圆柱坐标、连续注入与移动/旋转注入点、Write All Injections 限制；Attraction Forces——n1–n5/G_p/G_w；Initialize MPM——Initialize MPM Functions 挂 UDF、自动 mpm1/mpm3 execute 命令、耦合自动切 PRESTO!、Initialize Particles、Display Particles 四种着色）。**Ch.26 全章（pp. 3005–3026）完成。**
- 新建知识页 [[Fluent 宏观颗粒模型（MPM）]]。
- 提取边界：MDR/MA/弛豫时间与 Theory Guide Eqs 13.6–13.10 公式体未提取按语义记录；Figures 26.1–26.7 为图形元素。
- 下一续接位置：Part III / Ch.27 Modeling Multiphase Flows，从 p. 3027 开始。

### 批次 83：Part III / Ch.27 第 1 段——27.1–27.2（PDF pp. 3027–3089），十批任务（76–85）第 8 批

- 十批连续任务（批次 76–85）第 8 批，63 页：27.1 引言；27.2 使用步骤全节——九步流程（双精度推荐、granular 材料建 fluid 类、20 相上限）；27.2.1 三模型启用输入（Eulerian 的 DDPM/Boiling/Multi-Fluid VOF 开关、Apply 跨页告诫）；27.2.2 体积分数 Explicit/Implicit 语义与稳态选择准则、界面建模三类型与 Interfacial Anti-Diffusion（动态强度 Eq 27.1、指数 1.5/强度 0.75）、Zonal 与 Phase Localized Discretization、离散格式三表（Geo-Reconstruct 最准首选劣质网格、Donor-Acceptor 过时 show-all 命令、保形网格禁零厚壁）、cutoff 默认 1e-6 仅 Explicit 可调上限 1e-4、Expert Options 与 flotsam/节点过滤（0.001）；27.2.3 均质流关滑移；27.2.4 操作密度四法（minimum-phase-averaged 默认）与 Boussinesq（操作密度须 0）；27.2.5 可压流组合规则、Enhanced Numerics 默认、Alternative BC Formulation；27.2.7 Implicit Body Force 与 VOF 轻相操作密度；27.2.8 多相组分输运（Phase Properties 逐相 Full MCD、Stiff 限一混合材料相）；27.2.9 异相反应（Heterogeneous Stiff Chemistry 仅瞬态 Eulerian、分数步、逐反应 Phase+Species、速率函数 none/population-balance（多反应告诫）/arrhenius-rate（仅脱挥发）、完全混合假设）；27.2.10 传质（单机制建议、From 液 To 气规则、同模型覆写规则、替代能量源——RGP 排除、Eq 27.2–27.7 与显焓重定义、Latent Heat 变量与热失衡 Eq 27.10）；七机制——constant-rate（1/时间）/user-defined/population-balance/cavitation（Schnerr-Sauer 气泡数密度 1e11、ZGB 参数、蒸气压五法含 taylor-approximation 与 tabular-ptl-sat、Turbulence Factor 覆写规则、专家选项——蒸发冷凝系数 1/0.2、蒸气压限 1 Pa 与 5 倍、p-limit-method 三法与激波、广义湍流扩散与旧处理、裁剪压力显示与声速 1e30）/evaporation-condensation（Lee 系数 0.1 调参、Thermal Phase Change 缩放因子与单机制限制、tabular-pt-sat 绝对压力插值）/species-mass-transfer（五条件、Raoult/Henry、系数模型 ranz-marshall/hughmark/higbie/zero-resistance/UDF、连续相 RM-hughmark + 弥散相 zero-resistance 推荐、Overall）/boiling（仅 Eulerian）；27.2.11 多相 BC（接触角 90° 语义、Jump Adhesion、出口体积分数 Backflow vs From Neighboring Cell、Slope Limiter 0–2、Tables 27.4–27.9 逐边界分工、Eulerian 质量流进口滑移速度比/体积分数、湍流参数按模型归属、逐相复制不联动）；27.2.12 初始体积分数 patch 与 Patch Reconstructed Interface（良序坐标、仅最后 register）。
- 新建知识页 [[Fluent 多相流模型]]。
- 提取边界：Eq 27.1–27.11 公式体未提取按语义记录；Figures 27.1–27.26 为图形元素；Tables 27.1–27.9 提取照录。
- 下一续接位置：同章 27.3 Setting Up the VOF Model，从 p. 3090 开始。

### 批次 84：Part III / Ch.27 第 2 段——27.3 VOF（PDF pp. 3090–3150），十批任务（76–85）第 9 批

- 十批连续任务（批次 76–85）第 9 批，61 页：27.2.12.2 补遗（Localized Turbulence Initialization——TI 5%/黏度比 10 可调）；27.3 VOF 全节——27.3.1 稳态自动 Global Time Step + Coupled；27.3.2 伪时间法指南（Time Scale Factor 0.3、固定步长应对刚性问题、残差外监测场变量、明渠推荐 Coupled with Volume Fractions）；27.3.3 Coupled Level Set + VOF（伪流修正三选、geo-reconstruct 推荐、零通量默认）；27.3.4 Predefined Criteria 自适应；27.3.5 明渠流全节（启用流程与 Implicit 自动切换、Table 27.10 边界参数、进/出口组与三相规则、自由面/底部液位 Eq 27.12/27.13 与 UDF 瞬态 profile、Total Height Eq 27.14、压力指定三法与三相限制、密度插值三法与振荡告诫、velocity inlet 兼容、轴对称限制、设置建议——Froude 更新间隔 TUI、Froude 无关出口、倒流静压固定、平移 MRF 高速船壳方案）；27.3.6 明渠波 BC（Averaged/Segregated 速度输入、Power Law 廓线指数 0.16、缓冲层自动 0.02、波型四选、Shallow Wave 参数与孤立波 Inlet Offset、Wave Group 五种理论、Wave Spectrum 尾段（频率/角分量数、随机相位告诫）、open-channel-wave-settings 检查报告（H/h 0.78/0.55、H/L 0.142/0.10/0.12、Ursell、谱 min 0.5/max 2.5 峰值频率、海陡度、谱分辨优化流程）、波输入瞬态 profile UDF、Stokes Fenton/Skjelbreia 变体）；27.3.7 初始化 Flat/Wavy 与自动初始化 TUI、set-verbosity 波参数报告；27.3.8 数值海滩（Beach Group ID、Multi/Uni-Directional、Damping Type、线性/二次阻力、相对速度阻力、八条策略含 bottom=自由面−2.5λ 与粗网格建议）；27.3.9 主/二次相选择建议；27.3.10 表面张力（Ca/We 判据、CSF vs CSS、粘附与跳跃粘附、三限制、TUI 光顺参数全录、Smoothed VOF Gradient 后处理、四/六面网格建议与光顺网格依赖告诫）；27.3.10.2 Phase Localized Compressive（三应用示例、slope limiter 0–2 语义与弥散相勿用 2、DEFINE_PROPERTY 变量化、过渡区渐变）；27.3.11 Explicit 子步四法（Velocity/Flux/Hybrid 默认/Flux Averaged、Courant 0.25、每迭代求解与滑移动网格告诫）；27.3.12 熔凝（非熔凝相三参数置 0）；27.3.13 VOF-to-DPM（两方法对比、算法语义与体积守恒、四条限制、九步设置——网格/PUMA/DPM 大 Start Time/Explicit+Sharp+IBF/PISO+Geo-Reconstruct+PRESTO!/URF 0.98/等体积气体平衡/转换参数全套（Frequency/Injection/立即粗化/拆分因子/球径范围/两种 asphericity 0.5/0.5/Transcript 文件与 UDF/Lump Postprocessing/Consider Diffuse Lumps 0.9/1.1）、diffuse lumps 三机制最佳实践、Lump Detection 后处理变量）；27.3.14 DPM-to-VOF（应用场景、双向 LWF↔VOF、双精度、设置七步——材料匹配/Species 启用/液相混合物为主相限制、dpm-to-vof 机制、等体积移气防压力骤增、Auto Adaption 与 Coarsening 告诫、三体积分数阈值（无破碎 0.9/有破碎小值/LWF 0.0001）、膜转换两判据（Film Height Upper + Film/Cell Volume Ratio ≥ +0.1）、质量动量守恒与半球引入）。
- 扩充知识页 [[Fluent 多相流模型]]。
- 提取边界：Eqs 27.12–27.17 公式体未提取按语义记录；Figures 27.27–27.45 为图形元素；Tables 27.10–27.11 提取照录。
- 下一续接位置：同章 27.4 Setting Up the Mixture Model，从 p. 3151 开始。

### 批次 85：Part III / Ch.27 第 3 段——27.4 Mixture + 27.5 Eulerian 前半（PDF pp. 3151–3205），十批任务（76–85）第 10 批（收官）

- 十批连续任务（批次 76–85）第 10 批（收官），55 页：27.4 Mixture 全节——27.4.1 相定义（主相同 VOF、非颗粒二次相 Diameter 语义、颗粒相七参数——Friction Packing Limit 0.61/Granular Temperature/Solids Pressure 三法/Radial Distribution 四法/Elasticity Modulus/Packing Limit 0.63；IAC 输运方程法——sauter-mean 直径、聚并/破碎核 hibiki-ishii/ishii-kim/yao-morel 与 Table 27.12 参数、成核率、临界 We 数、耗散函数 wu-ishii-kim 与水力直径、稳态 URF 1.0 与 iac-pseudo-time-step；代数 IAC 五法 + ia-grad-sym TUI；拖曳子集；滑移 manninen-et-al；表面张力与边界邻单元湍流扩散开关）；27.4.2 漂移力；27.4.3 流型建模（仅代数滑移低 Stokes、Sharp/Dispersed+Regime Based Discretization 自动启用、limiters 1.5、相形态三选、六种相对组合的拖曳/滑移/界面面积默认表、drag-hybrid 与 ia-hybrid 分区拖曳/面积法、AIAD 参数四 TUI、求解策略——Relaxation Time 核验与滑移欠松弛、后处理 Slip 速度/Fcc-Fdd/Relaxation Time）；27.4.4 Singhal et al. 专家空化（TUI 启用、三参数——蒸气压默认 3540 Pa、先建传质机制再启用）；27.4.5 半机理沸腾（适用限制——仅 Mixture/k-ε k-ω 类/重力+零操作密度/温度或 CHT 沸腾壁/二元固定成分 pseudo-fluid；使用流程——Semi-Mechanistic 选项、Reference Velocity/Temperature 三法、Chen 法与 User-Defined、Power Law 叠加常数 2、单相热流三参数、核态沸腾三参数 forster-zuber/chen-steiner、专家选项 hsu 最小过热/最大过热/润湿分数 transition-function（临界 VF 0.2、过渡常数 20）、SMB 热流后处理、UDF；Cell Zone 级沸腾；求解策略——y+>5、低阶、URF 0.5–0.75/0.3–0.5、伪时间 0.1、热流欠松弛 0.8→0.3 TUI、非沸腾验证先行）；27.5 Eulerian 前半——27.5.1 简化指南；27.5.2 相定义（颗粒参数同 Mixture）；27.5.2.5 相间作用全节：拖曳函数 20 余种全录（ishii 限沸腾、schiller-naumann(-pb)、morsi-alexander、symmetric（MF-VOF 默认）、grace 与 swarm 修正 Cexp 指数语义、tomiyama、ishii-zuber 气泡群、anisotropic 自由面、universal-drag、wen-yu(-pb)、gidaspow、syamlal-obrien(-para 两输入与 Geldart B/-symmetric)、huilin-gidaspow、gibilaro、emms、filtered 自动属性、constant/expression/UDF 返回拖曳函数/none）、拖曳修正四法（brucato/wall-drag-enhancement）、恢复系数 0.9、升力七法（moraga/saffman-mei/legendre-magnaudet/tomiyama 交叉点/hessenkemper-et-al）与适用告诫、Shaver-Podowski 升力关联、壁面润滑三法（lubchenko 前置条件/antal Cw1-Cw2/tomiyama 仅管道）、湍流扩散五法（lopez-de-bertodano/simonin/burns-et-al/diffusion-in-vof/UDF 向量版 + Limiting Function 三式与上下限 TUI）、表面张力同 VOF、虚拟质量力；27.5.3 湍流（Mixture 默认/Dispersed/Per Phase 三选；湍流交互源项——默认不含、troshko-hassan（Cke/Ctd）/sato/simonin-et-al（限 Dispersed/Per Phase、含漂移湍动能源）、禁混用、先无源后有源策略、多数可忽略）。
- 扩充知识页 [[Fluent 多相流模型]]。
- 提取边界：Eqs 27.20–27.21 及 Theory Guide 引用式（14.x 系列）公式体未提取按语义记录；Figures 27.46–27.69 为图形元素；Table 27.12 提取照录。
- 下一续接位置：Part III / Ch.27 27.5.4 Including Heat Transfer Effects，从 p. 3205 开始。**用户指定的十批连续任务（批次 76–85）全部完成（10/10）。**

### 批次 86：Part III / Ch.27 第 4 段——27.5.4–27.5.11（PDF pp. 3205–3242），十批任务（86–95）第 1 批

- 新十批连续任务（批次 86–95）第 1 批，38 页：27.5.4 换热（十种换热系数相关式——constant-htc/nusselt/gunn/ranz-marshall/hughmark/tomiyama/none/UDF/fixed-to-sat-temp/two-resistance 及 time-scale 与 zero-resistance 子模型、Return-to-Saturation Time Scale、多沸腾机制禁 two-resistance 告诫）；27.5.5 代数 IAC 三法；27.5.6 AIAD（限制——不兼容 DDPM/Boiling；两相即可、夹带需第三相、相同材料；自动启用 MF-VOF+Sharp/Dispersed+Phase Localized；相处理三选项；力限制；drag-aiad 参数对话框四组；aiad-entrained-absorption 机制与 γ 系数、不可移除；ia-aiad；自动 k-ω SST/湍流阻尼/Per Phase/SWT；重力与瞬态自动启用；URF 保守值；夹带先关后开与 Vaporization Mass URF 0.2）；27.5.7 GENTOP（不兼容四模型；非均相 Eulerian+GENTOP、自动三相/gentop-complete-coalescence/PBM Inhomogeneous Discrete 不可改；校准系数 1.0；GENTOP Hybrid Phase Modeling 与同材料规则；主-GENTOP 拖曳限三法、湍流扩散与交互不可用）；27.5.8 DDPM（自动启用 DPM、VF Approaching Continuous Flow Limit 与 Transition Factor 0.75→0.5625、Discrete Phase Domain 下拉、能量耦合三 TUI——enhanced inter-phase exchange/via source term/linearized；颗粒离散相 VF Approaching Packing Limit + Enhanced Numerics + Transition Factor 0.75×0.63=0.4725）；27.5.9 沸腾模型 13 步全节（限制三条；自动默认表 0.07 N/m/ishii/tomiyama/boiling-dia/two-resistance；三模型 RPI/Non-equilibrium/CHF；liquid-vof-factor 与 thin-film TUI；Standard State Enthalpy 必须；气泡直径 Default/Unal、CHF 液滴直径 constant/blending；力五项沸腾流典型选法；Boiling Model 对话框全参数——界面传递系数 1、饱和温度绝对压力、脱离直径四法、cole 频率、成核密度三法、面积影响 delvalle-kenning、混合函数 lavieville/tentner/ioilev、NLBF（y+<30、线采样二阶平均、两参数、NLBF Averaged Temperature）、淬冷修正 Eq 27.25（等待系数 1、fixed y+ 250/fixed liquid temperature Eqs 27.26–27.28 与 VF 限 0.05/0.3）；two-resistance-boiling-framework TUI；ia-symmetric/particle/ishii；壁 BC 三类禁薄壁；Coupled 耦合；URF 系列 Courant 1–20 等；沸腾后处理八变量）；27.5.10 多分散沸腾（三相同汽材料、双 boiling 机制、成核仅在最小 bin 相、pb-boiling 自动与 sauter-mean）；27.5.11 Multi-Fluid VOF（不兼容 DDPM；界面建模联动拖曳法选择表；各向异性拖曳仅兼容 Mixture 湍流、mpmfluid-aniso-drag 参数 1000000/10/0.0001）。
- 扩充知识页 [[Fluent 多相流模型]]。
- 提取边界：Eqs 27.22–27.28 中出现的淬冷式与液参考温式（27.25–27.28）公式体未提取按语义记录；Figures 27.70–27.88 为图形元素。
- 下一续接位置：同章 27.6 Population Balance Model，从 p. 3243 开始。

### 批次 87：Part III / Ch.27 第 5 段——27.6 Population Balance（PDF pp. 3243–3287），十批任务（86–95）第 2 批

- 新十批连续任务（批次 86–95）第 2 批，45 页：27.6 PBM 全节——27.6.1.1 启用（双精度、Mixture/Eulerian、Method 五选：Discrete（Kv/Geometric Ratio 或 File/Bins ≤50/Print Bins）、Inhomogeneous Discrete（Active Secondary Phases、带相名 File 格式）、Standard Moment、Quadrature Moment（4/6/8 矩）、QBMM（2/4/6/8 尺寸矩）、DQMOM（三相、Reference Length/Min VOF/Max VOF Change、限四相系统、瞬态、无成核）；Phenomena 四项（成核/生长 Inhomogeneous 不可用、聚合/破碎）；VF cutoff 0.8；Include Expansion 仅 Discrete/QMOM/Inhomogeneous、可压二次相；聚合核六种（constant/liao 七参数/luo/free-molecular/turbulent Hamaker/prince-blanch 五参数/UDF）+ Aggregation Factor；破碎核频率七种（liao 四系数/luo/lehr 临界 We/ghadiri/laakkonen C2/martinez-bazan 搅拌槽/UDF）+ PDF 五种（parabolic 形状因子/laakkonen/generalized/inverted-u/UDF）；27.6.1.1.3 QBMM 专家 TUI 全套（advection-cfl ≤0.5 与五种 CFL 法、积分步 250、SSP-RK2/3/Euler/RK4、容差 1e-8/1e-6、源时间因子 0.9/0.5/2.0、verbosity 0–4、zero-moment/zeta ±1e-12 可调）；27.6.1.1.4 DQMOM 值生成（PDF/CDF/Overall Moments 三格式照录、QP0–QP2、乘真实 VF）；27.6.1.2 边界条件（Specified Value/Flux 逐 bin/矩、Log Normal 自动初始化仅全 Specified Value）；27.6.1.3 cell zone；27.6.1.6 成核生长传质（Eqs 27.30–27.34、离散法源项守恒 C_PB_DISCI_PS、SMM 尺寸无关生长、QBMM/QMOM 忽略成核、结晶须主相 Species Transport、population-balance 机制/反应速率函数免 UDF）；27.6.1.7 Size Calculator（气泡四判据——经验下限/升力反转/Eo=10/4×毛细长；液滴三判据——We=12/Taylor 2×毛细长）；27.6.2 QMOM 低 VF 源保留 TUI；27.6.3 后处理变量全集（Bin-i-fraction 等、扩散系数恒 0、非均相 bin-0 最大 bin-(n-1) 最小、QMOM Abscissa/Weight、DQMOM-m4）与 Moments/NDF 对话框（.pb 文件）；27.6.4 PBM UDF 宏（DEFINE_PB_NUCLEATION_RATE KCl 结晶完整示例、DEFINE_PB_GROWTH_RATE）。
- 扩充知识页 [[Fluent 多相流模型]]。
- 提取边界：Eqs 27.30–27.34 及 Theory Guide 14.x 引用式公式体未提取按语义记录；Figures 27.89–27.109 为图形元素；Table 27.12 提取照录。
- 下一续接位置：同章 27.7 Setting Up the Wet Steam Model，从 p. 3288 开始。

### 批次 88：Part III / Ch.27 第 6 段——27.7–27.10 收官（PDF pp. 3288–3334），十批任务（86–95）第 3 批

- 新十批连续任务（批次 86–95）第 3 批，47 页，**Ch.27 全章完成**：27.7 Wet Steam（27.7.1–27.7.5 用户输入与理论；选项 TUI 全套——define/models/multiphase/wet-steam/droplet-growth-rate young/hill、virial-equation vukalovich/young、rgp-tables 由表格替代解析性质、stagnation-conditions 相变判据、zonal-phase-change 限相变区、enhanced-source-linearization 收敛强化；UDWSPF 自定义湿蒸汽性质：16 个必需 C 函数——wetst_init/satP/satT/eosP/eosRHO/cpv/cvv/hv/sv/muv/ktv/rhol/cpl/mul/ktl/surft，WS_Functions 结构体 WetSteamFunctionList 装配、编译加载 TUI 流程）；27.8 多相求解策略（27.8.1 通用七小节：双精度建议；压力速度耦合五法 Coupled/PC-SIMPLE/PISO/SIMPLE/SIMPLEC 适用性与 Coupled with Volume Fractions 告诫；2020R1 默认控制与 2020R1 前差异 TUI；27.8.1.5 VOF 稳定性——参考压力位置设于最疏相、PRESTO! 非结构变体、网格差用 Geo-Reconstruct、网格好用 Compressive、BGM 收敛慢告诫、Rhie-Chow 处理选项、PISO 瞬态 URF=1、稳态 URF 0.2–0.5；27.8.2 模型专属：VOF/Mixture——滑移速度 URF ≤0.2 与初场技巧；Eulerian 四种初场方法；Wet Steam 策略）；27.9 求解前检查 define/report/mphase-summary 十五类检查项（相数/主相/BC/材料/操作条件/热交换等逐项核对照录）；27.10 后处理（各模型专属变量清单——VOF/Mixture/Eulerian/组分/湿蒸汽/DDPM；速度矢量逐相；相索引含义；Fluxes/Forces/Flow Rate 按相报告；逐相体积积分）。
- 扩充知识页 [[Fluent 多相流模型]]（**Ch.27 全章完成**，pp. 3027–3334）。
- 提取边界：Eqs 27.36–27.43（耦合求解器矩阵/修正）公式体未提取按语义记录；Figures 27.110–27.115 为图形元素；UDWSPF 十六函数与结构体照录。
- 下一续接位置：Part III / Ch.28 Modeling Solidification and Melting，从 p. 3335 开始。

### 批次 89：Part III / Ch.28 Modeling Solidification and Melting 全章（PDF pp. 3334–3342），十批任务（86–95）第 4 批

- 新十批连续任务（批次 86–95）第 4 批，8 页（3335–3342），**Ch.28 全章完成**：28.1 设置流程（Solidification & Melting 对话框启用并自动开能量方程；Mushy Zone Parameter A_mush（Eq 15.6，常量或 DEFINE_SOLIDIFICATION_PARAMS UDF）**推荐 10⁴–10⁷**、过大振荡；Include/Compute Pull Velocities 与 Flow Iterations Per Pull Velocity Iteration 默认 1；Lever/Scheil 规则仅 Species Transport 下可用、Scheil 可加 Back Diffusion γ∈[0,1]（Eq 15.19）；材料四参数——Pure Solvent Melting Heat L 必须>0、Solidus/Liquidus Temperature；多组分：mixing-law（Eq 15.8/15.9）或 DEFINE_PROPERTY 且固/液相线须同法、Mass Diffusivity、Eutectic Temperature、溶剂（Selected Species 最后一项）的熔化热/熔点、逐溶质液相线斜率/分配系数/共晶质量分数/Diffusion in Solid；壁面 Contact Resistance 气隙阻力（Eq 15.23）、Marangoni Stress 剪切条件）；28.2 连续铸造 pull velocity 三法（patch 常量/场函数——全域 patch 仅液相分数<1 生效；全程计算 Eq 15.22 代价高；只算一步后关闭沿用）；28.3 热/溶质浮力（两开关仅凝固+Species Transport 组合可用；Solutal Expansion Coefficient 除末组分全设；默认共晶分数作参考质量分数、TUI define/models/solidification-melting 自定义参考分数流程）；28.4 求解（先 patch 温度或稳态导热初场、推荐瞬态；Liquid Fraction Update URF α_β，Eq 28.1 β_{n+1}=β_n+α_β Δβ；四类易收敛困难工况——稳态/连铸/多组分/mushy 常数大）；28.5 后处理（Solidification/Melting 类别五变量——Liquid Fraction、Contact Resistivity 全可用，Pull Velocity 六分量需 pull velocity，Liquidus/Solidus Temperature 仅多组分）。
- 新建知识页 [[Fluent 熔化与凝固]]（**Ch.28 全章完成**，pp. 3335–3342）。
- 提取边界：Theory Guide Eq 15.3–15.23 公式体未提取按引用记录；Figures 28.1–28.4 为图形元素；p. 3336 的 A_mush 推荐范围与 p. 3341 的 Eq 28.1 经 fitz 300 dpi 渲染核实；α_β 数值默认本章未印出。
- 下一续接位置：Part III / Ch.29 Modeling Fluid-Structure Interaction，从 p. 3343 开始。

### 批次 90：Part III / Ch.29 Intrinsic FSI 全章（PDF pp. 3343–3354），十批任务（86–95）第 5 批

- 新十批连续任务（批次 86–95）第 5 批，12 页（3343–3354），**Ch.29 全章完成**：29.1 概览与限制（intrinsic FSI 单向/双向区分——单向可先流后固、双向必须动网格+瞬态；结构单元类型 2D quad/tri、3D hex/tet/wedge/pyramid、禁多面体与 hexcore；FSI 启动后禁换网格；wall/wall-shadow 分隔与至少一个固体区；禁 In-Cylinder/Six DOF/Contact Detection；壁面 UDF 仅 DEFINE_SOURCE_FE/DEFINE_WALL_NODAL_DISP/DEFINE_WALL_NODAL_FORCE、禁 Shell Conduction；不兼容网格自适应/morpher/英制与 CGS/FMG/自适应时间步；Workbench 下不可用；Linear Elasticity 限屈服强度内、兼容 2D 轴对称；Structure 变量仅固体区、周期边界按无应力）。29.2 设置十六步（双精度建议；General 时间相关性与 Gravity；固体区 Frame Motion 旋转；双向先收敛流体；Structural Model 对话框——Linear/Nonlinear Elasticity、Thermal Effects 需能量方程、Newman's P2D Battery Effects 与 resolved Li-ion Battery Effects 自动启用不可关；材料 Youngs Modulus/Poisson Ratio/热弹性加 Starting Temperature 与 Thermal Expansion、非常数起始温度场 re-initialization TUI 输 1；DEFINE_PROPERTY/SOURCE_FE/WALL_NODAL_*；Wall Structure 选项卡五类位移边界——Stress Free/Node Force/Node Displacement/Face Pressure/Intrinsic FSI 限 wall-shadow 对、可用表达式；对称面策略与刚体运动病态告警；双向动网格——Smoothing 三法/Implicit Update 强耦合/Intrinsic FSI 动网格区域；Structure Transient Formulation Newmark 默认或 Backward Euler；线性求解器 BCGSTAB 默认+GMRES 自动回退"fe-structure"提示、max-iter 默认 500、GMRES 建议 50 起、CG 最快最不稳、amg-stabilization 切换；numerical-damping-factor（Eq 16.16）；expert 三开关 explicit-fsi-force/include-pop-in-fsi-force/include-viscous-fsi-force；shear locking 与 enhanced-strain（2D quad/3D hex）；Rayleigh 阻尼两系数；结构点面与报告定义；初始化位移初值；**仅支持 CFF 写 case/data**；单向先流后构提速、先稳态；Structure 类别后处理变量——Total/X/Y/Z Displacement、Sigma 六分量、von Mises 自动计算、表达式/min-max/XY 图不受固体区限制）。29.2.1 非一致界面（仅流体-固体、禁固-固；Mesh Interfaces → New 流程、intersection facets 自动计算）。
- 新建知识页 [[Fluent 流固耦合（FSI）]]（**Ch.29 全章完成**，pp. 3343–3354）。
- 提取边界：Theory Guide Eq 16.16 未提取按引用记录；Figures 29.1–29.3 图形元素。
- 下一续接位置：Part III / Ch.30 Modeling Eulerian Wall Films，从 p. 3355 开始。

### 批次 91：Part III / Ch.30 Eulerian Wall Films 全章（PDF pp. 3355–3380），十批任务（86–95）第 6 批

- 新十批连续任务（批次 86–95）第 6 批，26 页（3355–3380，p. 3380 为空页），**Ch.30 全章完成**：30.1 限制（仅 3D；VOF/辐射等需 UDF 改 BC 才能正确交互；隔板交接非物理——孤立膜壁不得共边；单组分；不兼容非一致界面/Overset/网格操作 fuse 等（cell/face 分合兼容）/运动变形网格与旋转平移参考系（运动或旋转边界兼容）/LWF——启用后 DPM BC 下拉无 wall-film）；30.2 工作流七步与网格/区域操作影响（Make Polyhedra 自动恢复但数据丢弃、cell zone 分合需手动重启用、face zone 分合后须重初始化；网格自适应兼容数据保留、VOF 耦合判据可能需调整；改网格前须禁用 EWF）；30.3 模型选项（Solution Options——Solve Momentum/Energy/Scalar、DPM Coupling、Phase Coupling、Treat Sharp Edge；Momentum Options——Analytical Solution 或 Momentum Equation 五项（Gravity/Surface Shear/Pressure Gradient/Spreading 需 PG+Gravity/Surface Tension 需 PG）；Material Options——材料类型三选、属性方法五法（UDF 禁流体比热、default-method 限饱和压力）；DPM Interaction——Particle Splashing、Source Smoothing 默认 level 2/factor 0.5、Edge Separation 四参、Particle Stripping 三参、DPM 三要点（至少一个 injection、材料同名加后缀、自动 ewf-strip-sep-injection 与 -pcle 材料）；Phase Interaction——Phase Change（膜材料二次相禁组分混合物）/Phase Accretion/VOF Coupling（Transition Base 两判据）；Solve Wall Film 开关与必须先 Initialize）；30.4 求解控制（时间离散四法——High Order Explicit 默认阶 2 可升 3/4 TUI 全提示、空间一/二阶迎风、Maximum Thickness、Coupled Solution 与 Curvature Smoothing、稳态专属 Time Step 或 Adaptive（Courant/初值/升降因子均>1）、瞬态专属 Per Flow Iterations（0=步末）/子步数/Reporting Interval、隐式专属 Sub-Iteration Stop/次数/报告间隔、DPM 的 Film Steps per DPM Step 与松弛因子——限 DPM 关连续相交互时）；30.5 Wall 选项卡六子页（边界类型——质量/动量/温度/标量通量与动壁 Relative 选项、Flow Momentum Coupling 单双向；源项——五通量与能量源须配质量源告诫；相变三模型 diffusion-balance/wall-boundary-layer/user-defined（正 kg/s）；Surface Contact 部分润湿三参（Mean 0–180°、RSD 0–50%、Beta 0–10）；DPM Interaction 撞击三模型 stanton-rutland/kuhnke（Ra/Rz/Critical Temperature Factor）/stochastic kuhnke（五参）与 DEFINE_IMPINGEMENT/FILM_REGIME/SPLASHING_DISTRIBUTION 覆盖、DPM Wall Splash、Allow Boundary Separation；VOF Interaction——判据 Film-to-VOF 必须大于 VOF-to-Film、松弛因子默认 0.5、阈值打印控制台）；30.6 EWF-VOF 耦合六步；30.7 后处理（三十余变量按选项条件、Flux Reports 增 Film Mass Flow Rate/Film Heat Transfer Rate——能量通量只计外部边界、TUI report/fluxes/film-mass-flow 与 film-heat-transfer）。
- 新建知识页 [[Fluent Eulerian 壁面液膜]]（**Ch.30 全章完成**，pp. 3355–3380）。
- 提取边界：Theory Guide Eq 17.2/17.3/17.29/17.38 与 Eq 12.245–12.273 公式体未提取按引用记录；Figures 30.1–30.10 图形元素；p. 3380 空页。
- 下一续接位置：Part III / Ch.31 Modeling Electric Potential Field and Electrochemistry，从 p. 3381 开始。

### 批次 92：Part III / Ch.31 Electric Potential Field and Electrochemistry 全章（PDF pp. 3381–3426），十批任务（86–95）第 7 批

- 新十批连续任务（批次 86–95）第 7 批，46 页（3381–3426，p. 3426 空页），**Ch.31 全章完成**：31.1 电势场（启用电化学自动启用电势求解器；限制禁 shell conduction 壁面；设置六步——Potential Equation、Include Joule Heating 需能量方程、Electrical Conductivity、导电壁 Potential BC 三选 Specified Flux/Specified Value/Coupled（wall-shadow 对）与 Contact Resistance（Eq 18.3）、其他边界默认零电流、cell zone Fixed Values/Source Terms）。31.2 精细锂离子电池（小电极尺度专用、整电池用 MSMD 见 Ch.32；限制——电极区固体/电解液区流体、仅全电池；五选项卡——Zone Selection；Echem Rate Butler-Volmer 七参（Eq 18.13）+线性化选项+DEFINE_EC_KINETICS_PARAMETER；Material Properties 浓度五项与迁移数/活度项（Eq 18.8/18.12）；Advanced——老化三模型（SEI 生长八参 Eq 18.28–18.37、析锂六参含 Frac. of Li+ Forming SEI、正极膜生长四参）与少循环看趋势告诫、肿胀+FSI（Swell Coefficient/Reference Concentration Eq 18.38、DEFINE_LITHIUM_SWELL_STRAIN、结构单元仅 hex/wedge/pyramid 禁多面体、Li-ion Battery Effects 自动启用）、专家三开关（Li-Migration 默认开、两二次梯度修正可关）；设置流程 16 步——阳极 Specified Value 0、阴极电流密度符号约定、锂方程免边界、收敛准则收紧（电位 1e-10/锂 1e-12）、无流动时禁 Flow/Energy、Faradaic Interface Current URF 默认 0.01/UDF 平衡电位时低至 0.001、自动报告定义 li-ion-battery-soc/capacity、Report 页 SOC 设置与 Compute 电流平衡检查、老化另报损失锂质量与容量损失因子）。31.3 电化学器件（几何七区+集流体；自动启用 Mixture+组分输运、禁 VOF/Eulerian；Device Type 七选 PEM/碱性电解、H2 Pump、PEM FC、SOFC、SOEC、Customized；MEA 三法 Resolved/Unresolved 0D/1D；Options 九项（Butler-Volmer 默认否则 Tafel、Half Cell Voltage Nernst、Osmotic Drag、Capillary Pressure 仅多相、Phase Change、Water Content 等）；Electrical System Setup 三法（BC 面板/总电压/总电流——均自动置阴极 tab 零）；Parameters（J_ref/Ea/T_ref/C_ref/Con.Exponent 可用性按器件、Std.State E0、Entropy、Open Voltage、标准温压、蒸发冷凝速率、OSM_drag 默认 1.0/0.001；Customized 反应与机理对话框流程 Eq 7.118–7.120）；Anode/Cathode 四 Zone Type（集流体默认材料电导率表 1e6/1e4/1e4/1e-16 与 1e-16/1e-16/2.3677/2.3677；多孔层 Porosity/渗透率/Leverett 毛细压力三系数 1.417/2.12/1.263；催化层 Resolved 加 Surface Volume Ratio、Unresolved 三参直接给电解液电导）；Electrolyte（Resolved 区+材料+渗透选项 Eq 18.43；Unresolved 选 wall-shadow 对与 Membrane Thickness/电导 Eq 18.50）；Electrical Tabs；Customization 两 UDF；Advanced（Contact Resistivity 逐面施加单侧设置、Membrane Species Diffusion 默认 1e-15=不考虑）；求解策略——前 10–20 迭代关 Joule 热与电化学源）。31.4 后处理（电势场 Properties/Potential 两类别变量与各向异性显示为零告诫；Lithium 类别浓度/通量/过电位/老化/肿胀变量；电解 Potential 类别六变量；矢量图 Electric Current 与 Lithium Mass Flux）。
- 新建知识页 [[Fluent 电势场与电化学]]（**Ch.31 全章完成**，pp. 3381–3426）。
- 提取边界：Theory Guide Eq 5.1/7.118–7.120/8.4/18.x/20.x 公式体未提取按引用记录；符号占位缺失按名称语义记录；p. 3411 默认电导率表照录；Figures 31.1–31.19 图形元素；原文两疑误照录（Membrane Thickness 描述文字、31.3 开头用途表述与 Device Type 清单不一致）；p. 3426 空页。
- 下一续接位置：Part III / Ch.32 Modeling Batteries，从 p. 3427 开始。

### 批次 93：Part III / Ch.32 Modeling Batteries 第 1 段——32.1–32.2.3.4.4（PDF pp. 3427–3470），十批任务（86–95）第 8 批

- 新十批连续任务（批次 86–95）第 8 批，44 页（3427–3470），Ch.32 段 1/3：32.1 引言（MSMD 正交各向异性连续体、两电位方程；四电化学子模型 NTGK/DCIR、ECM、Newman P2D、User-defined；均匀热源法 CHT/FMU-CHT/Circuit Network；通用流程十步）。32.2.1 限制（包内电池初始相同、仅 nPmS、tab 必须连续面、真实或虚拟连接连通）。32.2.2 几何（不解析极片、活跃区+被动区两分）。32.2.3 设置：七选项卡总览（Apply/Reset）；32.2.3.1 Model Options——Solution Method 四选（CHT/FMU-CHT/Circuit Network 无或一电位方程、MSMD 两方程；ROM 须先跑 3 步作参考场、Number of Sub-Steps/Time Step、内部短路仅 MSMD 禁 ROM）；E-Chemistry 四模型特性（NTGK/DCIR 连续两方程无跳变条件、不能捕捉动态惯性响应；ECM 半经验；P2D 最全面最贵；User-defined 需 cae_user.c 的 user_defined_echem_model()）；Energy Source 三开关默认开；Solution Controls——Current URF 默认 0.8（荐 0.8–1.0）、Voltage Correction URF 默认 1.0、Cluster Cells 仅 ECM/P2D（Static Nx/Ny/Nz 默认 1/1/1 纯几何、Dynamic 目标变量 voltage/temperature/DEFINE_BATTERY_CLUSTER 每步成簇）；Electrical Parameters——Nominal Capacity、Life Model、Solution Options 六选（Specified C-Rate 电流=C-Rate×标称容量不计连接 2P2S 例、System Current/Voltage/Power/Resistance、Set in BC、Profile/Data Table；Echem Stop Criterion 电压或 SOC 每步检查）；32.2.3.1.1 Life Model（Calender Time/Cycle Number/Operation Temperature 非 CFD 温度；Calendar 四参 Eq 19.50；Battery Aging Table 温度×循环各≤20 层 Write/Read）；32.2.3.1.2 Profile/Data Table（Time-Scheduled 三列类型码 0–4 照录示例；Event-Scheduled 五列 FC 码 1–8 照录示例；时间表可改事件表反向不可；Table Data 快充 2D 表温度法取多报告定义最小值、四插值法 bilinear/staircase-floor/staircase-ceiling/corner minimum 数值示例 11.25/7.5/15/5）；32.2.3.1.3 查找表（plain text 2D 六行结构与 3D z-value 结构、compact scheme 括号格式与末位 0=bilinear 必用）；32.2.3.2 Conductive Zones（活跃/被动区、Display 按钮、分组合并减区）；32.2.3.3 Electric Contacts（Specific Contact Resistance；虚拟连接两格式——tab surface-based mP/nS 顺序 1P1S…mPnS、active zone volume-based 每电池一行多 cell 空格分隔且仅限无 Joule 热 Circuit Network（自动启用并禁 Joule）、Print Battery System Connection Information 核对）；32.2.3.4 Model Parameters——CHT（total Energy Source+Tab Electric Current、.ttab 瞬态 profile 格式、Use Same Settings）；FMU-CHT（Tcell 输出参数、FMU 对话框、Energy Source Mapping）；NTGK/DCIR（Initial DoD 默认 0=满电、Reference Capacity Eq 19.5；U/Y 五数据类型——Polynomial/Table（DOD≤50×温度≤20、默认 Kim 论文 315 须换）/Raw Data（导入放电曲线、Capacity Fade 自动生成不可改、改开关须重载）/Parameter Estimation/Internal Resistance（DCIR 3D 表按电流层正放负充、U Table 可选无 U 表限 current/C-rate+单电池纯串联）；Limiting Current 3D 表；Parameter Estimation——容量核对、DOD 层 10–20 默认 20、Min/Max 0.01/0.95、至少两 C-rate 文件、Crate/Temperature/time-voltage 格式、多温度→Table 自动/单温度→Polynomial 默认、Visualize、TUI p. 3525）；ECM（Initial SOC 默认 1、Rs/R1/R2/C1/C2/Voc 四数据类型 Chen 默认须换、充放电不同系数选项；Parameter Estimation——4P/6P 电路、JH（仅弛豫段）与 LM（脉冲+弛豫、先 JH 初值、失败警告）、HPPC 文件 SOC/I/Temperature/time-voltage 须含静置脉冲弛豫三段、每温度≥1 SOC 且覆盖仿真范围、两加载法、多温度→Table/单温度→Polynomial/充放双跑自动分参数组、6P 物理多 4P 稳 JH 比 LM 稳先 6P 后 4P、Visualize、TUI p. 3526；HPPC Library 仅 Generic-Cell、路径 addons/msmdbatt/hppc_database、目录约定 discharge/charge 一级+容量带 Ah、参数估计仅 discharge 支路单 C-rate）。32.2.3.4.5 Newman's P2D 节始于 p. 3470（正文在下段）。
- 新建知识页 [[Fluent 电池模型]]（Ch.32 段 1/3 完成，pp. 3427–3470）。
- 提取边界：Theory Guide Eq 19.x 公式体未提取按引用记录；Figures 32.1–32.20 图形元素；示例文件格式照录。
- 下一续接位置：同章 32.2.3.4.5 Inputs for the Newman's P2D Model 正文，从 p. 3471 开始。

### 批次 94：Part III / Ch.32 Modeling Batteries 第 2 段——32.2.3.4.5–32.2.3.6.7（PDF pp. 3471–3510），十批任务（86–95）第 9 批

- 新十批连续任务（批次 86–95）第 9 批，40 页（3471–3510），Ch.32 段 2/3：32.2.3.4.5 Newman P2D 输入全节（Theoretical Capacity 自动算；Initial SOC 默认 1；正/负极与隔膜三列三十余参数——Thickness/网格数与偏置比/颗粒直径/Solid 网格/Cs,max/Stoi 0%·100%/Init.Cs·Ce/VOF/Filler/Ds·Ed/Brugg（非 BPX）/Tran.Efficiency（BPX）/电导/速率常数·Er/传递系数/OCP·dU/dT/De·Ede/t+/Ionic·Ek/Activity；参数四形式 constant/piecewise-linear/polynomial/DEFINE_BATTERY_PROPERTY；echem 材料数据库三类型 Copy 与 Import BPX（json 开放标准、Import-BPX<ID> 自动材料、与 Fluent 三公式差异——比表面积算出 vs 显式、Bruggeman vs transport efficiency、BV 速率常数换算）；数据库文件 addons/msmd-batt/lib/echem_database.scm 可扩；Use Analytical Cs 降阶+Cs Function Order；Include Aging Effects 稳态 profile（独立模式生成自动可用）；Include Swelling Effects——Swell Coefficient（Eq 19.74）/Young's Modulus/Neutral Swell SOC（四参数按中性 SOC 给值）/Electrode Layer Orientation 四式（Pouch 法向/Cylinder 轴/Rounded Prismatic 双矢量/DEFINE_BATTERY_SWELL_LAYER_N；Eq 16.41）；独立模式机械载荷三型 External Pressure（正=压缩 Eq 19.83）/Total Deformation（Eq 19.84）/External Stiffness（Eq 19.85）；默认取 Cai & White [90]）。32.2.3.4.6 User-Defined E-Model（Memories per Cell/Initial SOC/Reference Capacity）。32.2.3.5 UDF 选项卡（宏清单见 Customization Manual）。32.2.3.6 Advanced Options 九功能：32.2.3.6.1 独立 Echem（Report Time Step/Total Run Time/Ref Temperature、P2D 肿胀 Mechanical Load 三型；Draw Profile；NTGK/ECM/P2D 输出 profile 名与变量清单——P2D 四位置 x=lnsp/lns/ln/0 与空间场六变量、SI 单位）；32.2.3.6.2 独立老化（P2D+Using Profile 单循环、Enable Physics-Based Battery Life Model、Total Run No. of Cycle 少循环先试、SEI 八参（Eq 19.61–19.67）+析锂五参（Eq 19.59–19.62）、Aging Speed Multiplier/每 N 循环存 profile/Start from Aged Battery、输出 aging-cycle-history-profile 四变量与 aging-field-profile.prof 十字段、Scenario A/B 自定义 profile 最低字段、x 坐标自动映射）；32.2.3.6.3 Pack Builder（模块+冷板两 case、定位手输/导入 12 数行文件（平移 xyz+原点 xyz+轴 xyz+角度+NS NP）、先旋后移、Build 覆盖几何、module#/coldplate 前缀、控制台 2S3P×8s1p 示例、对齐用户负责、Create NCI 建议手选配对面一对一法、冻结流场+Init 按钮纯电池仿真、限制——产物不能再作模块 case）；32.2.3.6.4 ROM Tool Kit（LTI 原理与成立条件恒流量恒物性线性 BC、SVD 降维、Twin Builder 联用；ROM Data Creator——LTI/SVD、输入 Volume Heat 组/个体与组内分配、Face Heat Flux 带 profile 四列 x y z flux 归一化、Face Temperature、Tab Current for Joule、LTI 输出五类、SVD 导出温度区、Transient Setup parametric 四参+停止条件 Max Time 与 Max dT_duration/T_range 或 file 三列、保存频率默认不存、Run Training 顺序跑存 LTI//SVD/；LTI-ROM Generation——Min/Max Order、Target Relative Error、0 阶容差忽略交叉加热、NonZero StepRes Slop 三选（绝热不停稳）、生成 Thermal_ROM_Matlab.m 与 Input_ROMconfig.txt 回读；SVD-ROM Post-Processing——Basis File+Transient Coefficient File 重建场与动画）；32.2.3.6.5 正交各向异性导热（逐材料繁琐 vs 内置工具 Orthotropic Material...——三 cell 型+方位矢量+Layer Normal/In-Plane 分量、自动定原点施加全部活跃区、Pack Builder 联动自动更新、两告诫单活跃区+方位一致）；32.2.3.6.6 经验肿胀（仅 NTGK/DCIR 与 ECM、Battery Swelling Model...、Swell Coefficient/Neutral SOC/取向同 P2D、DEFINE_BATTERY_SWELL_STRAIN）；32.2.3.6.7 Venting（Gas Release Faces 限活跃区-流体区之间面、Species Model 三选或 Phase of Venting Gas、组分质量分数、Release 两法——Abuse Rate 按一/四/N 方程热滥用（Eq 19.46–19.48）或 File Input（Activation Temperature+三列时间/温度/速率文件）、后处理 Venting Gas Mass Source、当前版本无 venting 阀门模型）。
- 扩充知识页 [[Fluent 电池模型]]（Ch.32 段 2/3 完成，pp. 3471–3510）。
- 提取边界：Theory Guide Eq 19.x/16.41 公式体未提取按引用记录；Figures 32.21–32.37 图形元素；BPX 站点 URL 原文作 http://www.ilight.com（疑为 -ilight.com 之误）照录并标注。
- 下一续接位置：同章 32.2.3.6.8 Including the Entropic Heat Effects，从 p. 3511 开始。

### 批次 95：Part III / Ch.32 Modeling Batteries 第 3 段收官——32.2.3.6.8–32.2.9（PDF pp. 3511–3536），十批任务（86–95）第 10 批

- 新十批连续任务（批次 86–95）第 10 批，26 页（3511–3536，p. 3536 空页），**Ch.32 全章完成**：32.2.3.6.8 熵热（Include Entropic Heat；Data Table 双充放表或 DEFINE_BATTERY_ENTROPIC_HEAT；P2D 可直接给正负极 dU/dT 或单一合并值——勿双重计入）。32.2.3.6.9 热滥用模型（One/Four/N-Equation 三动力学——One-Equation 三速率类型 Arrhenius（Eq 19.35–36 常数）/Table Data（dT/dt 表）/DEFINE_BATTERY_ABUSE_RATE，Enable Internal Short Heat 五常数 A_ec/E_ec/H_ec/T_trigger/Soc；Four-Equation（Eq 19.37–41）+滥用动力学数据库 Copy；N-Equation 每反应 8 参数导入/导出文件格式照录；Fitting Tool/Standalone——Common Inputs rho*Cp/T0/Adiabatic? 六参、Standalone Time Step/Total Time+ARC 数据对比+四种图、Fitting Initial alpha/峰值温度/固定指数两选项、仅一方程且 GUI 单组数据；Run Thermal Abuse Model Only 仅解能量方程；动力学电池专属告诫+TUI 拟合双格式回填）。32.2.3.7 内外短路（外部 Specified Resistance；内部预定义 UDM Short Circuit Resistance——Patching Region Register 或 C_BATTERY_SHORT_R UDF；仅 MSMD）。32.2.3.8 肿胀算例（MSMD/Circuit Network+三子模型；Young's modulus 自动取三列均值；Battery Effects 自动选中；动网格 Smoothing+Linearly Elastic Solid+Intrinsic FSI 区）。32.2.4 参数估计工具（TUI 总入口 define/models/battery-model/parameter-estimation-tool 三选；NTGK TUI——通配符/逐温度/DOD 层正文默认 30 与示例 [20] 并照录；ECM TUI——4P/6P、JH/LM、容量必给、衰减需放电曲线组，会话示例照录；热滥用 TUI——Eq 32.1 打印、多组不同加热条件数据建议、输出 A/E/HW/m/n）。32.2.5 初始化（流场同初始化或 Init 仅电池；换子模型必须重初始化）。32.2.6 材料（cell/tab/busbar 电导率必定义；活跃区 defined-per-uds 分 σ+/σ−、被动区 constant）。32.2.7 求解控制（Potential Phi+/Phi- 可在 Equations 开关；Advanced Solution Controls）。32.2.8 预定义报告 battery-max-temperature/terminal-voltage/terminal-current（后两者限 Circuit Network 与 MSMD；不可导出复制）。32.2.9 后处理（UDS 电位场经 .cdat 导出至 CFD-Post；CHT/FMU-CHT 与 Circuit Network 变量组+Active/Passive Zone Connection 与 9 位 Battery Connection Index 编码规则；MSMD 全变量清单含 P2D 平均量与肿胀量；热滥用三模型变量；矢量图 current-density-jp/jn/j 与 layer-nornal-direction（原文拼写照录））。
- 扩充知识页 [[Fluent 电池模型]]（**Ch.32 全章完成**，pp. 3427–3536）。
- 提取边界：Theory Guide Eq 19.x 引用式与 Eq 32.1 公式体未提取按引用记录；Figures 32.38–32.44 与 Battery Connection Index 数位含义图为图形元素；p. 3536 空页。
- 下一续接位置：Part III / Ch.33 Modeling Fuel Cells，从 p. 3537 开始。

### 批次 96：Part III / Ch.33 第 1 段——33.1 PEMFC（PDF pp. 3537–3584），新十批任务（96–105）第 1 批

- 新十批连续任务（批次 96–105）第 1 批，48 页（3537–3584）：章引言（三 add-on 模块——PEMFC 新推荐模型、Fuel Cell and Electrolysis（Resolved Electrolyte，PEMFC 低/高温+SOFC+SOEC）、SOFC with Unresolved Electrolyte）。33.1 PEMFC 全节：33.1.1 概览（UDF+GUI、电位场/毛细压力/水含量/流道液饱和按 UDS、并行可用；限制——各向异性组分扩散率不兼容）；33.1.2 几何九区+集流体与冷却流道；33.1.3–33.1.4 安装加载（addons/pemfc、ribbon 或 addon-module 模块号 9、有效 case 前提）；33.1.5 工作流（3D 双精度、对话框不取代 BC 界面）；33.1.6 设置——Model 选项卡（Joule/Reaction Heating、Electrochemistry Sources、Butler-Volmer 默认否则 Tafel、Liquid Phase 默认开、Multicomponent Diffusion、Anisotropic E-cond in GDL/MPL（defined-per-uds 三选项、Electrical Conductivity 被忽略）、Effective P-Cond in MEA、Use Half-Cell Potentials（否则 V_Open）、Cathode Particle Model、Compute Liquid in Channels 默认关、Include Dynamic Head、Knudsen Diffusion、Temperature Dependent Jref 默认开、N2 Crossover 默认关、Ice Phase 仅瞬态默认关、W-Diff Wu/Wang；Electrical System 三法（BC 面板/总电压/总电流÷电解液投影面积）；URF 四项（Liquid-Vapor 等）；F-cycle for All Equations 最佳实践）；Parameters 选项卡（J_ref/C_ref/浓度指数/传递系数/Std.State E0/Entropy/V_Open/I_leak=泄漏密度×投影面积/标准态温压；Reference Diffusivity；Liquid Phase 组八参；Other——OSM_drag 默认 1.0、平衡水含量 a=1 与 s=1、N2 Crossover factor、冰相升降华速率）；Anode 选项卡五 Zone Type（集流体电导率仅常量、多孔电极八参+Leverett 三系数 1.417/2.12/1.263+各向同性渗透率限制、TPB 催化层加 S/V 比+质子传导五参+Jref 温度两参、MPL 减 Water Removal；电堆同类区整组选、Update Cell Zones）；Electrolyte 选项卡（膜仅固体区但允许溶解水/液水/离子电流；Equivalent Weight 等五参）；Cathode 选项卡（镜像；催化层加 Cathode Particle Model 三参 O2 溶解扩散积/颗粒半径/离子导体电阻）；Electrical Tabs；Advanced 选项卡（Contact Resistivity——仅 wall 与 porous-jump、逐面施加单侧设置、Use First Value for All；Coolant Channel——Enable Coolant Modeling 自动建 pem+cool-mixture 五组分；Stack Management——燃料电池单元 Create/Modify/Delete 保电气连通、Match Zone Name Pattern 通配；Degradation——独立退化模型、自动建 degradation-membrane、UDS-5 溶解相 OH 自由基限催化层与膜、两反应电位 0.695/1.76 V 与参考电流 0.01/1e-5 A/m²、PEMFC 跑完后 Calculate Initial Conditions→Calculate Degradation→Plot）；Customized UDFs（pemfc_user.c/pem_user.c/constit.c 三源文件、Create Customized Addon Library）；Reports 选项卡（Create Monitors 七个 .out 文件与 Monitor Frequency；Inlet Condition Calculator 十输入八输出——仅辅助换算、多入口须均分）；自动挂接 UDF 全表（Table 33.1 照录）与 DEFINE_SOURCE 不一致告警恢复法。33.1.7 边界条件（阴阳极/冷却入口 coolant 与 UDS-4 要求、压力出口回流、阳极端子必须锚零、阴极端子通量取负）；33.1.8 求解指南（恒电位从近开路电压起步/恒电流从低电流起步、F-cycle+BCGSTAB、前 5–10 迭代关 Joule 与反应热）；33.1.9 后处理（UDS 0–4 与 UDM 0–18 全表照录、list_pemfc_udf）；33.1.10 pemfc_user.c 用户函数清单（饱和压/水活度/电渗透/膜电导/水扩散/气体扩散/Leverett/毛细扩散/水含量/AV 比/传递系数/开路电压/泄漏电流/流道阻力/Set_UDS_Names/UDM_Names——单位不可改、旧 case 监视器 UDS 名检查）。
- 新建知识页 [[Fluent 燃料电池]]（Ch.33 段 1/3 完成，pp. 3537–3584）。
- 提取边界：Theory Guide Chapter 20 各式与 Eq 33.1–33.5 公式体未提取按引用记录；33.1.8 多重网格终止判据数值文本层缺失未照录；Figures 33.1–33.18 图形元素；Leakge_Current 原文拼写照录。
- 下一续接位置：Part III / Ch.33 33.2 Using the Fuel Cell and Electrolysis Model，从 p. 3585 开始。

### 批次 97：Part III / Ch.33 第 2 段——33.2 Fuel Cell and Electrolysis（PDF pp. 3585–3617），新十批任务（96–105）第 2 批

- 新十批连续任务（批次 96–105）第 2 批，33 页（3585–3617；p. 3585 顶部为 33.1.10 pemfc_user.c 函数清单收尾四函数，已并入知识页 33.1.10）：33.2 Fuel Cell and Electrolysis（Resolved Electrolyte）全节：33.2.1 概览（UDS 电位/液饱和/水含量；限制同 PEMFC——各向异性组分扩散率不兼容）；33.2.2 几何七区（无微孔层）；33.2.3–33.2.5 安装加载（addons/fuelcells、模块号 3）与工作流（无 3D 双精度强制）；33.2.6 设置——Model 选项卡（PEMFC/SOFC/SOEC 三选；选项几乎全默认开——High Temperature PEM、Joule/Reaction Heating、Electrochemistry Sources（全关须连 Membrane Water Transport 与 Multiphase）、Butler-Volmer 默认否则 Tafel Eq 20.72、Membrane Water Transport 仅低温、Multiphase 仅低温、Multicomponent Diffusion、Anisotropic E-cond（同三选项）、Knudsen；URF Saturation Source 与 Water Content；Enable Smooth Partition（Metis+Laplace）与 F-cycle）；Parameters 选项卡（Ref. Current/Concentration/Exponent/Exchange 系数/Open-Circuit Voltage Eq 20.74/Leakage Current（Leakge_Current() UDF）；Reference Diffusivities、Pore Blockage 两项、相对渗透率指数；**符号约定——负电压接阳极（与电解惯例相反）**）；Anode/Cathode 选项卡四 Zone Type（多孔电极给 Porosity+Viscous Resistance+Contact Angle+Pore Size；TPB 催化层加 S/V 比）；Electrolyte 选项卡（低温专属三参；**膜可流体或固体区**）；Advanced（接触电阻同法；冷却流道直接给四物性+Enable Coolant Channel(s)；电堆管理+Suggest Stack Setup 自动识别——五处区信息前提、须自行核验）；Customized UDFs（pem_user.c）；Reports（Electrolyte Projected Area 与 External Contact Interface(s)、恒电位=差值恒电流=解的一部分）。33.2.7 集流体建模（固体/流体/多孔均可；固体区须激活 UDS-0 且 **UDS Diffusivity 必须 user-defined (cond::fuelcells) 勿用 defined-per-uds**——与 PEMFC 相反）；33.2.8 边界条件（同 PEMFC 但入口置零 UDS-2 Water Saturation、阴极通量取负）；33.2.9 求解指南（同 33.1.8）；33.2.10 后处理（UDS 0–3 与 UDM 0–14 全表照录、UDM 不直接后处理、.cdat 导出 CFD-Post）；33.2.11 pem_user.c 用户函数清单（15 函数含 SOFC 专属 Electrolyte_Conductivity Eq 20.93、Saturation_Diffusivity Eq 20.86）。
- 扩充知识页 [[Fluent 燃料电池]]（Ch.33 段 2/3 完成，pp. 3585–3617；并补 33.1.10 尾部四函数）。
- 提取边界：Theory Guide Eq 20.69–20.107 公式体未提取按引用记录；Figures 33.19–33.36 图形元素；Leakge_Current 原文拼写照录。
- 下一续接位置：Part III / Ch.33 33.3 Using the Solid Oxide Fuel Cell With Unresolved Electrolyte Model，从 p. 3618 开始。

### 批次 98：Part III / Ch.33 第 3 段——33.3 SOFC With Unresolved Electrolyte（PDF pp. 3618–3634），新十批任务（96–105）第 3 批

- 新十批连续任务（批次 96–105）第 3 批，17 页（3618–3634，p. 3634 空页；p. 3618 顶部为 33.2.11 pem_user.c 尾函数——传递电流函数含 dRade/dRcde 偏导与 Thermal_ctk_pemfc，已并入知识页），**Ch.33 全章完成**：33.3 SOFC with Unresolved Electrolyte 全节：33.3.1–33.3.3 限制（各向异性组分扩散率不兼容）/安装（addons/sofc）/加载（模块号 4、树项 SOFC (Unresolved Electrolyte)、Enable SOFC Model）；33.3.4 设置流程（3D 双精度；启用自动配置——压力基稳态 Absolute 公式、能量方程、层流、组分输运四设置（Inlet Diffusion 关/全多组分/热扩散开）、F-cycle、Metis+Laplace；自动建混合物（diffusivity::sofc 与 E_Conductivity::sofc UDF）与四种固体材料；支持电解质 shell conduction 但**不支持横向导电**；H2/CO 需 CO/CO2 组分；残差判据 1e-08；UDM 0–13 全表（UDM-0 守恒界面电流密度面积分=总电流、UDM-4–6 单元中心非守恒可能与 UDM-0 不符、UDM-7/8 线性化量无物理意义、UDM-10/11 分列活化极化）与 UDS-0）；33.3.5 五选项卡——Model Parameters（Electrolyte Conductivity Submodel 仅 1073–1373 K Eq 33.6、Volumetric Energy Source 先关后手动开、Surface Energy Source 必须常开、Knudsen 扩散 Kn>>10、Species Sources 必须常开、Electrolysis Mode（负电流/电压须大于开路电压）、Disable CO Electrochemistry 互斥；Current URF 0.3/0.2；Total System Current/Converge to Voltage/逐边界电气条件/Leakage Current Density（constit.c 温度实现）；F-Cycle 默认）；Electrochemistry（交换电流密度阳极 1e10/阴极 100 A、摩尔分数参考 1、浓度指数 0.5、对称因子 0.5 与同步改浓度指数建议、Temperature Dependent I_0 系数 A/B）；Electrolyte and Porous Zones（阴阳极电解液界面区、迂曲度典型 2–4、Knudsen 孔径）；Electric Field（导电区+电导率、接触面+电阻、Voltage/Current Tap Surface）；Customized UDFs（constit.c）；33.3.6 constit.c 八函数（Nernst/Activation/Resistivity/Leakage_Current_Density/Solve_Butler_Volmer_NR/CONDUCTIVITY_CELL 组 ID 1–5/CONTACT_RESIST_FACE 组 ID 1–3/h2_co_split_func Eq 20.141）。
- 扩充知识页 [[Fluent 燃料电池]]（**Ch.33 全章完成**，pp. 3537–3634；并补 33.2.11 尾部函数）。
- 提取边界：Theory Guide Eq 20.108–20.141 与 Eq 33.6/33.7 公式体未提取按引用记录；Figures 33.37–33.42 图形元素；UDM-2 原文拼写 Overpotentail 照录；p. 3634 空页。
- 下一续接位置：Part III / Ch.34 Modeling Magnetohydrodynamics，从 p. 3635 开始。

### 批次 99：Part III / Ch.34 Magnetohydrodynamics 全章（PDF pp. 3635–3658），新十批任务（96–105）第 4 批

- 新十批连续任务（批次 96–105）第 4 批，24 页（3635–3658），**Ch.34 全章完成**：34.1 引言（DC/AC 电磁场与导电流体；外磁场内置函数或导入数据；兼容 DPM/VOF/Eulerian 含离散相电导率影响）；34.2 实现（感应方程 Eq 21.14/21.16 与电位方程 Eq 21.22 走 UDS——2D 2 个/3D 3 个感应分量标量+1 个电位标量；mhd_flux/mhd_magnetic_diffusivity/mhd_mag_source/mhd_phi_source/mhd_unsteady_source 五 UDF；可在固体区解、多相只在混合物域；壁面 BC 三类外边界——绝缘/导电/薄壁（法向一维扩散+材料厚度）与内边界耦合；UDM 存 MHD 变量、mhd_adjust 每迭代更新；动量 Lorentz 力/能量 Joule 热源；DPM 的 DEFINE_DPM_BODY_FORCE/SOURCE）；34.3 使用（addons/mhd、模块号 1、加载自动完成全套基础设置、**case 保存绝对路径——挪位置即加载失败、UDF Library Manager 卸载重载**；两方法 UDS 表——B_x/B_y/B_z Tesla 或 Phi Volt；外磁场 Patch（DC/AC、频率/波长/传播方向/相位偏移、Moving Field 正弦或方波）或 Import（第三方 MAGNA、B0 Data Media Non-Conducting/Conducting=Case 1/2、DC+AC 双段叠加导入、Apply External Field 到 zone/register、Reset 清零）；**BC 必须在 MHD 对话框设——不支持自定义 BC**；cell zone 材料电导率五法+磁导率仅常数；壁面四类绝缘/导电/耦合/薄壁（仅感应法）；电位法导电壁给 Voltage 或 Current Density；Solution Control——Initialize MHD/DPM、Solve MHD Equation、Include Lorentz Force/Joule Heating、URF、B0 Scale Factor；求解——从已收敛流场起步感应方程 URF 0.8–0.9、电位方程 URF 勿设 1、动量能量 URF 调小、缩放因子渐进重启；后处理五矢量 Induced/External-Field、Current-Density、Electric-Field、Lorentz-Force；限制四条——低磁雷诺数假设、仅常数各向同性电磁物性、必须直接给磁场不支持电流指定、AC 低频显式解析无时间平均）；34.4 指南（目录结构 lib/addon.bin+架构子目录；十步概览）；34.5 磁场定义（正弦 Eq 34.1 平均+幅值+传播矢量/频率/波长/相位偏移、非移动场传播矢量为零；方波 Eq 34.2）；34.6 外磁场数据格式（文本七段结构——ID 标签/三方向点数/三行范围均匀分布/AC 旗标行 nAC 与频率/数据行实虚部升序 N=nx·ny·nz；DC+AC 复合场两段重复顺序无关；快照解释+复数形式）。
- 新建知识页 [[Fluent 磁流体动力学（MHD）]]（**Ch.34 全章完成**，pp. 3635–3658）。
- 提取边界：Theory Guide Eq 21.x 与 Eq 34.1–34.4 公式体未提取按引用记录；Figures 34.1–34.11 图形元素；感应方程 URF 区间符号文本层缺失按指南节补全。
- 下一续接位置：Part III / Ch.35 Modeling Continuous Fibers，从 p. 3659 开始。

### 批次 100：Part III / Ch.35 Continuous Fibers 全章（PDF pp. 3659–3698），新十批任务（96–105）第 5 批

- 新十批连续任务（批次 96–105）第 5 批，40 页（3659–3698，p. 3698 空页），**Ch.35 全章完成**：35.1–35.2 安装加载（addons/fiber、模块号 2；TUI 两问——预置 UDF 挂钩 yes 全流体区/no 逐区且旧 case 必答 no、质量交换挂钩干纺答 yes；UDF 清单 fm_adjust/fm_src_*；**不初始化流场 UDM 分配不正确——收敛 case 须重载 data**；case 绝对路径保存告诫）；35.3 起步（UDM 增至 8、挂 fm_adjust::fiber；逐区源项 Table 35.1——fm_src_mass/x_mom/y_mom/z_mom/enthalpy/dom；辐射交互自动挂 fm_src_dom 且须先初始化）；35.4 模型与选项（Melt Spun/Dry Spun 二选；Interaction with Fluent、Include Lateral Drag（Eq 22.30、不考虑侧弯）、Fiber Radiation Interaction（P-1/DO+Emissivity）、Fiber Viscous Heating；Exchange 相关式——拖曳 const-drag/kase-matsuo/gampert/UDF、换热 const-htc(SI W/m²K)/kase-matsuo-1/2/gampert/UDF、传质 const-mtc(**输速率 kg/m²s**)/同名/UDF）；35.5 材料属性（单纤维材料限制；fluid 类型作聚合物/溶剂、可 UDF 化五属性；属性清单——Blending Interval、Cp/Density/导热干纺质量平均、Emissivity、Flory Huggins（干纺 Eq 22.3）、Latent Heat+参考汽化温度（干纺）、Solidification Temperature（熔纺）、Antoine 蒸气压（干纺、结果须 Pa、范围外取端点）、零剪切粘度熔纺固/液双设与干纺 Eq 22.37——粘度随速度梯度可致失稳告诫）；35.6 定义纤维（主要输入八项；注入四类型 single/line/matrix(3D)/file（7 列格式照录）；Injections 对话框十二操作（Initialize/Compute/Print/Read/Write/Binary/List 列名照录）；Set Injection Properties——组内纤维数（400 孔 5 组=80 例）、单孔流量、卷取点唯一须拆分、prescribed-velocity 或 tensile-force(0=自由下落)；纤维网格四种 equidistant/one-sided/two-sided/three-sided（细化点位置无量纲 0–1、Compute 估算））；35.7 UDF（fiber_fluent_interface.c 模板、拷贝 addons/fiber 勿链接、八个不可改名函数、Kase/Matsuo 1967 换热示例照录、fiber.h/fib-mem.h 勿改头文件、Linux make Makefile-client/Windows build_fiber_udf.bat+FLUENT_INC+FLUENT_ADDONS、挂接 Enable UDF Properties）；35.8 求解控制（三方程开关、离散三格式、URF、判据与 Check Convergence、Relative Residuals Eq 22.20、Iterations、Reporting Interval 0 只输出末次推荐、Fluent 迭代间隔、源项 URF 不影响收敛解）；35.9 后处理（fiber-location 等值线/等值面、Fiber Mesh Display 与 Fiber Display（Nodes/Edges/单纤维/着色 ID-Density-Tension）、七个交换项 Custom Field Functions 仅耦合时更新、print-xy 二十三个 x/y 变量、并行 host 进程瓶颈告诫）。
- 新建知识页 [[Fluent 连续纤维模型]]（**Ch.35 全章完成**，pp. 3659–3698）。
- 提取边界：Theory Guide Eq 22.x 公式体未提取按引用记录；Figures 35.1–35.17 图形元素；UDF 示例代码照录（排版符号有损处按语义记录）；p. 3698 空页。
- 下一续接位置：Part III / Ch.36 Creating Reduced Order Models (ROMs)，从 p. 3699 开始。

### 批次 101：Part III / Ch.36 ROMs 全章（PDF pp. 3699–3708），新十批任务（96–105）第 6 批

- 新十批连续任务（批次 96–105）第 6 批，10 页（3699–3708），**Ch.36 全章完成**：36.1 定义 ROM（ROM Production/Consumption 两段——FMU 2.0 或 ROMZ 导出；**2026 R1 仅稳态、牛顿流体、无激波 Ma<1、无辐射**；add-on 模块 **define/models/addon-module/11**；输入参数数量指引 Low 1–2/Medium 3–6/High >7/Very high >15；至少一个输出参数（custom field function→报告定义→Create Output Parameter）；Reduced Order Model 对话框选 Variables+Zones——选太多文件大、**必须选与输入/输出参数对应的变量**）；36.2 Fluent 内求值（Workbench 流程 ROM Builder Export ROM→romz、Fluent Setup cell Import ROM、Evaluate 选项卡范围输入、后处理关 Node Values 用 ROM Cell Functions——须先点 Evaluate；四条 Fluent 内后处理限制）；36.3 导出（Write Profile 对话框选 ROM cell functions 与面）；36.4 限制（界面区不可用、无几何参数更新、仅稳态、禁燃烧与辐射、禁参数化优化、禁动变形网格、Expression/User-Defined 报告定义不可用、Vertex/Mass-Weighted 类报告不建议改 Facet/Area-Weighted 类、四类报告定义不支持输出参数）。
- 新建知识页 [[Fluent 降阶模型（ROM）]]（**Ch.36 全章完成**，pp. 3699–3708）。
- 提取边界：DesignXplorer 侧行为未摄取（指向其 User's Guide）；Figures 36.1–36.2 图形元素。
- 下一续接位置：Part III / Ch.37 Using the Solver，从 p. 3709 开始。

### 批次 102：Part III / Ch.37 第 1 段——37.1–37.5（PDF pp. 3709–3758），新十批任务（96–105）第 7 批

- 新十批连续任务（批次 96–105）第 7 批，50 页（3709–3758），Ch.37 段 1/4：37.1 总览（压力基/密度基两求解器与隐式显式、segregated/coupled 两算法特性；模型可用性清单——压力基专属 15 项、密度基专属 Wet Steam；11 步通用流程）；37.2 空间离散（梯度三选；默认离散——单相二阶/湍流量一阶、多相一阶；一阶 vs 二阶与混合因子 solve/set/numerics 0–1；QUICK 限 quad/hex、三阶 MUSCL、BCD/CD 限 LES 系且 Peclet<1、modified HRIC；压力插值六格式选型——PRESTO!/BFW/MBFW 各适用与 boundary-presto-treatment；密度插值四格式与激波 QUICK 建议；HOTR——Standard/Convection Only、Flow Variables Only/All Variables、默认 0.25 稳态 0.75 瞬态、三限制；逐方程下拉与 VOF 体积分数五格式、组分统一设置、阶梯棱柱勿 node-based+MUSCL）；37.3 压力基设置（P-V 耦合 SIMPLE/SIMPLEC/PISO/FSM/Coupled 全选型——SIMPLEC 压力修正 URF 1.0 与斜网格 0.7、PISO neighbor 瞬态推荐 URF 1.0 与 skewness-only 和为 1、FSM 仅 NITA、Coupled 禁 NITA 且 porous jump 告诫；Local Time Step Courant 5/Coupled Flow CFL 200+显式松弛 0.5、瞬态 1e7+1.0、<10 不建议；增强斜率修正 TUI；Flux Type——Rhie-Chow momentum/distance based 与 Auto Select 四条件组合、多相固定 momentum based；URF 全则——0.2/0.5/0.5/0.5 失稳组合、标量 0.8、coupled 算法提标量 URF；NITA 全套——设置步骤、Accelerated Time Marching 三改二限、显式松弛分层建议、Expert 三参数（Max Corrections/Correction Tolerance/Residual Tolerance 与 CFL 关系）、Hybrid NITA Aggressive 2/Conservative 3 外迭代、Instability Detector CFL 25/速度 1000、四条高级 TUI、策略清单、兼容三清单、PRESTO!+NITA 告诫；方程顺序 optimized-for-volumetric-expansion；动量修正形式默认开未来移除关闭命令）；37.4 密度基设置（CFL 显式默认 1 不超 2/起步 0.1–0.5、隐式默认 5 可至 100+、AMG 自降 CFL 五次重试、CFL 报告定义自动建；通量 Roe-FDS/AUSM/Low Diffusion Roe-FDS（仅 SRS+隐式+亚音速）与 Roe-FDS+BCD 组合建议；CASM——隐式稳态拉伸网格、乘子截断 100、典型 CFL 5–10、显式松弛 0.5、与 pseudo time 互斥、低 y+ 优势、增强 CASM（no→yes、0.75）；High-Speed Numerics；Divergence Prevention（冻结压力温度+其他 0.1）；显式松弛 TUI；FAS 多重网格（仅显式、4–5 层、禁显式时间步进、残差光顺 0.5×2 道 CFL 翻倍）；轴稳定化 TUI）；37.5 AMG 参数（默认循环分配——压力修正 V/能量 F/流动修正 F 或 V/其余 flexible；Restriction/Termination 判据语义；稳定化方法 BCGSTAB/RPM/GMRES/CG 选型与回退提示；Fixed Cycle 前后松弛默认与各向异性导热告诫、并行能量 Fixed F-cycle；Coarsen by 与 smoother 组合表 ILU 3/8 GS 1/2、Max Coarse Levels 0=关 AMG；三粗化选项；Gauss-Seidel vs ILU；Verbosity 1–2 输出样例；FAS industrial-strength 策略四条与风险）。
- 新建知识页 [[Fluent 求解器使用]]（Ch.37 段 1/4 完成，pp. 3709–3758）。
- 提取边界：Theory Guide Eq 23.x/37.1 公式体未提取按引用记录；个别符号占位按语义记录；"MDM"原文如此照录；Figures 37.1–37.12 图形元素。
- 下一续接位置：Part III / Ch.37 37.6 Setting Solution Limits，从 p. 3759 开始。

### 批次 103：Part III / Ch.37 第 2 段——37.6–37.13（PDF pp. 3759–3811），新十批任务（96–105）第 8 批

- 新十批连续任务（批次 96–105）第 8 批，53 页（3759–3811），Ch.37 段 2/4：37.6 解限值（压力/温度/湍流量限值语义与最小体积分数；绝对压力限仅 ideal/real-gas；Positivity Rate Limit 默认 0.2、高速流能量发散降 0.05/0.02、High-Speed Numerics 时也作用于压力；37.6.1 各限值字段与 Eulerian/VOF/Mixture 适用差异；Default/Reset）；37.7 多级时间步进（稳态 3 级 0.2075/0.5915/1.0、瞬态 4 级 0.25/0.3333/0.5/1.0、系数 (0,1) 末级必须 1、Dissipation/Viscous 逐级勾选——粘性首级必算、稳态与层级无关）；37.8 梯度限制器（Standard/Multidimensional/Differentiable；三方向 Cell to Face 默认/Cell to Cell/Cell to Node（拉伸斜高长宽比优、overset 与 multidimensional 不可用）；Limiter Filter——噪声抑制保间断、改善表观收敛、multidimensional 不可用）；37.9 初始化（超音速风洞类比；UDRGM/UDF 密度/解相关表达式的先无区标准初始化要求；标准初始化三来源与 relative 默认；Patch——表达式/场函数/shell 区只温度/不影响计数/Workbench 需 /solve/patch 命令、register 用法、中途可 patch；profile 内存冲洗 TUI 默认关）；37.10 FMG 初始化（TUI 参数——层级默认 5 小算例 3–4、逐层残差 0.001 与循环 100–800、Courant 0.75、verbose；湍流先合理标准初始化；密度基粘性 FMG——viscous-terms?、湍流粘度比默认 100）；37.11 Hybrid 初始化（单相稳态默认；More Settings 三选项卡——迭代 10/URF 1/参考框/三个 Initialization Options（进口初压/外流气动/常速模）、湍流域平均或局部、组分零值或指定；多孔介质推荐标准初始化、Hybrid 仅限常速模）；37.12 稳态计算（Run Calculation、Global Time Step 先设 pseudo 参数、Reporting Interval 兼收敛检查频率但不作用于报告定义、Stop/Ctrl+C、UDF Profile Update Interval、重置、稳态数据采样两法与矢量模量统计差异、-dataset 后缀、壳面不采集）；37.13 瞬态计算（应用与瞬态化稳态技巧；隐式 Fixed——User-Specified/Period-Based/Frequency-Based（in-cylinder 仅 User-Specified）与 Δt 选择准则（理想每步 5–10 迭代、周期每周期 20 步、Courant 数 20–40 验证）；Adaptive 三法+CFL-Based（仅隐式、禁多相/动网格/声学/结构、Courant 近 1、变化因子默认 0.5/2、高级四 CFL type——Convective/Convective-Diffusive/Acoustic/Flow）+Error-Based（预测-校正截断误差、5 次尝试、容差默认 0.01、Euler-Euler 禁）+Multiphase-Specific（湿蒸汽外全部多相、Global CFL 默认 2 与显式/隐式建议 2–20、八时间尺度与 Physics/Moving Mesh 约束 VOF 专属、变化因子默认 0.8/1.2、Effective Global CFL 打印）；Duration 四法 Total/Incremental；Adaptive 前先固定步、自动自适应联动差异、DEFINE_DELTAT、Extrapolate Variables（NITA/显式禁、不可压关压力外推）；显式瞬态 Specified Time Step 或 Courant 数 Eq 37.2、rk2 快速瞬态 TUI；时间统计采样与 DPM 采样特性、运行时 DFT（目的二条、Inverse DFT beta、数据集组织、限制清单起于 p. 3811 末续下段））。
- 扩充知识页 [[Fluent 求解器使用]]（Ch.37 段 2/4 完成，pp. 3759–3811）。
- 提取边界：Theory Guide Eq 37.2–37.23 公式体未提取按引用记录；Figures 37.13–37.29 图形元素；运行时 DFT 限制清单跨段（p. 3811→3812），批次 104 补记。
- 下一续接位置：Part III / Ch.37 37.14 Performing Calculations with a Pseudo Time Method，从 p. 3812 开始。

### 批次 104：Part III / Ch.37 第 3 段——37.14–37.19（PDF pp. 3812–3854），新十批任务（96–105）第 9 批

- 新十批连续任务（批次 96–105）第 9 批，43 页（3812–3854），Ch.37 段 3/4：37.14 伪时间方法（适用范围与两法——Local Time Step（压力基 segregated；禁结构/多相/G Equation/缝隙/NITA、组分+关能量不支持；Pseudo Time Courant Number）、Global Time Step（coupled/密度隐式稳态；单相无电池燃料电池熔凝默认）；Global 三设置——Pseudo Time Explicit Relaxation Factors 逐方程、Expert 选项卡两手段（Time Scale Factor 或关闭改标准稳态+URF；燃烧方程需手动启用、UDS 默认全关、多相体积分数限 segregated）、Run Calculation 的 Fluid/Solid Time Scale——User-Specified 或 Automatic+Time Scale Factor（3–10 常加速、0.3/0.1 降）与 Length Scale Method 三选（Conservative 体积立方根/Aggressive 最大延展/User-Specified）、Verbosity 0–2、固体时间尺度组出现条件）；37.15 远程资源（Manage Remote Resources 对话框增删改集群、本地缓存跨会话、认证、参数化并发默认集群语义、Remote Compute 对话框提交、Jobs on Remote Cluster 监视默认 1 分钟刷新）；37.16 Ansys Cloud Burst Compute（前提四项、Web Browser/In-session 认证、账户选择对话框余额查看、提交流程与余额报错重试、Linux 会话内认证无害报错；Job Details 全字段——Project/Job Name、Precision、CPU、MPI、Queue 自动匹配、EFA Interconnect、GPU 求解器/Web Server/Advanced（每节点 CPU、最大执行时长、Exclusive）；Case Details 两种上传与 data 询问；Journal Default/Custom+报告导出 HTML/PDF/PPT；Output Files 全留或指定；View Jobs 对话框动作九项（含 beta 远程后处理）、过滤与 Auto/Manual 刷新；云端 portal 查看）；37.17 收敛监视（单精度 6/双精度 12 量级极限；压力基残差定义——unscaled/global/local 三式、连续方程增强局部式与 TUI、全局连续分母前 5 迭代最大值、归一化 N=5 与 Renormalize；密度基 RMS 残差与两缩放式；Residual Monitors 对话框——存储 1000 隔点丢弃、默认判据能量/DO/P-1 1e-06 其余 1e-03、局部缩放判据改 1e-05/1e-04、判据四型 absolute/relative/relative or absolute/none（relative 仅非稳态、NITA 无判据）、Plot 参数 Iterations to Plot 为存储点、残差场后处理 retain-cell-residuals 且 DO 辐射无、unscaled 值）；37.17.2 统计监视五量（flow-time/delta-time 可同图）；37.17.3 解量监视与运行平均；37.18 收敛条件（Check For 两选、All/Any Condition、默认与残差 AND、Ignore Before/Use Steps/Stop Criterion 公式 Res-m(k) 最大值比较、Print 只对前一步）；37.19 执行命令（Execute Repeatedly Every+When 五选项、Reporting Interval 保持 1 告诫、Execute Once、专用对话框优先告诫）。
- 扩充知识页 [[Fluent 求解器使用]]（Ch.37 段 3/4 完成，pp. 3812–3854；并补 37.13.6 运行时 DFT 输入参数与后处理变量尾段）。
- 提取边界：Theory Guide Eq 37.25–37.37 公式体未提取按引用记录；Figures 37.30–37.52 图形元素。
- 下一续接位置：Part III / Ch.37 37.20 Automatic Initialization of the Solution and Case Modification，从 p. 3855 开始。

### 批次 105：Part III / Ch.37 第 4 段收官——37.20–37.24（PDF pp. 3855–3904），新十批任务（96–105）第 10 批

- 新十批连续任务（批次 96–105）第 10 批，50 页（3855–3904，p. 3904 空页），**Ch.37 全章完成**：37.20 自动初始化与 case 修改（Automatically Initialize and Modify Case；Case Modification Manager——Pre-Initialization/Original Settings/New、Auto Initialization Method 三选（case 值不执行 Hybrid/文件数据/既有解数据重置计数）、命令需含应答、.tsv 导入导出、Original Settings 先于首步应用、启用时 Run Calculation 忽略、迭代清零规则）；37.21 动画（Animation Definition 十步——Raytracer、帧频三基、Storage Type 六选与 HSF/PPM/In Memory 特性、相对路径默认、Animation Object 十类（Volumes 需 Raytracer）、创建指南四条；回放全操作（速度/片段/注解 HSF/快进/循环模式/逐帧/删除规则）；保存三式——.cxa+.hmf/.hsf/.ppm、Picture Files（AVZ/VRML 不支持）、Video File 五格式（MPEG Ubuntu 不支持、学术许可无 Video Options）与 FPS/分辨率/质量/H.264；读取免 case）；37.22 case 检查（Check Case 五选项卡自动/手动实施；Mesh 四条——质量 0.01、动网格先 zone 后 mesh motion 预览、轴对称负 y 平移；Models 七条——Realizable k-ε、DO 耦合光学厚度、S2S 边界温度、混合平面 URF 1、动网格 smoothing、NOx 湍流交互、空化模型换型；Boundaries 十三条——axis 边界、outflow 五不兼容、操作压力、正压边界、湍流默认值、shell 厚度、VOF 0/1、Moving Wall、非零速度、进口默认值、换热器多孔区；Materials 四条——Cp 多项式、Boussinesq 两参数、吸收系数；Solver 四条——Transient、LSQ 梯度、能量 URF 0.90、VOF PRESTO!）；37.23 收敛与稳定性（37.23.1 判断收敛——无普适标准、默认判据局限三条、局部缩放更普适、三量级下降三例外与初值差告诫、积分量为准；37.23.2 分步求解——Equations 开关、能量仅压力基可关、反应开关与 patch 高温；37.23.5 Poor Mesh Numerics——三档 0/1/2 阶默认 1、只应小比例、五判据命令（默认/quality/gradient/solution+quality/register-based 全参数与 pmn_pdf_stability_marker）、print-count/reset/turbulence-production-term（k-ω 族与 Transition SST）；37.23.6 WFGC——适用网格、fast/memory 两模式（+22% 内存）、左旋面除外；37.23.7 能量噪声滤波器——默认关、疑难从头启用）；37.24 Solution Steering（密度基隐式稳态专属；FMG+两阶段策略、五 Flow Type 马赫区间、启用四条件、Flow Type/blending 100% 可降、Courant Initial/Maximum 与 Linear Ramp-up、Update Interval、FMG Settings 选项卡）。
- 扩充知识页 [[Fluent 求解器使用]]（**Ch.37 全章完成**，pp. 3709–3904）。
- 提取边界：Theory Guide 引用式公式体未提取；Figures 37.53–37.78 图形元素；37.23.1 默认判据两处符号占位按 37.17 默认值补全；p. 3904 空页。
- 下一续接位置：Part III / Ch.38 Using the Fluent Native GPU Solver，从 p. 3905 开始。

### 批次 106：Part III / Ch.38 第 1 段——38.1–38.9 前半（PDF pp. 3905–3940），新十批任务（106–115）第 1 批

- 新十批连续任务（批次 106–115）第 1 批，36 页（3905–3940），Ch.38 段 1/2：38.1 引言（原生 GPU 求解器、最高 5 倍 CPU 速度）；38.2 支持平台（NVIDIA CUDA 12.8+/驱动 570+/Pascal 起；AMD ROCm 6.0+）；38.3 基本八步（遵守支持特性与限制）；38.4 启动（Launcher——仅 CFD Enterprise/HPC Ultimate 两许可级、Native GPU Solver、GPU ID 勾选每 GPU 一额外 CPU 进程、AMD 仅命令行；命令行 fluent 3d/-3ddp/-gpu_hybrid_precision -t<n> -gpu——<n> 三种语义、-scheduler 与 -scheduler_gpn 多节点、-gpu=ID 手选；38.4.3 CPU/GPU Remapping——默认一对一、-gpu_remap 多对多（减跨机传输）、DPM/声学回退一对一、与 -gpu_async 同用限制；38.4.4 -gpu_async 异步输出——监视/动画/自动存盘/自动导出提速、负载比 1 最大、Cortex 收敛追平机制、仅 Intel MPI）；38.5–38.8 退出/GUI（隐藏不支持特性）/CPU 进程用于设置后处理（读入后分区、计算时并为每 GPU 一分区）/读入 CPU case（自动转换或禁用并列打印、残留不支持项阻止启动）；38.9 支持特性——一般要求（NVIDIA、单/双精度、仅 3D、五种单元+悬挂节点）；38.9.1 模型（CHT 各向异性但禁 Loosely Coupled；DO 可配非绝热 FGM；S2S；Shell Conduction 三限制；组分输运两 TCI 两求解器；FGM；可压；湍流——Laminar/k-ε 两型/GEKO WDF+k-ω SST/LES（Smagorinsky-Lilly、WALE、WMLES、二格量）/SBES 限 k-ω 族/代数转捩/曲率修正/黏性功；FW-H 声学；海绵层仅单个；叶轮机械整轮多排 TRS/FR/周期扇区含 instancing；38.9.1.1 电势模型（仅固体区）；38.9.1.2 电池模型（CHT Coupling/被动区 Joule/ROM 工具包/热滥用四型）；38.9.1.3 DPM（仅瞬态追踪、CPU 生成包上传 GPU、单向/双向耦合与源类型、五注入类型（file 仅稳态）、三颗粒类型、两种直径分布、spherical 拖曳、SSD 破碎四默认参数、DRW 固定 1/0.15、蒸发沸腾六条件、GPU 专属两选项、无 DPM Laws、film-averaged 扩散 1/3 规则））；38.9.2 材料属性七类清单；38.9.3 求解器设置（压力基绝对速度；Coupled 仅稳态配 CFL/pseudo transient、SIMPLE/SIMPLEC；Flux Type 两 RC；梯度 LSQ；一/二阶；压力 Linear/BFW；LES/SBES 的 BCD 与 Low Diffusion Central；Bounded Second Order Implicit+Use limiter in time；瞬态 CHT 固体步长；poor mesh removal/numerics TUI；稳态统计采样；coupled-pseudo-transient 提示可忽略；38.9.3.1 Optimized LES Numerics——每步两迭代、减步优于加迭代、URF 0.95/1.0、低扩散中心算子 Eq 38.1 非 TVD 禁激波、Linear 压力（与 CPU 不同）、distance-based 通量）；38.9.4 DPM 求解器设置（仅 High-Res、重心插值、三固定时间格式、Step Length Factor、禁 Accuracy Control、Linearize Source Terms）；38.9.5 参数化顺序更新；38.9.6 单元区与边界条件（进口/出口/远场/对称/壁面（含 Zero Specified Shear）/周期/非一致界面/porous jump/internal fan/单海绵层；三边界不可压可压通用；流体区七设置；38.9.6.1 Profiles and Expressions——steady/transient(beta) profile、parametric/static/dynamic 表达式三型、表外模型不支持、Table 38.1–38.4 摘要（Table 38.4 跨段续下批））。
- 新建知识页 [[Fluent GPU 求解器]]（Ch.38 段 1/2 完成，pp. 3905–3940）。
- 提取边界：Eq 38.1 公式体未提取按语义记录；Table 38.1–38.4 摘要照录（38.4 跨段）；Figures 38.1–38.2 图形元素；nvidia-smi 输出照录；"combusion"原文拼写照录。
- 下一续接位置：Part III / Ch.38 Table 38.4 续（Momentum - Boundary Conditions），从 p. 3941 开始。

### 批次 107：Part III / Ch.38 第 2 段收官——Table 38.4 续–38.14（PDF pp. 3941–3974），新十批任务（106–115）第 2 批

- 新十批连续任务（批次 106–115）第 2 批，34 页（3941–3974），**Ch.38 全章完成**：Table 38.4 续（进出口 Fan/Vent 各字段、Wall Moving Wall 三分量时变表达式、三条混用注意）；Table 38.5–38.13 摘要（能量单元区/边界、黏性模型 N/A 与湍流量字段、组分/电势/VOF 边界同 pattern）；38.9.6.2 DPM 边界（reflect/escape/trap、非重叠区壁面仅 reflect）；38.9.7 监视器与报告定义（三类自定义面不可建、不支持变量运行时 0 值、Force/Flux/Surface/Volume/Expression 五类全清单、内部区仅质量流量正确、支持的场变量十一类别、DPM 后处理四特性与 CPU pathlines、表达式支持域全清单与 Table 38.14 运算函数、Table 38.15 四科学常数、表达式报告定义引用的既有定义类型限制）；38.9.8 EnSight DVS 导出（节点/自定义面不可、单一导出定义、变量名差异、GUI 与 TUI 流程照录、自动导出前建全报告定义告诫）；38.9.9 Arm 部署（双包安装序、推荐 RHEL/Rocky）；38.10 限制清单（TUI 可设不支持项、DO 四限、壁面 Prandtl、Workbench 不可用、report-interval 20 建议、圆柱 profile 不支持、监视器先于初始化、非一致界面符号、静壁动压输出参数、稳态转瞬态热限制、混合初始化远场告诫、零剪切壁、封闭域压力偏移、二阶重启一阶步、GPU 转 CPU 重启限制、流动关闭残差不更新、Linear 压力差异、CHT 固体伪时间无穷、默认非 coupled pseudo-transient、组分 20 上限、表达式显式/区域限制/有限单位集照录、compressible-liquid 混合物禁组分、FGM 禁多孔与 frame motion；38.10.1 DPM 五限——仅静止网格、TUI 启用不支持项可崩溃丢数据）；38.11 稳态转瞬态四步；38.12 疑难排除五步（AMG BCGSTAB、SIMPLE URF 0.2/0.4/0.4、降一阶、mesh improve-quality）；38.13 性能排查（单 GPU 三查、多 GPU——每 GPU ≥200 万单元、负载均衡 metis+use-stored-partitions、带宽 5 GB/s/延迟 1e-6）；38.14 GPU 内存（节止于 p. 3974 章尾）。
- 扩充知识页 [[Fluent GPU 求解器]]（**Ch.38 全章完成**，pp. 3905–3974）。
- 提取边界：Theory Guide 引用式未提取；Table 38.5–38.15 摘要照录；Figures 38.3–38.8 图形元素；p. 3974 章尾。
- 下一续接位置：Part III / Ch.39 Adapting the Mesh，从 p. 3975 开始。

### 批次 108：Part III / Ch.39 Adapting the Mesh 全章（PDF pp. 3975–4014），新十批任务（106–115）第 3 批

- 新十批连续任务（批次 106–115）第 3 批，40 页（3975–4014），**Ch.39 全章完成**：39.1 使用自适应（并行自动负载均衡；叶栅五步示例；指南七条——表面网格须先足、初始网格足量、多面体仅 PUMA、悬挂节点+多面体两情形、先收敛后自适应、先存 case+data、梯度变量选型、勿过局部加密）；39.2 细化粗化（Manual/Automatic 对话框；方法三选——PUMA 默认/悬挂节点/2.5D PUMA、2D+Geo-Reconstruct 禁 PUMA；Refinement/Coarsening Criterion；Prismatic Adaption 各向异性拆分（PUMA 限、棱柱类限定、split ratio 0.5、prismatic-boundary-zones）；General Adaption Controls——Max Refinement Level 默认 2、Max Cell Count（PUMA）、Min Edge Length、Additional Refinement Layers、Min Cell Orthogonal Quality（2D/悬挂节点不可用）、Zones 限定、几何重建自适应（辅助几何配对规则、位移传播指数 0.01 起）；List Criteria/Display；Copy to Automatic；skip-until（默认 1、按控制台迭代计数、Hessian 三判据自动 2）；39.2.1 预定义判据五组——边界层 Cell Distance（boundary_cell_distance、可切 Volume Distance、PUMA 默认 Prismatic）；空气动力学五判据（Shock+Density-based、Pressure/Mach/Combined Hessian（光滑解告诫、ideal/real gas 限制、多场）、Goal-Based 伴随 observable（Sensitivities 类 Goal based error indicator (Raw)）与默认频率表（2/20、20/20、100/100、100/100、100 步/20 迭代）与 Hessian 需长频率告诫、register 名与 Hessian derivative 失效告诫、Pressure Hessian Indicator 场变量）；燃烧 Flame Indicator（含涡量默认开、Spark Region 球形火花区 Time/Centroid/Radius、频率 2、表达式与全局限制不一致告诫与最佳实践）；VOF 三选（Volume of Fluid/VOF-to-DPM Generic/Advanced、频率 2、vof_refinement_1）；Overset（不用 register、Orphan/Size（比值阈 3）/Gap（分辨率 4）/Coarsening 四选项、棱柱各向异性、define/overset-interfaces/adapt/set）；39.3 示例（边界 register 不能提高曲面分辨率；区域 register 鼠标探针；场变量 register——高梯度假设、Scaling Option 首选值 0.3–0.5/0.7–0.9、Scale by Global Maximum Eq 39.1 [0,1] 与粗化 0.2–0.4/细化 0.5–0.9；表达式自适应组合布尔照录两例）；39.4 悬挂节点几何重建（hanging-node 方法切换、Geometry Based Adaption 对话框、Reconstruct Geometry、Surface Meshes 读入、Wall Zones Set、止于 p. 4014 章尾图）。
- 新建知识页 [[Fluent 网格自适应]]（**Ch.39 全章完成**，pp. 3975–4014）。
- 提取边界：Theory Guide Eq 39.1 未提取按语义记录；Figures 39.1–39.38 图形元素；39.4 控制对话框内容止于章尾图。
- 下一续接位置：Part III / Ch.40 Creating Surfaces and Cell Registers for Displaying and Reporting Data，从 p. 4015 开始。

### 批次 109：Part III / Ch.40 第 1 段——40.1–40.2.10 前半（PDF pp. 4015–4046），新十批任务（106–115）第 4 批

- 新十批连续任务（批次 106–115）第 4 批，32 页（4015–4046），Ch.40 段 1/2：40.1 表面创建细节（Facets/Vertices 概念；Facet 值三类赋值——后处理表面取所在单元值不插值、内部区表面取 c0/c1 平均、边界区按边界物理（主变量=设定值/因变量=邻单元值）；Vertex 值——区表面顶点=网格节点值（加权平均/边界条件）、后处理表面顶点线性插值）；40.2 使用表面总览（表面存 case、边界区自动建 zone surface、命名规则字母/下划线开头禁斜杠；十类表面与两条显示注意——Flat 光照减伪线、2D 平面开 Edges）；40.2.1 Zone Surfaces（自动创建、reset-zone-surfaces、多选不自命名、zone-surface-N 前缀）；40.2.2 Partition Surfaces（Int/Ext Part、Cells/Interior 四组合语义）；40.2.3 Imprint Surfaces（**弃用**、仅 TUI、改用 External Surfaces、单位一致告诫）；40.2.4 External Surfaces（.stl 导入、Split Surface at Boundaries、**不存 case 须保留文件**、TUI）；40.2.5 Split Surfaces（跨边界拆分、TUI）；40.2.6 Point Surfaces（节点值线性平均/单元值、**overset 不兼容**、三定位法、closest-point-search TUI、2D 吸附须显示单元区面、triad 尺寸重启生效）；40.2.7 Structural Point Surfaces（须固体区+结构模型启用、Center 按钮）；40.2.8 Line/Rake（rake 等距/line 交点不等距、三定位法、Line Tool 全操作——平移/横向/旋转白轴/缩放端矩形/Reset 默认位、Preferences 需设 Probe）；40.2.9 Plane Surfaces（三法——坐标面/Point+Normal/Three Points、一次多面与 Spacing、Name Format plane-x={x:+.6f} 坐标命名、Bounded/Sample Points/Sample Density、Plane Tool 按方法三形态与多面行为）；40.2.10 Quadric Surfaces 前半（Type 三选、Line/Plane 与 Circle/Sphere 定义式、一般二次十系数——式中段跨下批）。
- 新建知识页 [[Fluent 表面与单元寄存器]]（Ch.40 段 1/2 完成，pp. 4015–4046）。
- 提取边界：二次曲面方程符号占位按数学语义补记；Figures 40.1–40.22 图形元素。
- 下一续接位置：Part III / Ch.40 40.2.10 Quadric Surfaces 续，从 p. 4047 开始。

### 批次 110：Part III / Ch.40 第 2 段收官——40.2.10 续–40.3（PDF pp. 4047–4078），新十批任务（106–115）第 5 批

- 新十批连续任务（批次 106–115）第 5 批，32 页（4047–4078，p. 4078 空页），**Ch.40 全章完成**：40.2.10 尾（命名/Create）；40.2.11 Iso-surfaces（前提初始化/读 data、patch 后须推进一步、From Surface/Zones、Compute Min/Max、滑块临时面告诫、多值一个面、Q Criterion Raw 不支持、多面命名递增）；40.2.12 Clipping（Iso-Clip 六步、表盘交互预览、原面不变）；40.2.13 Transforming（旋转/平移/等距偏移组合、用户创建面不可 transform、2D 绕 z）；40.2.14 Expression Volumes（面/体双态、两创建法、2D 面积体积参考深度语义、表达式示例、同变量可视化超范围插值告诫）；40.2.15 表面管理（Group/UnGroup、Rename、Rendering Priority 治 z-fighting 不作用于全局网格、Delete 不可逆、统计 Points/0D/1D/2D Facets 与先显示告诫）；40.3 单元寄存器（用途五项、三条注意——Overlays/并行计数差异/最多 16 个；Region 三形状与鼠标取点规则；Boundary Cell/Volume Distance 两法（式 40.1）；Variable Limiter 触限标记；Field Variable 四求导途径（Isovalue/Gradient 强激波/Curvature 光滑/Hessian 外流气动）+ 四缩放 + Type 十种 + Compute + Hessian 配 Global Average 建议；Residuals 仅压力基与 Threshold Percent；Volume Magnitude/Change 体积比；Yplus/Ystar 限第一层；管理对话框；Register Operations 报告（频率/最大单元数）；复制/重命名；后处理显示——Cell Registers... 类别、关 Node Values、值 1/0）；40.2.10 Quadric 尾补记。
- 扩充知识页 [[Fluent 表面与单元寄存器]]（**Ch.40 全章完成**，pp. 4015–4078）。
- 提取边界：Theory Guide Eq 40.1–40.7 公式体未提取按语义记录；Figures 40.23–40.42 图形元素；p. 4078 空页。
- 下一续接位置：Part III / Ch.41 Displaying Graphics，从 p. 4079 开始。

### 批次 111：Part III / Ch.41 第 1 段——41.1 前半（PDF pp. 4079–4130），新十批任务（106–115）第 6 批

- 新十批连续任务（批次 106–115）第 6 批，52 页（4079–4130），Ch.41 段 1/5：41.1 基本图形生成前半——persistent/non-persistent 图形对象（弃用与恢复开关、DPMS 远程显示）；41.1.1 图形性能（OpenGL2/DX11/Mesa、Preferences 五项——Surface Caching/Optimize for/Optimize Input Data/Min Frame Rate/Fast Interactive Display 及两条注意、default-interior 警告）；41.1.2 网格显示（四种视图与 Mesh Display 步骤；配色 Classic/Pastel 与 By Type/By Surface/Uniform 三法、偏好主题墙色、Ctrl+Shift+O 随机化限制；真实感材质与边界标记不兼容；透明默认 2 层与 Depth Peeling；Feature Angle 默认 20、Partitions、Shrink Factor；网格绘图定义）；41.1.3 等值线与剖面（两类对象、In Memory 动画无等值线、FSI 区域限定；快速着色 Save as Scene；生成七步——Levels 最大 100、Profile Options Reference/Scale/Direction 300K 例、Display State；选项——Filled 平滑条件、Auto Range/Clip to Range/Global Range、Draw Mesh 不存定义、Node/Boundary Values 四组合与 bnv 标记与不连续量用单元值告诫、Setup 1–10 不存 case；等值线定义唯一命名与 Add to、colormap 拖动、2D 自动建面）；41.1.4 矢量节起始（正文续下段）。
- 新建知识页 [[Fluent 图形显示]]（Ch.41 段 1/5 完成，pp. 4079–4130）。
- 提取边界：以界面流程为主；Figures 41.1–41.36 图形元素；p. 4118 "XREF" 占位照录。
- 下一续接位置：Part III / Ch.41 41.1.4 Displaying Vectors 正文，从 p. 4131 开始。

### 批次 112：Part III / Ch.41 第 2 段——41.1.4 续–41.2.1（PDF pp. 4131–4182），新十批任务（106–115）第 7 批

- 新十批连续任务（批次 106–115）第 7 批，52 页（4131–4182），Ch.41 段 2/5：41.1.4 续（Vector Definitions 管理——只读定义/删除/重命名禁标准名/Save-Load Scheme；矢量定义命名保存与 colormap）；41.1.5 迹线全集（生成步骤与 Step Size×Steps≈域长法则、Style 十种与 Pulse 限制、各 Style Attributes（sphere 直径 1/4 单元/refined-sphere 特性/Detail 4–50/Gouraud、ribbon Twist By）、配色默认 Particle ID、Path Skip 与自适应外观告诫、Path Coarsen 进单元恒画、Reverse、Oil Flow、Pulse Mode 与 Save Pulse Animation（Continuous 5 秒/Single 一周期）、Accuracy Control、Relative Pathlines、XY Plot along trajectories（Y Axis/X Axis Time-Path Length、Write to File）、迹线数据保存三格式（FIELDVIEW .fvp 稳态 ASCII 瞬态 BINARY/.ibl GAMBIT/EnSight .mpg+.mscl+.new.encas 格式照录）、Node Values 与不连续量告诫、迹线定义与场景限制）；41.1.6 LIC（原理与标准 LIC 无方向性、鼠标探针不可用、须先建 plane surface、设置十步含 Vectors of/Range 三选/Texture Size）；41.1.7 体渲染（Home/Transparencies（透明度 1 全透 0 不透）/Iso-Values/Clipping 四选项卡、裁剪作用于整窗、高质量图 Quality Best+Max Rendering Time 300s）；41.1.8 场景（多对象合成与逐对象透明度、材质面滑块无效须自定义材质、XY Plot 迹线不兼容、Save as Scene 含显示状态、colormap 逐对象尺度）；41.1.9 扫掠面（Sweep Axis/Compute/Display Type 三选/Create 存为等值面、动画仅 legacy 对象）；41.1.10 隐藏图形窗口（-driver null、存图变慢且可能不同、恢复与 close-all-open-windows、远程用 x11/msw）；41.2 起始（[Out of Date] 刷新、41.2.1 嵌入式仪表板 picture-in-picture 与 MP4 动画——节续下段）。
- 扩充知识页 [[Fluent 图形显示]]（Ch.41 段 2/5 完成，pp. 4131–4182）。
- 提取边界：以界面流程为主；Figures 41.37–41.55 图形元素；迹线数据文件格式照录（FIELDVIEW/.ibl/EnSight）。
- 下一续接位置：Part III / Ch.41 41.2.1 续，从 p. 4183 开始。

### 批次 113：Part III / Ch.41 第 3 段——41.2.7.2 续–41.3.2（PDF pp. 4183–4234），新十批任务（106–115）第 8 批

- 新十批连续任务（批次 106–115）第 8 批，52 页（4183–4234），Ch.41 段 3/5：41.2.7.2–41.2.7.4 标注管理（编辑/删除/拖动移动/Hide-Show 右键与对话框、与图形对象自动关联及 Annotations... 选用）；41.2.8 色标全套（Quick-Edit 面板、临时隐藏 X 与 Show Colormap、偏好 Colormap Settings、灰度存图告诫；术语十条 Diverging/Field/Flow-feature-N-bright-peak/Fringes/Highlights/Sequential/Split/Stacked/Striped/Symmetric/Value；预定义色标约 60 个名称照录；选择与 Size（10 倍数）/Log Scale/Dimensions；数字格式 float/exponential/general；Titles 三选与 Automatic Skip/Skip；自定义色标 Colormap Editor（Base/stops 增删改/Distribute（颜色数≥锚点）/Reverse/Apply/存 case）；参考文献六条照录）；41.2.9 灯光（偏好 Lighting 三项、只显网格面边显圆告诫与 Flat 解、Display Options 的 Lights On+三插值法 Flat/Gouraud/Phong、Lights 对话框 Headlight/Lighting Method、默认 light 0 深灰 (1,1,1)、加灯四步三定方向法（坐标/球面中键/Use View Vector）、移除保留定义与 Reset）；41.2.10 渲染选项（Line Weight/Marker/Animation All-Wireframe/Double Buffering/Front Faces Transparent 双面壁告诫/Hidden Surface Removal 四法 HW-Z、Painters、SW-Z、Z-sort 与适用性；Info 设备信息与驱动更新告诫）；41.3 增强视觉效果（前提 OpenGL2/DX11/Mesa；41.3.1 优先级四选 Automatic/Enhanced Graphics/Enhanced Performance/Custom；41.3.2 效果——Anti-aliasing/Reflections/Static-Dynamic shadows 与 Plane direction-offset 两字段——其余续下段）。
- 扩充知识页 [[Fluent 图形显示]]（Ch.41 段 3/5 完成，pp. 4183–4234）。
- 提取边界：以界面流程为主；预定义色标清单与文献条目照录；Figures 41.56–41.82 图形元素。
- 下一续接位置：Part III / Ch.41 41.3.2 续，从 p. 4235 开始。

### 批次 114：Part III / Ch.41 第 4 段——41.3.2 续–41.10.2.5（PDF pp. 4235–4286），新十批任务（106–115）第 9 批

- 新十批连续任务（批次 106–115）第 9 批，52 页（4235–4286），Ch.41 段 4/5：41.3.2 尾（Ground plane grid+Grid Lines Color、Update after mouse interactions）；41.4 光线追踪（Raytracing Display 设置——Keep Effects、3D HDRI 环境、backplate、Vertical/Horizontal/Spin 视点基准告诫、View Zoom/Model Scaling、Lock Model Location+Ground Height、Intensity/Color、Rendering 选项卡 CPU Threads/Quality/时长；动画两法——Runtime 勾 Raytracer Image 仅 2D 格式、Playback 转换 HSF；环境/backplate 清单照录；限制五条——仪表板不存 case、禁正交视图、Monochrome 不兼容、仅 3D 窗、keyframe 不兼容）；41.5 鼠标按键（Navigation/Theme、Box Select 三变体方向语义、Probe 短长描述与 Hover-Over 值差异告诫、Roll-Zoom、Rotate、Set View Center、Zoom 与滚轮迭代限制、Esc、3Dconnexion 不支持）；41.6 应用窗口；41.7 测量（Distance/Angle、Snap to Node、三点测角首点为顶点）；41.8 显示状态与视图（Ctrl+L/view last 回 20 视图；Display State 字段清单与全窗作用告诫与 None 语义；triad 交互五操作与 2D 限制；Auto Scale、旋转/自旋 auto-spin、平移、缩放与迭代限制；Perspective/Orthographic；相机四参数逐项 Apply；Default/Previous/Save/Write/Read/Delete 视图与默认视图覆盖告诫；镜像 Mirror Planes 与式 41.1 自定义平面；Periodic Instancing——Number of Reppeats 原文拼写照录、多排逐区设、Detect Surfaces 与跨区 iso 面告诫、Rotational/Translational、Clear Repeats、pathlines 粒子轨迹不能重复与 Scene 透明度不作用于重复面）；41.9 高级场景（Scene Description Compose；Names/Type；Display Properties 可见性九开关与 Colors/Transparency 0-100 与 Vector 存图告诫；Transformations 平移旋转缩放非累积与 Meridional 子午视图；Iso-Value 改值更新面上对象；Pathline Attributes Max Steps；Delete Geometry；Bounding Frame——Domain/Display、平面方块与棱边标注、Draw Frame 持久）；41.10 关键帧动画（两法对比——HSF/In Memory 免 case 可存 MP4 vs case/data 只能 MPEG；Animate 对话框、3000 帧上限、先改帧号再 Add 告诫、播放/Increment 快进/Auto Repeat-Auto Reverse/逐帧、保存三式 Key Frames .anm 须 case/Picture Files/MPEG 不可读回、Read .anm 前提；41.10.2.5 注意清单起于 p. 4279 末续下段）。
- 扩充知识页 [[Fluent 图形显示]]（Ch.41 段 4/5 完成，pp. 4235–4286）。
- 提取边界：界面流程为主；式 41.1 未提取按语义记录；Figures 41.83–41.115 图形元素；"Number of Reppeats"原文拼写照录。
- 下一续接位置：Part III / Ch.41 41.10.2.5 续，从 p. 4287 开始。

### 批次 115：Part III / Ch.41 第 5 段收官——41.10.2.5 续–41.14（PDF pp. 4287–4324），新十批任务（106–115）第 10 批

- 新十批连续任务（批次 106–115）第 10 批，38 页（4287–4324），**Ch.41 全章完成**：41.11.2 尾（并行 Write 的 Order Points 与重复点散点图告诫）；41.11.3 多数据源 XY 绘图（Load/Add XY/Add Report、Curve Information、Change Legend Entry、恒 SI 单位）；41.11.4 profile 两绘图（原始数据点 vs 初始化后插值边界值）；41.11.5 周向平均 XY（circum-avg-radial/axial TUI、带数默认 5、面积/质量加权、2D 用 interior volume 告诫、radial-bands/axial-bands 面）；41.11.6 XY 文件格式（title/labels/曲线结构照录、实验数据免 Cortex 变量示例）；41.11.7 残差绘图；41.11.8 直方图（Divisions 默认 10、Auto/Global Range、Add to Simulation Report、Plot/Print/Compute）；41.11.9 轴属性（标题字号、数字格式三型、Log 刻度指数语义、Range、Major/Minor Gridlines）；41.11.10 曲线属性（Pattern blank/Symbol blank、Size 屏高 3%、Sample 预览）；41.12 FFT 后处理（限制——五输入格式、等间隔假设、1/T 与 1/(2Δt) 频率界；窗函数四式；prime-factor FFT 与支持点数表；FFT 对话框——Load Input File/Process Receiver、Plot FFT 总声压级；Plot/Modify Input Signal——Clip to Range/Subtract Mean/分段平滑频谱（Overlap 建议 0.5、hop size）；输出全为单边正频率谱——Y 轴七函数（PSD/Magnitude/SPL/Sound Amplitude/A-B-C Weighted 公式号与默认参考声压 2e-5 Pa）、X 轴五函数（Frequency/Strouhal/Fourier Mode/Octave/1-3 Octave，Table 41.3 频带与计权照录）、Write FFT、Window 默认 None）；41.13 累积绘图（四类型、Direction+Divisions 切片、Force Direction 或 Moment Center+Axis、Compute from Force Statistics、Save/Plot）；41.14 瞬态后处理（Transient ribbon 选项卡前提、不用于单步、Timestep Selector 语义、Transient Display/Animation/Monitor/Compare Results、创建动画五步与 compute-and-clip-range TUI、Scene 禁含迹线粒子轨迹、Monitors 与 Stop Writing Files）。
- 扩充知识页 [[Fluent 图形显示]]（**Ch.41 全章完成**，pp. 4079–4324）。
- 提取边界：Theory Guide Eq 41.2–41.18 公式体未提取按语义记录；Table 41.1–41.3 照录或摘要；Figures 41.116–41.136 图形元素。
- 下一续接位置：Part III / Ch.42 Reporting Alphanumeric Data，从 p. 4325 开始（不在本十批任务范围内）。

### 批次 116：Part III / Ch.42 第 1 段——42.1–42.2（PDF pp. 4325–4360），新十批任务（116–125）第 1 批

- 新十批连续任务（批次 116–125）第 1 批，36 页（4325–4360），Ch.42 段 1/2：42.1 报告约定（2D 单位深度默认 1 m 且不受单位切换影响、DPM/流体质量流量按 1 m 深度缩放；轴对称按 2π）；42.2 监视与报告解数据（报告定义概念与 2019 R3 前 Expression 定义迁移告诫；通用创建十步——Per Surface/Zone 与 Average Over>1 不兼容、Average Over 滑动平均与 Retain Instantaneous Values、Create 组默认 Report File+Plot（Automatically Plot and File 偏好）、Create Output Parameter、Field Variable 与多相 Mass Flow Rate 专项告诫）；42.2.1.1 Surface 十七类型；42.2.1.2 Volume 十类型（Sum*2Pi 仅 2D 轴对称；Cell Zones 含表达式体积但 cell registers 不可用）；42.2.1.3 Force/Moment 四对话框（先填 Reference Values、Force Vector/Moment Center/Moment Axis 默认、Drag/Lift Force 未缩放输出 Tip、提前停算须核质量与换热守恒）；42.2.1.4 Flux 十一类型（内部区质量流量须 Per Zone 否则 0 及原因、通量仅在边界、输出参数含源贡献）；42.2.1.5 Mesh 报告（Cell/Face Count）；42.2.1.6 Aerodamping（TWM）报告（Per Zone 逐叶、Integrate Over=每周期步数）；42.2.1.7 DPM 报告七类型（瞬态限定标注、per-injection TUI 须在首批颗粒前启用、Show Mass Flow/Change Rate、Penetration Length 参数）；42.2.1.8 User Defined（DEFINE_REPORT_DEFINITION_FN 两步）；42.2.1.9 Expression 报告（花括号引用禁自动建议）；42.2.2 报告文件与绘图（同 Plot 定义须同单位、文件格式照录、Linux 文件名首字母 n/t 隐藏文件告诫、瞬态 Average Over 须 time-step/flow-time、Write Instantaneous Values、Report Plot 默认 1000 点与 History Size 偏好、滑动平均监视流程、Clear Data 清史）。
- 新建知识页 [[Fluent 数据报告]]（Ch.42 段 1/2 完成，pp. 4325–4360）。
- 提取边界：42.1 Depth 与轴对称角度数值为符号占位按惯例补记；Figures 42.1–42.22 图形元素。

### 批次 117：Part III / Ch.42 第 2 段收官——42.3–42.15（PDF pp. 4361–4394），新十批任务（116–125）第 2 批

- 新十批连续任务（批次 116–125）第 2 批，34 页（4361–4394），**Ch.42 全章完成**：42.2.2 尾（Clear Data——文件删盘重建/绘图清内存）；42.3 输出参数（十四种来源含命名表达式；Parameters 对话框 More 五命令；Per Surface/Zone+多选=单一合并值且 Average Over 须 1）；42.4 通量报告（Options 九选逐条语义——Total Heat 四项和与太阳源单列、Pressure Work/Viscous Work 条件、Film 两项 EWF、Electric Current；内部区双侧同流体改 wall 再回 interior 重定向量告诫、只选内部区净流量 0、比 Surface Integrals 的 Flow Rate 准；反应流两口径 Total Heat 守恒 vs Total Sensible 非守恒+Heat of Reaction Source 符号约定与非预混特殊处理；DPM 三源字段与颗粒反应热归 DPM Sensible；多相选 mixture 查总平衡与逐相 Heat of Reaction 约定；DDPM In-domain 两字段、示例报告照录、读旧 data 先跑一步与混合 injection 须重跑两限制、reinjected 颗粒归 In-domain；电位 Electric Current 与 Joule Heat Source；其他体积源不计入平衡=不平衡等于源值）；42.5 力报告（Forces/Moments/Center of Pressure 三 Options、分量零值坐标固定规则、输出压力/黏性力与系数逐区+净值、压力中心不可存输出参数、参考值依赖告诫、翼型示例照录）；42.6 投影面积（Min Feature Size 减半迭代至收敛、仅 3D）；42.7 面积分二十一类型（质量平均偏高速、Flow Rate 不如 Flux 准、零面积面用 Facet/Vertex、均匀性指数面积/质量加权语义）；42.8 体积分九类型（含 Sum*2Pi；表达式体积可用、cell registers 不可）；42.9 效率计算（Device Efficiency 对话框 Type/Process/Ratio 三选、Turbo Report 恒 Cp/γ 与 use-in-turbo-report 切换、命名表达式 EfficiencyIsentropic/Polytropic 规约函数、限制——理想气/单组分 real gas/湿蒸汽与支持位置清单）；42.10 直方图报告（Print 版）；42.11 DPM 采样报告指引；42.12 S2S 信息；42.13 参考值（用途清单、Compute From 部分设置、2D Depth 单位独立、Reference Zone 切换相对量）；42.14 case 摘要（Modified Settings Summary 双击可改 + Input Summary 四类 Print/Save）；42.15 系统资源（CPU Info/GPU Info/Memory Usage/Time Usage 三表字段与 Performance Timer 示例照录）。
- 扩充知识页 [[Fluent 数据报告]]（**Ch.42 全章完成**，pp. 4325–4394）。
- 提取边界：以界面流程为主；Figures 42.23–42.38 图形元素；DDPM 两相示例报告照录。
- 下一续接位置：Part III / Ch.43 Field Function Definitions，从 p. 4395 开始。

### 批次 118：Part III / Ch.43 第 1 段——43.1–43.3 前半（PDF pp. 4395–4434），新十批任务（116–125）第 3 批

- 新十批连续任务（批次 116–125）第 3 批，40 页（4395–4434），Ch.43 段 1/3：43.1 节点/单元/面值（单元值定义与 face-only 函数语义、节点值两步算法（逆体积加权+边界简单平均）与 bnv 标注、非网格节点顶点插值规则、zone surface 面值算术平均与主/因变量边界取值差异、后处理表面面值=关联单元值）；43.2 速度报告三选项（笛卡尔/柱坐标（四类工况坐标系与正向约定、可用分量按维度）/相对速度（Reference Zone 语义、无动区等价、滞止量与 Axial/Radial Coordinate 同用柱坐标））；43.3 分类场变量表结构——24 张类别表清单照录（Expressions 至 Cell Registers）、限制代码体系照录（2d/2da/bnv/cv/e/ke/kw/les/melt/mp 等约 80 个代码及其含义）、Table 43.1–43.4 前部内容示例（Velocity 类与 Temperature/Radiation/Solidification/Two-Temperature 类逐变量括注摘录）。
- 新建知识页 [[Fluent 场函数定义]]（Ch.43 段 1/3 完成，pp. 4395–4434；类别表仅记结构与代码体系不逐行复制）。
- 提取边界：Table 43.1–43.24 为参考清单按证据边界原则记结构与代码；Figures 43.1–43.2 图形元素。
- 下一续接位置：Part III / Ch.43 43.3 表续（Table 43.4 中段），从 p. 4435 开始。

### 批次 119：Part III / Ch.43 第 2 段——43.3 表尾 + 43.4 前半（PDF pp. 4435–4480），新十批任务（116–125）第 4 批

- 新十批连续任务（批次 116–125）第 4 批，46 页（4435–4480），Ch.43 段 2/3：43.3 表尾（Table 43.23 Aeromechanics——Wall Work/Power Density；Table 43.24 Cell Registers——register 名即变量）。43.4 字母序清单前半（A–M）：条目结构（类别+语义+单位量=Set Units 的 Quantity）；通用条目——cell_register_name（值 1/0、须关 Node Values）、Runtime DFT 三变量（-ba-mag 频带幅值/-ta-mag/-ta-phase [-π,π]）；代表性定义摘录——叶轮机坐标族（Abs (C-H)/(H-C) Spanwise、Abs Meridional、Abs Pitchwise 及单位 length/angle）、Absolute Pressure=操作压力+表压、Absorbed Radiation Flux (Band-n) 与 Absorbed Visible/IR Solar Flux、Absorption Coefficient（平均自由程倒数、多波段加权）、Accumulated Deformation（侵蚀动网格）、Accum Parcels/Particles in Cell（稳态/瞬态两种计数语义）、Dynamic Pressure 参考量、Pressure Discontinuity Sensor（二值激波标识、只示最强段）、Pressure Hessian Indicator；其余 A–M 条目（Density 族/Effective 三量/Enthalpy 族/Entropy/Gradient Quality Measure/Internal Energy/Laminar Flame Speed/Mach 等）同结构。
- 扩充知识页 [[Fluent 场函数定义]]（Ch.43 段 2/3 完成，pp. 4435–4480）。
- 提取边界：字母序清单为参考内容，按证据边界原则记结构与代表性条目不逐条复制（原条目 pp. 4435–4518）。
- 下一续接位置：Part III / Ch.43 43.4 清单续（M 之后），从 p. 4481 开始。

### 批次 120：Part III / Ch.43 第 3 段收官——43.4 续 + 43.5（PDF pp. 4481–4524），新十批任务（116–125）第 5 批

- 新十批连续任务（批次 116–125）第 5 批，44 页（4481–4524），**Ch.43 全章完成**：43.4 清单后半（M–Z 代表条目——Progress Variable 及方差（Eq 8.109）、PSD of dp/dt 倍频程/恒带宽族（Acoustic Sources FFT、2πf 换算）、Q Criterion Normalized/Raw（Eqs 43.30–43.32、TUI 名）、Radial Coordinate/Pull Velocity/Velocity/Radial-Wall Shear Stress、Radiation Heat Flux/Intensity Std Dev/Radiation Temperature (Eq 43.33)、NOx 七速率与 Soot 七速率族、Rate of Reaction-n（finite-rate/eddy-dissipation 取小者、颗粒反应 kmol/s/m³ 换算）、Reactor 族三量、Reduced Temperature/Pressure（仅 ARK）、Reflected 辐射通量、Refractive Index——同结构语义）；43.5 自定义场函数全节（三条语义——恒 SI 求值、fv 量用表达式、插值顺序差异；创建步骤与数值范围 1e-39/1e-45、命名禁重名、INV/ABS/ln/log10 按钮 ≤0 为 0、含报告定义不可导出；Manage 管理与 Save/Load Scheme 文件；三示例——压力比 Eq 43.78–43.79、临界速度比 λ Eq 43.80、旋流角动量流量 Eq 43.81；含模型相关函数仅在模型激活时计算）。
- 扩充知识页 [[Fluent 场函数定义]]（**Ch.43 全章完成**，pp. 4395–4524）。
- 提取边界：Eqs 43.30–43.33/43.78–43.81 公式体未提取按语义记录；字母序清单按证据边界原则摘录；Figure 43.3–43.4 图形元素。
- 下一续接位置：Part III / Ch.44 Parallel Processing，从 p. 4525 开始。

### 批次 121：Part III / Ch.44 第 1 段——44.1–44.5.4 前半（PDF pp. 4525–4555），新十批任务（116–125）第 6 批

- 新十批连续任务（批次 116–125）第 6 批，31 页（4525–4555），Ch.44 段 1/2：44.1 引言（host/cortex/compute-node-0 架构、MPI 消息传递、扩展性与系统匹配；推荐四步与异构集群告诫）；44.2 Launcher 并行（Parallel Settings——Interconnects/MPI Types 兼容性用户负责、Shared vs Distributed Memory、hosts 文件与 machine X:Y 块分配、GPU Remap、Select IP Interface；44.2.1 Scheduler 选项卡——Microsoft Job Scheduler、LSF（checkpointing）/SGE/PBS/Slurm 四调度器全设置、Submission Host/Queue/Node Only/Tight Coupling、环境变量 FL_SCHEDULER_EXCLUSIVE/PPN/GPN、Graphics Rendering Machine 三选与 Exceed CORTEX_PRE、HPC Pack 三选项；44.2.2 Remote 选项卡远程 Linux——SSH 免密、命令行 -nodepath/-node0/-nodehomedir/-rsh、cygwin 告诫、混合 UDF 两注意（文件不可见、单 UDF 库）、远程调度器设置全字段与排队时 GUI 保持打开、-gui_machine 图形机器）；44.3 Windows 命令行（fluent 3d -t4 -cnf=hosts.txt、hosts 规则、Tables 44.1–44.3 照录——msmpi/intel 默认分界 64 逻辑核、-ccp Microsoft Job Scheduler 全流程四式含 XML 模板与批模式照录）；44.4 Linux 命令行（-pinfiniband 示例、QT_XKB_CONFIG_ROOT 告诫、Tables 44.4–44.6 结构）；44.5 分区与负载均衡前半——44.5.1 概览（自动分区推荐、自适应保分布、meshing 分区保留与不均衡自动重分区）；44.5.2 自动分区（Auto Partition 对话框、Metis+Laplace 默认、架构感知重分区 >5%、Laplace Auto-Partition/Auto-Repartition 2023 R2 分界、Print Partitions 报告）；44.5.3 手动分区指南（Metis 默认、目标最小化边界面数比最大值）；44.5.4 对话框——Partitioning（整除约束、Laplace Smoothing+Cutoff Aspect Ratio、Reordering 两法 Architecture Aware/Reverse Cuthill-McKee 与 Reorder/Use Stored Partitions 流程）、Optimization（Merge/Smooth+Pre-Test）、Zones/Registers 指定分区 ID 用法、Weighting 选项卡（Faces per Cell 附加 2/Solid Zones 0.1 与 30–70% 规则/VOF geo-reconstruct/DPM/ISAT/Stiff Chemistry——后半续下段）。
- 新建知识页 [[Fluent 并行处理]]（Ch.44 段 1/2 完成，pp. 4525–4555）。
- 提取边界：XML 模板与示例命令照录；Tables 44.1–44.3 照录、44.4–44.6 记结构；Figures 44.1–44.8 图形元素。
- 下一续接位置：Part III / Ch.44 44.5.4 Weighting 续，从 p. 4556 开始。

### 批次 122：Part III / Ch.44 第 2 段收官——44.5.4 续–44.8（PDF pp. 4556–4584），新十批任务（116–125）第 7 批

- 新十批连续任务（批次 116–125）第 7 批，29 页（4556–4584），Ch.44 段 2/2 收官：44.5.4 Weighting 续（DPM 权重——需跑过一步颗粒追踪、Hybrid Optimization 兼 DEM；ISAT 权重与 Stiff Chemistry 权重互斥取后者、flame sensor；model-weighted partitioning（Metis 多约束，`parallel/partition/set/model-weighted-partition`）；动网格 Auto Repartition/Repartition Interval；Partition/Use Stored Partitions 按钮；44.5.4.1.1 分区 ID 示例照录；44.5.4.1.2 区内/寄存器内分区（Metis 不支持）；44.5.4.1.3 报告 verbosity 0/1/2；44.5.4.1.4 Default/Reset）；44.5.4.2 负载均衡（模型聚合计时、动态负载均衡）；44.5.5 分区方法（三目标；17 法全录——Metis 固体默认 0.1、虚拟多边形面跨非一致界面；Principal Axes 默认；44.5.5.2 Smooth/Merge 优化与 orphan cluster；44.5.5.3 Pre-Testing 2D×3/3D×4；44.5.5.4 分区过滤器 `utility partition` 与 Metis Zone...）；44.5.6 检查（active vs stored、统计字段全解、分区 ID→节点映射、overset 附加表、Cell Info 等值线图形检查）；44.5.7 负载分布 `load-distribution` (2 1 1) 示例；44.5.8 疑难（#AMG# 警告四对策、`global-check-coarsening?`、`enhanced-encapsulation?`）；44.6 线程控制三选；44.7 Connectivity 对话框；44.8 并行性能（44.8.1 Parallel Check 五项；44.8.2 performance meter 统计字段全解——消息数/延迟、数据量/带宽；44.8.3 Reporting Interval 告诫与加速 DO（`do-acceleration?`、强制一阶迎风+显式松弛 1.0、不兼容清单））；44.8.4 清 Linux 文件缓存（`-cflush` 或 `(drop-cache)` 需 sudo、NUMA 告诫、AMD 常见）。
- 知识页 [[Fluent 并行处理]] 扩充至全章完成（Ch.44 段 2/2，pp. 4525–4584）。
- 提取边界：44.5.4.1.1 示例命令输出要点照录；分区统计两表示例字段全录；performance meter 472 迭代示例字段全录。
- 下一续接位置：Part III / Ch.45 Running Fluent on Arm Compute Nodes，从 p. 4585 开始。

### 批次 123：Part III / Ch.45 Running Ansys Fluent on Arm Compute Nodes 全章（PDF pp. 4585–4588），新十批任务（116–125）第 8 批

- 新十批连续任务（批次 116–125）第 8 批，4 页（4585–4588），Ch.45 全章（45.1–45.5）：aarch64 + Armv8.2-A、仅批模式无 UI/图形、不支持 Windows；45.1 安装（tar/sh 安装器、推荐 Rocky 8.9/RHEL 8.8/9.3 与前置库）；45.2 Open MPI 4.1.8 唯一 MPI；45.3 命令行启动（默认 -g）；45.4 Slurm（-scheduler=slurm）；45.5 已知限制全清单（GUI/图形/Launcher/Meshing/FMU/MC 辐射/RBF 动网格/解释型 UDF/参数化研究/fe2ram/MKL/linx64 beta/各向异性自适应/五 Integrations/两 Add-ons/四 Workspaces）。
- 知识页 [[Fluent 并行处理]] 扩充 Ch.45 节（并入并行运行主题，Ch.44–45 同页）。
- 提取边界：Figure 45.1 记图形元素；45.5 限制清单全录。
- 下一续接位置：Part III / Ch.46 Using Simulation Reports，从 p. 4589 开始。

### 批次 124：Part III / Ch.46 Using Simulation Reports 全章（PDF pp. 4589–4616），新十批任务（116–125）第 9 批

- 新十批连续任务（批次 116–125）第 9 批，28 页（4589–4616），Ch.46 全章（46.1–46.8）：46.1 概览（HTML/PDF/PowerPoint 导出、Report Outline 任务页字段、本地服务器 vs serverless Ansys Dynamic Reporting——远程/参数化并发作业强制本地服务器）与 46.1.1 限制 13 条（OpenGL 2.1+、2025 R1 报告需 2025 R2 重生成、Linux QtWebEngine 警告与遗留文件、VMware Horizon、多会话服务器关闭、H264 插件、图形加速、AVZ 不入界面、字号不适用、BC 组分分数不显示、PPT 长表不拆分）；46.2 准备（Header 字段、各节 Description、46.2.1 全局属性四组——Visibility/Layout/Image/Theme、46.2.2 拖放重排与 Header 顶端/专用容器不可改两约束）；46.3 生成（report server 首启耗时、Stop 中断）；46.4 查看九节（FluentReportServer 文件夹保留即免重生成、System/Geometry-Mesh/Setup（Show Only Modified Settings 默认开、Reference Values、表达式超链接互跳）/Run（Include License Usage）/Solution Status/Named Expressions/Report Definitions/Plots（工具栏八钮）/图形对象（invert-normals-for-avz、AVZ 静态代理播放））；46.5 保存（PDF/standalone HTML/PPT、Linux PDF 需 X11）；46.6 Options 四项；46.7 定制五节（Object State View、X/Y 分辨率、Save Hardcopy、tabs/columns、*.fsrt 模板与 journal 模板跟踪、User Data 加图两式、隐藏节）；46.8 TUI /report/simulation-reports/。
- 新建知识页 [[Fluent 仿真报告]]（Ch.46 全章完成）。
- 提取边界：Figures 46.1–46.34 记图形元素；工具栏/字段名照录；`Qt WebEnging` 原文拼写照录并标注。
- 下一续接位置：Part III / Ch.47 Performing Parametric Studies 段 1，从 p. 4617 开始。

### 批次 125：Part III / Ch.47 Performing Parametric Studies 第 1 段——47.1–47.7.8.1 开头（PDF pp. 4617–4650），新十批任务（116–125）第 10 批

- 新十批连续任务（批次 116–125）第 10 批，34 页（4617–4650），Ch.47 段 1：47.1 前提（Base DP 前配好后处理量、optiSLang 免许可可用）；47.2 限制 11 条（meshing 无参数、CFD 相关、路径长度、optiSLang 中止标 failed）；47.3 四步入门；47.4 Ribbon 七分组（Study/Design Point/Simulation Report/Update Options/Update Status/optiSLang Capabilities/Comparison Plot）；47.5 Automatic DP Report Settings（DP 报告自动生成 + 参数化报告自动生成，HTML/PDF/PPTX 存储规则）；47.6 Outline View 双视图（Case View/Parametric Study View）；47.7 设计点表全套——47.7.1 列定制；47.7.2 更新（Sequential/Concurrent、180 秒远程延迟、分布式内存基准会话保持与许可影响、Concurrent Settings 对话框 Remote/Local 全流程、License Details 两式、HPC Platform 监视、47.7.2.1.2 本地并发 GPU 一 DP 一 GPU）；47.7.3 添加 DP（Manual；optiSLang Create DOE——默认六采样型 + Pro 另八型、±10% 边界、AWP_ROOT→OPTISLANG_EXE→OPTISLANG_HOME 查找序；Create DOE and Optimize——Criteria 表、AMOP/One-Click、结果表红绿高亮；47.7.3.2.2.1 AMOP 设置全字段（Refinement Type/Start Iteration/Refinement/Target CoP 等）；47.7.3.2.2.2 OCO 设置全字段（Max Evaluations/Use MOP/Seed/999 上限等））；47.7.4 DP 右键操作 14 项；47.7.5 Generate DP Reports 对话框（跳过规则、必要操作原则）；47.7.6 CSV 导入导出全规则（Name/Units 忽略、状态全置 Needs Update、列名精确匹配）；47.7.7 Update Mesh Morphs（参数更新后解初始化前执行）；47.7.8 DP 流程细节（Base DP 起止行为、case 改动三分支、相对路径告诫、数据文件初始化）至 47.7.8.1 开头（初始化数据三来源）。
- 新建知识页 [[Fluent 参数化研究]]（Ch.47 段 1/2 完成，pp. 4617–4650）。
- 提取边界：Figures 47.1–47.8 记图形元素；采样类型/许可字段/对话框字段照录；原文拼写 `Parameteric Report`、`Tn the local approach`、`dependant` 照录并标注。
- 下一续接位置：Part III / Ch.47 47.7.8.1 Initializing Design Point Data 续，从 p. 4651 开始。

### 批次 126：Part III / Ch.47 第 2 段收官——47.7.8.1 续–47.12（PDF pp. 4651–4684），新十批任务（126–135）第 1 批

- 新十批连续任务（批次 126–135）第 1 批，34 页（4651–4684），Ch.47 段 2/2 收官：47.7.8.1 续（初始化三选项 Case Settings/Base Data/Previous Updated 及 Sequential 链式、Local/Remote 并发差异、Previous Updated 强制写数据）；47.7.8.2 复用 case（Read Case Before Each Design Point Update Yes/No × 三初始化法行为表）；47.7.8.3/47.7.8.4 case 改动管理与更新期改动提示（Automatically proceed 选项）；47.8 监视（十状态计数、Updating/Queued 期禁用项、Show transcript/monitors/residuals、残差 Iterations to Plot/Store 告诫）与 47.8.4 图形定制；47.8.1 optiSLang 导出五式（Export Designs/Go to optiSLang/Open Designs in Postprocessor/Open OMDB/CSV）与 TUI；47.8.2 Data Visualization 交互图与 Design Table；47.8.3 Parametric Plots 比较图；47.9 DP 报告与参数化报告（设置入口、Save Settings 先于更新告诫、DP 报告节差异 Mesh Size/Value、参数化报告 Conditional Formatting 三式、Image Slider View Settings 三式、Pan/Grid/Probe/Pin 工具与 Probe 互斥、XY 过滤比较 HTML 动态 vs PPT/PDF 静态、PPT 嵌入 Excel 与登记导出、过时判定与 "(out of date)" 标签、named expressions 输入参数表达式两报告差异）；47.10 偏好（Write Data/Capture 默认、逐 DP 存项目、自动刷新 10s/最小 5s、Layout 两开关）；47.11 当前 case 参数表；47.12 文件管理（*.flprj 项目开存归档、Project View 列定制与 .out 可见性、DP 工作目录切换与文件注册、动画 Storage Directory '.'、轻量项目不载 case/data）。
- 知识页 [[Fluent 参数化研究]] 扩充至全章完成（Ch.47 段 2/2，pp. 4617–4684；p. 4684 空白页）。
- 提取边界：47.7.8.2 三张 Yes/No 行为表要点照录；Figures 47.9–47.20 记图形元素；十状态名称照录。
- 下一续接位置：Part III / Ch.48 Design Analysis and Optimization 段 1（48.1 The Adjoint Solver），从 p. 4685 开始。

### 批次 127：Part III / Ch.48 第 1 段——48.1 The Adjoint Solver（PDF pp. 4685–4702），新十批任务（126–135）第 2 批

- 新十批连续任务（批次 126–135）第 2 批，18 页（4685–4702），Ch.48 段 1：章引言（伴随 = 梯度法 vs 变形器/优化器 = 非梯度；共同网格变形途径；两选择判据——物理/观测量支持性与设计空间维度 10–20 自由度分界）；48.1 全节——原理定位（单次计算得观测量对大量输入导数、高敏感区改动原则、Taylor 一阶外推边界）；48.1.1 通用观测量全类型（expression/Force/Moment/Swirl 两积分/pressure drop/fixed value/表面积分十式/体积分十式含 Target-volume-integral、场变量与 adjoint energy/turbulence 前提、目标场数据写 UDM 要求）；48.1.2 通用运算（比/积/二次惩罚/线性组合七型/平均/方差/一元运算）；48.1.3 离散 vs 连续伴随（连续法不一致性污染敏感度、Ansys 判定不适用；离散法被采纳）；48.1.4 离散伴随概览（三要素、控制变量界定与网格拓扑固定、伴随方程定义消去流扰动、adjoint velocity/pressure、Jacobian 转置、伪时间推进预条件迭代、人工压缩性）；48.1.5 稳定化（Dissipation 与 Residual minimization 两方案全解）；48.1.6 基于解的自适应（ε~h^p、伴随加权、大伴随速度/压力单元自适应）；48.1.7 用数据改设计（梯度/最速下降、稳健性、噪声平滑）与 48.1.7.1 三变形技术（polynomials 的 Bernstein+B-spline 叠加、direct interpolation 加权平均与限制、RBF 核函数与非线性区域条件限制）与两约束法（standard 三选择建议、enhanced 四限制）。
- 新建知识页 [[Fluent 设计分析与优化]]（Ch.48 段 1/6 完成，pp. 4685–4702）。
- 提取边界：式 48.1–48.54 记结构与语义（抽取文本符号缺失，注明须对照原文）；Figures 无（本段以公式为主）。
- 下一续接位置：Part III / Ch.48 48.2 Using the Adjoint Solver 段 2（48.2.1–48.2.3.2），从 p. 4703 开始。

### 批次 128：Part III / Ch.48 第 2 段——48.2.1–48.2.3.2.1 前半（PDF pp. 4703–4730），新十批任务（126–135）第 3 批

- 新十批连续任务（批次 126–135）第 3 批，28 页（4703–4730），Ch.48 段 2：48.2 引言七步典型工作流；48.2.1 模型考量——48.2.1.1 基本假设与一致性检查（稳态单相/理想气体、k-ε/k-ω、冻结湍流与 GEKO、UDS/组分伴随最多 50 条及支持范围、2D 轴对称与 MPM 不支持、SRF/MRF 绝对速度、材料属性非常数支持清单、边界条件类型限定与 Wall 限制、警告 vs 错误消息机制）与 48.2.1.2 用户源项 DEFINE_SOURCE_AE 宏与 dS[] 导数要求；48.2.2 观测量定义——创建/编辑（工作区概念）、各类型输入全清单、表达式观测量规则（单值/场/组合、禁 Flux 与 Report Definition、禁 gradient/normalize、避不连续函数、角度除 1[rad]、可用变量全清单）、单观测量选择与 Sensitivity Orientation、湍流模型优化观测量（目标场 UDM write-data/read-data、常数目标三步法）；48.2.3 求解伴随——48.2.3.1 Methods 对话框（Adjoint Energy/Ideal Gas/Turbulence（GEKO 优点与代价、Intermittency 不兼容）/UDS/species、AMG Full vs Partial 块结构（49 vs 16+1）、Default/Best Match/Balanced 三预设、Rhie-Chow 与 match-fluent-flux-type?、劣质网格数值与 undo-2024r1-default-changes?）；48.2.3.2 Controls 对话框（Solution-Based Controls Initialization、Auto-Adjust Controls 行为、Apply Preconditioning/Courant/Artificial Compressibility/各 Equation Scaling/欠松弛因子、AMG Tolerance/Max Iterations/Show Iterations）；48.2.3.2.1 稳定化策略前半（None/Blended、Residual Minimization 4、Auto Detection? 与显式切换、Initialize Strategy 告诫、Default/Complex Case 预设）。
- 知识页 [[Fluent 设计分析与优化]] 扩充（Ch.48 段 2/6）。
- 提取边界：DEFINE_SOURCE_AE 参数表照录；可用表达式变量清单全录；Figures 48.1–48.7 记图形元素。
- 下一续接位置：Part III / Ch.48 48.2.3.2.1.1 Dissipation Scheme 续，从 p. 4731 开始。

### 批次 129：Part III / Ch.48 第 3 段——48.2.3.2.1 续–48.2.4.3 开头（PDF pp. 4731–4746），新十批任务（126–135）第 4 批

- 新十批连续任务（批次 126–135）第 4 批，16 页（4731–4746），Ch.48 段 3：残差最小化使用提示（先无稳定化跑至发散再启用、Blended 即此法、残差停滞判据与 Initialize Stabilization）；48.2.3.3 Adjoint Residual Monitors 对话框（Print/Plot/Iterations to Plot、八伴随方程收敛判据）；48.2.3.4 收敛诊断三 TUI（print-residuals-by-zone / retain-cell-residuals——局部发散可避区使用 / print-residuals-by-distribution、至少跑 1 迭代告诫）；48.2.3.5 Run Adjoint Calculation 对话框（Initialize/Initialize Strategy/Initialize Stabilization 三按钮语义、Number of Iterations、Calculation Activities——Autosave 与 Execute Commands 的 Adjoint Iteration/Design Iteration 时机）与 48.2.3.5.1 Adjoint Autosave（默认 0 不存、保留 5 份）；48.2.4 后处理总则（逐单元敏感度、体积归一化）；48.2.4.1 Postprocess Options（Maximize/Minimize、Method RBF vs Spring 与 Laplace 平滑、Smoothness）；48.2.4.2 场数据全集（体敏感度族、Artificial Dissipation、形状敏感度族含 Normal/Surface/log10 与分量、最优位移族、边界速度/压力/温度/热通量/UDS/组分敏感度、Flow Blockage、GEKO 四参数敏感度与优化/训练值、神经网络流特征与 Mahalanobis distance、Local Solution Marker、七伴随残差场）与矢量场六种（含 Optimal Displacement 绝对位移显示法、Boundary Mass Flux）；48.2.4.3 标量数据开头（Adjoint Reporting 对话框入口）。
- 知识页 [[Fluent 设计分析与优化]] 扩充（Ch.48 段 3/6）。48.2.4.3 尾部（p. 4747 开头）随批次 130 读取并入。
- 提取边界：Sensitivities... 字段与 Vectors of 矢量场清单全录；原文拼写 `Sesnitivity to Shape` 照录；Figures 48.8–48.12 记图形元素。
- 下一续接位置：Part III / Ch.48 48.2.4.3 续 + 48.2.5 Design Tool 段 4，从 p. 4747 开始。

### 批次 130：Part III / Ch.48 第 4 段——48.2.4.3 续 + 48.2.5 Design Tool（PDF pp. 4747–4779），新十批任务（126–135）第 5 批

- 新十批连续任务（批次 126–135）第 5 批，33 页（4747–4779），Ch.48 段 4：48.2.4.3 收尾（Adjoint Reporting 的 Report/Write 与线性外推示例）；48.2.5 全节——总览与 11 步流程（Basic/Advanced 可见性、Enhanced 默认 Polynomials、Modifiable Zones、双面壁与非一致界面告诫）；48.2.5.1 区域定义（Cartesian/Cylindrical、Get Bounds 与 Comfortable/Automatic Coordinate、圆柱区域四注意、对称条件对区域的影响）；48.2.5.2 区域条件（控制点 20–40/向、Motion Enabled、Shape Preserving、Symmetric、Periodic 与三区分告诫、Region Boundary Continuity 的 Uniform/By Boundary 与 In-Plane Motion Only、Apply Continuity）；48.2.5.3 观测量目标（Export/Import 敏感度、Include Current Data、Objective 三选、Target/Reference Change 与 As Percentage）；48.2.5.4 设计条件九类型全解（Iso-Clip by Region 对话框、条件选项、预测范围缩小告诫与同面单条件 Important、Fixed Walls/Bounding Planes/Bounding Surfaces（.stl/.msh/.cas 导入、Orientation 全局、Bounding Offset、Fit 与 Scale Factor、Preconditioning 建议）/Prescribed Profiles（表达式 vs UDF 语义差、Scale Factor 自由参数）/Rotation/Translation/Scaling 四型/Rigid Body/Compound（superposed vs sequenced））；48.2.5.5 数值（三法 Smoothness 语义、RBF 两核 Inverse MultiQuadric 默认与 Bi-Harmonic、Calculation Numerics 按方法设置全解、Constraint Relaxation/Preconditioning 取舍、Enhanced 主/次变形器三 Improve 选项与 Solve Free Parameters by Using Direct Interpolation）；48.2.5.6 形状修改 14 步全流程（Applied Constraints 与 Fix Surfaces 的 adjacency/distance 两法、Weight 使用条件、Freeform Scaling Scheme 两式、Check 的 Fatal/Possible 分级、Calculate Design Change、Export Expected/Displacements 格式、Preview 与 Export STL、Mesh History 参考网格与两限制、Modify/Revert/Remesh（仅四面体+棱柱/三角形、重划后不可逆）、Export STL Merge Surfaces 与 Export CAD 全字段（Base CAD/STL、New STL、Feature Tolerance 1/10 法则、Detach Original Bodies、Remove Inputs from CAD）与 CAD 导出五限制）。
- 知识页 [[Fluent 设计分析与优化]] 扩充（Ch.48 段 4/6）。
- 提取边界：Figures 48.13–48.23 记图形元素；原文 p. 4779 CAD Feature Tolerance 条目重复排版两次，照录并标注；`descibed` 原文拼写照录。
- 下一续接位置：Part III / Ch.48 48.2.6 Using the Gradient-Based Optimizer 段 5，从 p. 4780 开始。

### 批次 131：Part III / Ch.48 第 5 段——48.2.6 Using the Gradient-Based Optimizer（PDF pp. 4780–4814），新十批任务（126–135）第 6 批

- 新十批连续任务（批次 126–135）第 6 批，35 页（4780–4814），Ch.48 段 5：48.2.6 全节——准备豁免清单与湍流优化前置；通用流程 14 步（Type shape-opt/turb-model-opt、Observables 的 instantaneous/averaged、Operating Conditions、Objectives 表 Goal 四选 None/Step Size/Equal（二次惩罚 50%/迭代）/Bounded 与约束可行性机制（清零、界+容差拉回、35% 规则、Tolerance 与 Tol. Perc?/Percentage? 示例）、Optimizer Settings 三 Method（fixed/adaptive（接受判定与 50% 缩减规则、自动保存 -design-latest）/line-search（单观测量限、5–10 次流场子迭代、适用场景））、No. of Design/Flow/Adjoint Iterations 与 Convergence Criteria、Mesh Quality 组（Min. Cell Volume/Orthogonal Quality、Print Current Status、Post Morph Smoothing/Remeshing）、Monitor 虚实线诊断、Autosave 命名与 Save During the Optimization 限制、Execute Commands 十个 ;@ 关键字、Solution Animation design-iteration、Initialize/Optimize/Summarize、最佳实践五条）；48.2.6.1 Turbulence Model Design Tool——48.2.6.1.1 online（推荐）/offline 两策略优劣与组合用法、两模式流程；48.2.6.1.2 Design Region（壁面与尾迹）；48.2.6.1.3.1 设计变量（Enable Turbulence Source Term、TKE Source Coefficient 推荐、CMIX 钝体告诫、Limits、Initialize 与 BF 先收敛）；48.2.6.1.3.2 Model（None + Smooth Sensitivities / Neural Network、Hook/Unhook）；48.2.6.1.3.2.1 NN 设置（激活函数四种、默认拓扑 24/16/8、八个默认 Input Features 及输出范围、表达式特征最多六条、无隐层特例）；48.2.6.1.3.2.2 离线训练（Epochs、Mini Batch 10–1000、Learning Rate、.tdat 训练数据管理、Train 与冗余特征判据）；48.2.6.1.3.3 验证三步（Apply Trained Model 后不可访问）；48.2.6.1.3.4 管理（.scm 导入导出、训练/部署工况相似性要求、Clear）。
- 知识页 [[Fluent 设计分析与优化]] 扩充（Ch.48 段 5/6）。
- 提取边界：式 48.55–48.75 记结构与输出范围（符号缺失须对照原文）；文件命名模板照录；Figures 48.24–48.37 记图形元素。
- 下一续接位置：Part III / Ch.48 48.3 Geometry Parameterization and Exploration 段 6，从 p. 4815 开始。

### 批次 132：Part III / Ch.48 第 6 段收官——48.3–48.5（PDF pp. 4815–4848），新十批任务（126–135）第 7 批

- 新十批连续任务（批次 126–135）第 7 批，34 页（4815–4848），Ch.48 段 6/6 收官：48.3 几何参数化与探索（Parameterize and Explore、无需伴随、Region/Region Conditions（Custom Plane?/External Periodic 与 Design Tool 行为差异告诫）/Design Conditions 七类、默认全可改须 fixed-walls、Symmetric/External Periodic 区内网格也变形、Numerics、Design Change）；48.4 网格变形器/优化器（三限制——动滑移网格/几何参数重算/任意形状区域；流程本质（盒式区域、控制点、RBF 或 Bernstein）；48.4.3 六优化器全解——Compass/NEWUOA（信任域、参数多推荐、须 UDF 目标）/Simplex（Nelder-Mead、顶点=CFD 计算）/Torczon（rotation 先行）/Powell（黄金分割+共轭方向）/Rosenbrock（λ 步长伸缩））；48.5 使用流程 17 步全解（目标函数三式与 objective_function/objective-function 命名及 rpvar、Control Point Distribution Regular（Bernstein、仅平移）vs Unstructured（RBF、旋转径向、扭转）、变形区盒定义与 Direction 向量规则、控制点四法定义（Mouse-Probe/BSP 分布/坐标/ASCII 文件）、Constraints 三选默认与固定区须有自由区告诫、参数值单位规则（米/度）与 Bounds、Motion Settings 两式（Indexed Grouping、多运动位移叠加与顺序无关）、手动 Deform/Check/Reset、disable-mesh-check 与 Initial Commands 修复、Objective Function Definition（UDF/Scheme/Custom Calculator）、Optimizer Settings（Maximum Number of Designs 与 Run 号区分、newuoa Initial Parameter Variation）、Mesh Quality 下限、中间文件组、Initialization 三选（Read Data File 非 newuoa）、Execute Commands Initial/End 与 %i 迭代号陷阱、Optimization History Monitor、Optimize 与续算告诫、workbench 优化器（须从 Workbench 启动）与设计点路线）。
- 知识页 [[Fluent 设计分析与优化]] 扩充至全章完成（Ch.48 段 6/6，pp. 4685–4848；p. 4848 空白页）。
- 提取边界：Figures 48.38–48.51 记图形元素；TUI 路径与 rpvar 名照录；六优化器文献编号照录。
- 下一续接位置：Part III / Ch.49 Performing System Coupling Simulations Using Fluent 全章，从 p. 4849 开始。

### 批次 133：Part III / Ch.49 Performing System Coupling Simulations Using Fluent 全章（PDF pp. 4849–4886），新十批任务（126–135）第 8 批

- 新十批连续任务（批次 126–135）第 8 批，38 页（4849–4886），Ch.49 全章（49.1–49.12）：49.1 能力（力/位移/热传递、刚体 FSI 三步与 SC 运动参数、Maxwell 电弧、时均 HTC 子步与 Wall Functions/Y plus 法、 Tables 49.2–49.4 流入边界变量全录）与限制 13 条（禁 RSM、Unified remeshing、3D 无悬挂节点、拓扑固定、禁 NITA、禁 shell conduction 等）；49.2 .scp 生成（Write/Auto-write、2020 R1 元素数据映射 TUI）与 Fluent Input Option 三值表及 GenerateInputFile()；49.3 Workbench 流程与 OutOfDate 状态错误；49.4 变量表（Tables 49.2–49.7 全录）、壁面传力式 49.1 与参考压力语义、多孔跳跃两情形传力、增量位移与首迭代 0 m、滑移网格参与者禁旋转、绝对压力海底管道示例（最佳参考压力 −10 bar）；49.5 Fluent 设置（双精度、MDM 与解稳定化、HTC 参考温度法 use-tref-in-htc-calculation?、UDM 耦合变量、Run Calculation 时间步与迭代数被 SC 接管、稳态迭代语义与 rpsetvar 恢复旧法）；49.6 FSI 建议全节——49.6.1 接触检测两侧配置与渲染/verbosity TUI；49.6.2 动网格（扩散平滑 α=1.5、线性弹性/RBF 例外、Lmin/Lmax 0.4/1.4 起点与 Region Face+Local Cell 必选）；49.6.3 四病理（折叠诊断 TUI、棱柱层三对策与 49.6.3.2.1 边界层平滑拆区八步含 dummy UDF、49.6.3.2.2 overset 工作流与 donor-priority-method 0/1 及 CFD-Post/体积分注意、高偏斜两对策、起跑封堵三对策）；49.7 执行影响；49.8 重启（自动重启文件、Solution 单元勿 Setup、Recover Missing Solution、.backup 不可用于重启）；49.9 补丁数据 *.ip 变通（不适用设计点）；49.10 SC 界面运行参与者指引；49.11 排障三文件（cortexerror.log/solution 1.log/solution.trn、sc/verbosity 1）；49.12 许可（参与者各需许可、SC 本身免费）。
- 新建知识页 [[Fluent System Coupling]]（Ch.49 全章完成）。
- 提取边界：Tables 49.1–49.7 全录（`k-epsiloin` 抽取伪影已注明）；dummy UDF 代码照录；Figures 49.1–49.15 记图形元素；式 49.1 与时均公式符号缺失注明。
- 下一续接位置：Part III / Ch.50 Customizing Fluent 全章，从 p. 4887 开始。

### 批次 134：Part III / Ch.50 Customizing Fluent 全章（PDF pp. 4887–4888），新十批任务（126–135）第 9 批

- 新十批连续任务（批次 126–135）第 9 批，2 页（4887–4888），Ch.50 全章：全章仅一段——可用 Ansys ACT 创建仿真向导（simulation wizards），在独立 Fluent 或 Workbench 中的 Fluent 运行；一般 ACT 用法见 ACT Developer's Guide，Fluent 专属见 ACT Customization Guide for Fluent（本手册不展开）。p. 4888 空白页。
- 内容过小不单独建页；已并入知识页 [[Fluent 程序架构与能力]] 的"定制（ACT）补充"节。
- 提取边界：无图表。
- 下一续接位置：Part III / Ch.51 Task Page Reference Guide 段 1（51.1–51.3），从 p. 4889 开始。

### 批次 135：Part III / Ch.51 Task Page Reference Guide 第 1 段——51.1–51.3（PDF pp. 4889–4902），新十批任务（126–135）第 10 批

- 新十批连续任务（批次 126–135）第 10 批，14 页（4889–4902），Ch.51 段 1：章引言 21 任务页清单；51.1/51.2 各一句（Meshing/Setup 任务页导引）；51.3 General 任务页全解——Important CFD Pro 功能受限；Mesh 组（Scale/Check/Report Quality/Display）；Solver 组（Type 压力基/密度基、Velocity Formulation、Time、2D Space 三式与轴对称 zone 类型改 axis 告诫）；Gravity；51.3.1 Scale Mesh 对话框（Domain Extents、Mesh Was Created In 自动因子、Scale/Unscale、View Length Unit In）；51.3.2 Mesh Display 对话框（全局非持久 vs New... 持久两版、Options 六项含 Overset/Gap、Edge Type、Surfaces 与 New Surface 七式、Outline/Interior/Adjacency、Coloring 四式与 Ctrl+Shift+O 随机化）；51.3.3 Set Units（四标准制 default/si/british/cgs、Factor/Offset）；51.3.4 Define Unit；51.3.5 Mesh Colors。
- 新建知识页 [[Fluent 任务页参考]]（Ch.51 段 1，章内进行中）。
- 提取边界：控件名照录、页码交叉引用保留；无图表（本段为控件参考）。
- 下一续接位置：Part III / Ch.51 51.4 Models Task Page 段 2，从 p. 4903 开始。

## 续接检查点

- 跨会话/智能体唯一进度文件：[[ingest-state]]。
- 最近完成：批次 135，Part III / Ch.51 段 1（pp. 4889–4902，51.1–51.3）；知识页 [[Fluent 任务页参考]] 新建。**新十批连续任务（批次 126–135）全部完成（10/10）。**
- 下一续接位置：Part III / Ch.51 51.4 Models Task Page 段 2（p. 4903 起）；详见 [[ingest-state]]。



## 摄取边界

- 本资料处于 `partially-ingested` 状态。已建立完整书签地图；Part I Chapter 1–4 已完成（p. 219 Glossary 待摄取）；Part II 全部完成（pp. 223–908，含 Appendix C 与 Bibliography）；Part III 扉页与 Ch.1–6 已完成（pp. 909–1168）；Part III Ch.7（自 p. 1169）起与 Part IV 待摄取。
- 目录页码来自 PDF 书签定位；正文批次引用 PDF 物理页码。使用时应以来源原文和具体 Fluent 版本为准。
- 文本提取存在字符间空格异常；p. 183 部分残差阈值公式在抽取文本中缺失，因此未将其数字纳入知识页。需要具体残差门槛时，须视觉核对 PDF 页面。
- 批次 4 核验记录：Table 1.1（pp. 153–154）普通文本提取丢失勾选列位置，已用版面模式提取 + 字形 x 坐标与表头列坐标逐行比对确认级别归属；p. 170 两处可疑字符串（`FLUENT_WB_REMOVE ALL_GENERATE_FILES` 含空格、`/usr/lib/x86-64-linux-gnu/lib-stdc++.so.6` 写法）经 600 dpi 渲染视觉核对，确认为手册原文印刷形式，知识页中已标注疑为排版错误、待验证。
- 手册中的操作建议和默认值受问题、模型、网格和版本条件影响，不应脱离上下文视为通用保证。

## 关联页面

- [[Ansys Fluent User's Guide - 总览]]
- [[Part I - Getting Started]]
- [[Part II - Meshing Mode]]
- [[Part III - Solution Mode]]
- [[Part IV - Web Interface]]
- [[index]]
- [[Ansys Fluent Users Guide 2026 R1 - 目录地图]]
- [[Fluent 程序架构与能力]]
- [[Fluent 2026 R1 已知限制]]
- [[CFD 仿真工作流与验证]]
- [[Fluent 启动与批处理自动化]]
- [[Fluent 网格模式入门]]
- [[Fluent 网格模式文件读写与导入]]
- [[Fluent 引导式网格工作流]]
- [[Fluent 水密几何网格工作流]]
- [[Fluent 容错网格工作流]]
- [[Fluent 2D 网格工作流]]
- [[Fluent 高级网格主题]]
- [[Fluent 第三方网格导入与 fe2ram 过滤器]]
- [[Fluent 网格文件格式（legacy .msh）]]
- [[Fluent 网格质量诊断]]
- [[Fluent 快捷键与实体信息]]
- [[Fluent 手册排版与数学约定]]
- [[Fluent 求解模式 GUI]]
- [[Fluent 求解模式文件读写]]
- [[Fluent 单位制]]
- [[Fluent 表达式语言]]
- [[Fluent 模型拓扑（Model Topology）]]
- [[Fluent 网格读取与操作]]
- [[Fluent Cell Zone 与边界条件设置]]
- [[Fluent 物理属性]]
- [[Fluent 基本流动建模]]
- [[Fluent 运动参考系]]
- [[Fluent 运动定义与辅助几何]]
- [[Fluent 滑移与动网格]]
- [[Fluent 叶轮机械流动]]
- [[Fluent 湍流模型设置]]
- [[Fluent 热能模拟]]
- [[Fluent 高超声速流动]]
- [[Fluent 虚拟叶片模型（VBM）]]
- [[Fluent 组分输运与有限速率化学]]
- [[Fluent 缩阶湍流燃烧模型]]
- [[Fluent 发动机点火模型]]
- [[Fluent 污染物生成模型]]
- [[Fluent 气动噪声模型]]
- [[Fluent 离散相模型（DPM）]]
- [[Fluent 宏观颗粒模型（MPM）]]
- [[Fluent 多相流模型]]
- [[Fluent 熔化与凝固]]
- [[Fluent 流固耦合（FSI）]]
- [[Fluent Eulerian 壁面液膜]]
- [[Fluent 电势场与电化学]]
- [[Fluent 电池模型]]
- [[Fluent 燃料电池]]
- [[Fluent 磁流体动力学（MHD）]]
- [[Fluent 连续纤维模型]]
- [[Fluent 降阶模型（ROM）]]
- [[Fluent 求解器使用]]
- [[Fluent GPU 求解器]]
- [[Fluent 网格自适应]]
- [[Fluent 表面与单元寄存器]]
- [[Fluent 图形显示]]
- [[Fluent 数据报告]]
- [[Fluent 场函数定义]]
- [[Fluent 并行处理]]
- [[Fluent 仿真报告]]
- [[Fluent 参数化研究]]
- [[Fluent 设计分析与优化]]
- [[Fluent System Coupling]]
- [[Fluent 任务页参考]]

## 尚未处理

- Part I：Chapter 1–4 已完成；p. 219 Glossary 尚未摄取。
- Part II：全部完成（Chapter 1–7 与 Appendix A–C 及 Bibliography，pp. 223–908）。
- Part III：扉页导航与 Ch.1–50 已完成（pp. 909–4888）；Ch.51 Task Page Reference Guide 章内进行中（pp. 4889–4902 已摄取，4903 起 51.4）。
- Part IV：Web Interface。

### 批次 24：Part II / Chapter 7 完成（PDF pp. 838–868）

- [[Fluent 高级网格主题]]：补齐 7.14 Rapid Octree Meshes（内部/外部体域定义、Boundary Projection/Cartesian Snapping、分辨率与网格过渡、局部/自定义尺寸、边界层网格和限制）。
- 复核目录地图：Chapter 7 实际止于 p. 868；p. 869 起是 Appendix A。纠正此前将本章范围误记为 pp. 605–916 的检查点。
- Chapter 7 全章 pp. 605–868 已完成，本轮五章任务 Chapters 3–7 完成 5/5。后续目录项 Appendix A 从 p. 869 起。

### 批次 25：Part II / Appendix A 完成（PDF pp. 869–876）

- [[Fluent 第三方网格导入与 fe2ram 过滤器]]：GAMBIT 与 ICEM CFD TetraMesher（RAMPANT）；`utility fe2ram` 命令行（dimension/read-format/merge/zoning/write-format；输出不得为 CFF；VRML 1.0）；I-deas Universal、PATRAN Neutral、ANSYS（STIF63、隐式 ID 顺序编号）、ARIES（须经 Prep7 中转的六项条件）、NASTRAN 的识别数据集与分组/周期/重复节点要求；所有导入边界 zone 一律视为 wall。
- Appendix A 目录范围 pp. 869–876 至此完成；p. 876 为版权页脚，无正文。本批文本提取无表格错位，未触发额外视觉核对。下一目录项 Appendix B 从 p. 877 起。

### 批次 26：Part II / Appendix B 完成（PDF pp. 877–892）

- [[Fluent 网格文件格式（legacy .msh）]]：节结构与类型索引（Comment 0/Header 1/Dimensions 2/Nodes 10/Edges 11/Cells 12/Faces 13/Periodic Shadow Faces 18/Cell Tree 58/Face Tree 59/Interface Face Parents 61）、二进制前缀 20（单精度）/30（双精度）与 End of Binary Section 约定、声明节（zone-id=0）与右手法则、bc-type/element-type/face-type 全表（非一致相交面 bc-type+1000）、hanging-node 树节可读性差异（59 可读、58 不可读）、Zone 节 39/45 差异与十进制 zone-id、zone-type 枚举、Scheme 符号命名规则、三个完整 2D 示例。
- Appendix B 目录范围 pp. 877–892 至此完成。下一目录项 Appendix C 从 p. 893 起。

### 批次 27–32：其他会话完成（2026-10-16；2026-10-17 批次 33 会话补录簿记）

- 用户指定自 Appendix C 起按目录连续摄取 10 个条目。有项目页记录的：批次 27 = ①Part II Appendix C（pp. 893–906，[[Fluent 快捷键与实体信息]]）+ ②Bibliography（pp. 907–908，Part II 参考文献 22 条，见 [[Part II - Meshing Mode]]）；批次 28 = ③Part III 扉页与 Using This Manual（pp. 909–916，[[Fluent 手册排版与数学约定]]），见 [[Part III - Solution Mode]]。
- 完成可由检查点与知识页佐证、但当时未留日志/来源页批次记录的：④Ch.1 GUI（pp. 917–962，[[Fluent 求解模式 GUI]]）、⑤+⑥Ch.2 TUI 与 Ch.3 Reading and Writing Files（pp. 963–1054，[[Fluent 求解模式文件读写]]）、⑦Ch.4 Unit Systems（pp. 1055–1058，[[Fluent 单位制]]）、⑧Ch.5 Fluent Expressions Language（pp. 1059–1154，[[Fluent 表达式语言]]）。④–⑧ 具体批次号不可考（按顺序推定为 29–32）；批次 33 会话仅补记簿记，未重读其对应 PDF 正文。

### 批次 33：Part III / Ch.6 Model Topology 完成（PDF pp. 1155–1168）

- 核对来源身份（SHA-256 一致）后按检查点续接并登记批次 33；发现 ⑨ 的知识页 [[Fluent 模型拓扑（Model Topology）]] 已由先前会话建好但未回写任何簿记。本批次以 pypdf layout 模式提取全章 14 页逐节比对核验该页，全部主张与原文相符。
- 据原文两处小幅修订：标注 6.1.2（p. 1157–1158）"创建新体积时界面自动定义"与 6.5（p. 1168）"New Volume 不自动创建任何界面"的手册内部表述张力（操作口径以 6.5 为准）；将 6.4.2 Important 的失效结果精确为"变更过的 physics volumes/boundaries 上评估的结果"。
- 补记批次 27–32 缺失簿记，并同步 Part II/Part III 项目页与索引。Ch.6 目录范围 pp. 1155–1168 至此完成；下一目录项 Ch.7 从 p. 1169 起。

### 批次 34：Part III / Ch.7 章内第 1 段——7.1–7.3（PDF pp. 1169–1201）

- 10 条目连续任务最后一项 ⑩（Ch.7，全章 pp. 1169–1346）按小节分段推进；本批完成 7.1 Mesh Topologies、7.2 Mesh Requirements and Considerations、7.3 Mesh Sources。
- 新建知识页 [[Fluent 网格读取与操作]]：接受单元类型与悬挂节点默认转多面体（`file/convert-hanging-nodes-during-read? no` 及其 interior wall 报错三情形）；七种单元 face-node 连接表（3D poly 无显式编号）；选型三考量（setup time/计算开销/数值扩散）与四档推荐组合；正交性双点积定义、正交质量按单元类型（tet/prism/pyramid 取 min(orthogonality, 1−skewness)）、增强定义开关、长宽比定义；手册阈值（正交质量 > 0.01、tri/tet 偏斜度 < 0.95、通道 ≥ 5 单元）与 Eq 7.3 层流壁面间距式；网格来源清单、NASTRAN 三路径与识别 Bulk Data、CFX 分区两法与保留边界类型、fe2ram 概要、多文件读取三法（solution append/meshing 合并/tmerge，tmerge 不支持 CFF）、悬挂节点转换产物的动网格/自适应限制、表面网格读入。
- 提取缺口核验：Eq 7.3 公式体与 p. 1193 "constant z plane" 的坐标符号经 fitz 500 dpi 渲染视觉核对；Figures 7.1–7.25 为图形元素未摄取。7.3 与 Part II Appendix A 高度重叠处（fe2ram/格式细节）作交叉引用未重复展开。
- 下一续接位置：同章 7.4 Reference Frames，从 p. 1202 开始；其后 7.5（1206）、7.6（1212）、7.7（1250）、7.8（1279）、7.9（1290）、7.10（1296）、7.11–7.12（章尾，页码届时按目录地图核对）。

### 批次 35：Part III / Ch.7 章内第 2 段——7.4–7.6（PDF pp. 1202–1249）

- 续接批次 34 同章分段推进（约 48 页）：7.4 Reference Frames、7.5 Curvilinear Coordinate Systems、7.6 Non-Conformal Meshes（至 7.7 起始页 p. 1250 前）。
- 扩充 [[Fluent 网格读取与操作]]：参考帧（User Defined/Track by Zone、Constant Velocity/Motion Definition、OK 即重定义帧的告诫、可用于 point surface/profile/injection/motion definition）；CCS（Direction 0/1 必填、Direction 2 叉积、Diffusion/Base Vector/Vector Projection 三法与线圈示例、多孔区禁变形、Jump boundary 仅限闭环且每环一个）；NCI（交线生面通量计算、六选项及限制——one-to-one 仅支持 Coupled Wall、Mapped 不支持密度基/DPM/动网格/shell conduction、Static 误用即错误结果；三种算法沿革与左手面处置；命名规则全集；要求与限制清单含容差≤相邻单元尺寸、many-to-many NCI 面不参与后处理、3D fan zone 禁 NCI；7.6.4 十四步使用流程含 auto-options 全套 TUI、over-intersected 指标（面交叠 > 面积×1.25）、Interface Overlap Fraction 云图复查、delete-interfaces-with-small-overlap；运动传递 transfer-displacements/project-nodes 两法与 (recreate-sliding-interfaces) 迁移命令；多对多/一对一手动创建差异）。
- 本批开头 p. 1202 为 7.3.14 的收尾步骤（PUMA/hanging node 两法的自适应设置入口），已并入知识页 7.3 节。提取无表格/公式缺口，未触发渲染核对；Figures 7.26–7.54 为图形元素。
- 下一续接位置：同章 7.7 Overset Meshes，从 p. 1250 开始；其后 7.8（1279）、7.9（1290）、7.10（1296）、7.11–7.12 至章尾 p. 1346。

### 批次 36：Part III / Ch.7 章内第 3 段——7.7 Overset Meshes（PDF pp. 1250–1278）

- 续接同章分段（29 页）：7.7 全部十个小节（7.7.1–7.7.10）。p. 1250 顶部为 7.6.4.3 收尾注记（大位移时被动侧启用网格更新方法），已并入知识页 7.6 节。
- 扩充 [[Fluent 网格读取与操作]]：Overset 概念与四类单元（dead/solve/receptor/donor）、background/component 规则（一个 zone 只属一个接口、物理边界不得相交但可重叠、collar mesh 化解相交、cut control）；域连接三步（hole cutting 及 cut control/collar 命令、overlap minimization 与 donor 优先级两法/grid priorities、donor search 至少 4 单元重叠）；诊断（seed 误入流体区、重叠边界泄漏容差一单元、orphan 成因与"细化 donor 侧而非 orphan 侧"）；自适应（orphan/size/gap 三种标记、5 cycle×2 sweep、手动与自动差异、全部控制项与默认值）；最佳实践（Coupled 压速耦合、双精度、闭域不可压不支持、时间步长准则、插值法选择与多孔注意项）；限制与兼容性清单（不支持 FMG/FAS/隐式残差光顺、SRS 不兼容、DPM 限制、边界条件排除清单、源项/fixed values 限制、多孔仅 superficial velocity）；设置步骤（overset 边界必须在建接口前改完）与后处理（Overset Cell Type 整数值表、mark-cells/display-cells/list、体积/面积分重复计数误差随重叠增大）。
- 提取缺口核验：尺寸自适应判据符号（V_d/V_r > R_l³（3D）/R_l²（2D），默认 R_l=3）与湍流/转捩模型名（k-ε、k-ω、Transition k-kl-ω）经 fitz 500 dpi 渲染视觉核对。发现手册 p. 1269 verbosity 命令印作 `overset-interface`（单数）与其余处不一致，按原文照录待核。Figures 7.55–7.76 为图形元素。
- 下一续接位置：同章 7.8 Controlling Flow in Narrow Gaps for Valves and Pumps，从 p. 1279 开始。

### 批次 37：Part III / Ch.7 章内第 4 段——7.8–7.9（PDF pp. 1279–1295）

- 续接同章分段（17 页）：p. 1279 顶部为 7.7.10 Overset 文件读写（CFF 保存域连接、无需重建、update-before-case-write 开关），已并入知识页 7.7 节；正文为 7.8 Controlling Flow in Narrow Gaps（Gap Model）与 7.9 Checking the Mesh。
- 扩充 [[Fluent 网格读取与操作]]：Gap Model（flow-blocking/flow-modeling 两型机制与优点；长清单限制——密度基/SRS 类湍流/DPM/多相多数/NITA 等；边界条件与材料可压性建议、CFL=1 自适应时间步等收敛建议；Gap Model 对话框全流程：face zone 选取规则、proximity threshold、Gap Reynolds Number、Sponge Layer 的 Fictitious/Real Viscosity、UDF 源项、Exclude Cell Zones（overset 不兼容）、Stabilization Level 全局覆盖、sponge-layer 细化参数、专家命令组、Gap ID/Gap Type/Flow-Blocking Gap Interface 场变量、稳态改动须重初始化、gap 重叠告诫）；网格检查（检查项全集、四类退化、负体积/零面积的定位与处理、check-verbosity 0–3）与修复（Report Poor Quality Elements、solver 变量 1–6 及默认/推荐值、Repair 按钮能力与边界节点开关、多面体转换开关、improve-quality）。
- 提取缺口核验：Eq 7.4 公式体（Re_gap = ρ_avg·u_avg·L / μ_avg）经 fitz 500 dpi 渲染核对；p. 1290/1292 轴对称坐标轴符号按 7.2.1 明确陈述与报告样例互证为 x/y/z。Figures 7.77–7.83 为图形元素。
- 下一续接位置：同章 7.10 Reporting Mesh Statistics，从 p. 1296 开始；其后 7.11–7.12 至章尾 p. 1346。

### 批次 38：Part III / Ch.7 章内第 5 段（末段）——7.10–7.12（PDF pp. 1296–1346），Ch.7 全章完成

- 五批连续任务第 3 批，Ch.7 最后一段（51 页）：7.10 统计报告、7.11 多面体转换、7.12 网格修改（22 项操作）。p. 1296 顶部为 7.9.2 修复收尾（repair-face-node-order/repair-face-handedness/repair-periodic），已并入知识页 7.9 节。**至此 10 条目连续任务全部完成（10/10）**。
- 扩充 [[Fluent 网格读取与操作]]：统计报告四命令（Size/Memory/Zone/Partitions，Linux 与 Windows 内存定义、进程名）；多面体转换三路径（全域 dual 聚合与边界层/hex 处理规则、preserve-interior-zones、并行分区不自动迁移、偏斜单元局部转换算法、悬挂节点转换；poly 公共限制）；网格修改 22 项（合并、分离四法/两法与 32 区上限、断开、融合（部分融合不支持、容差 ≤0.5、自适应网格限串行 PUMA）、周期区创建六步与解耦、slit 与 disconnect/separate 的区别及散热器出口改 mass-flow-inlet 用例、定向、挤出（仅 3D 串行）、投影、替换 zone（BC 按名转移、overset 须关插值、限 legacy 文件）/删除/停用（含界面 zone 须先初始化）/激活、复制 zone（周期边界先 slit）、替换整网（跨区插值不保守恒、Scheme 分区开关、限 legacy 且缩放须一致）、邻接改名（通配符规则）、RCM 重排、缩放（先于视角因子/初始化，Unscale 语义）、平移/旋转（保形连接区不可单独动）、光顺与换面（仅 quality-based 受推荐、并行限制、阈值组合流程）、边界层重分布、删除/提取单元（overset 与 shell conduction 不支持、不可撤销））。
- 提取缺口：7.12 平移/旋转/缩放小节的坐标轴符号（x/y/z）丢失，按上下文与 7.2.1 约定、p. 1291 报告样例互证补全，未逐处渲染。Figures 7.84–7.111 为图形元素。
- 下一续接位置：Part III / Ch.8 Cell Zone and Boundary Conditions，从 p. 1347 开始。

### 批次 39：Part III / Ch.8 第 1 段——8.1 Overview（PDF pp. 1347–1369）

- 五批连续任务第 4 批，Ch.8 起始段（23 页）：8.1.1–8.1.11 全部（8.1.12 Saving and Reusing 自 p. 1370 起，留批次 40）。
- 新建知识页 [[Fluent Cell Zone 与边界条件设置]]：zone 类型四大类清单（Table 8.1：External/Internal/Periodic/Cells）；任务页与树双入口；改类型规则（同类别内互换、默认名自动改名、wall/shadow 对一次性转换、periodic 除外、多相差异另见 p. 3070）；设置与 TUI 批量语法（`define/boundary-conditions/set/<type>` 括号列表与通配符、q 退出后设置才生效）；复制条件（全部条件、外部/内部 wall 求能量方程时不可互拷）；Turbo CSV 导出（Add Global Node Number 与 System Coupling 共享节点识别）；改名（非默认名改类型时保留）；非均匀分布（profile/UDF）；参数体系（输入/输出参数、New Input Parameter、表达式须为带单位常数且不可引用其他表达式、单位变更影响参数值、默认名不复用、Scheme 过程挂接 args->string 规则与单行限制、UDF 的 RP_Get_Input_Parameter 宏、TUI advance/use-in）；图形选区与操作条件入口。
- 本批无表格/公式提取缺口，未触发渲染核对；Figures 8.1–8.10 为图形元素。
- 下一续接位置：同章 8.1.12 与 8.2 Cell Zone Conditions，从 p. 1370 开始。

### 批次 40：Part III / Ch.8 第 2 段——8.1.12 + 8.2.1–8.2.3（PDF pp. 1370–1422）

- 五批连续任务第 5 批（收官），53 页：8.1.12 保存/复用 BC（指向 p. 991）与 8.2 的 Fluid、Solid、Porous Media 三节全内容（8.2.4 3D Fan Zones 自 p. 1423 起留待后续）。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：Fluid（唯一必填材料、多相/组分差异、Laminar Zone 默认置零 μt 且关生成项及 define/boundary-conditions/fluid 保留 μt 的开关、除 LES 外可用、旋转轴规则与同轴告诫、MRF/滑移运动与 Relative To Cell Zone、Copy To Mesh Motion/Frame Motion 切换）；Solid（纯固体域应手动去激活流动方程、Frame/Solid/Mesh Motion 三选项与适用条件、Boundary Advection、速度须无散（与边界相切）及其唯一例外、同时平移+旋转须同轴同向、convert-all-solid-mrf-to-solid-motion、限制三条）；多孔介质全节（动量汇本质与限制假设清单、表观/物理速度公式及其切换注意、Standard Initialization 推荐与 Hybrid 限制、NETM 的 dual cell 机制与不兼容清单、动量源两部分与 Darcy/惯性/幂律、相对黏度三子模型、能量平衡/非平衡两模型、湍流默认照算与 Laminar Zone 抑制、porosity 对瞬态项的作用、14 步用户输入、阻力系数定义（方向向量自动确定与正交化告诫、plane/line tool、圆锥/圆柱与曲线坐标系、惯性系数单位为长度倒数、Alternative Formulation 仅压力基且切换须重跑）、系数推导四法与实验数据拟合法（避免负系数）、porosity 0–1 且 NETM 禁 0/1、NETM 设置流程（先 Apply 再启用、自动建固体区的边界转换规则、网格细化须相近、低 porosity 瞬态建议 Solid Time Step ~1s）、相对黏度"最后输入值作用于全部多孔区"陷阱、相对渗透率 Corey 模型与表格法及残余饱和度 fix 命令、毛细压力五模型与 Maximum Capillary Pressure 限幅及作扩散的替代法、能量源不按 porosity 折算、求解策略（压降初场最佳、各向异性限 2–3 个数量级、2022R1+ 非一维/非一致界面收敛问题与 presto-dissipation Scheme 变通））。
- 提取边界：Eq 8.1–8.55 公式体多为图形对象未提取，知识页按公式周边文字记录结构与式号、未凭空补写（k_eff 体积平均、v_sup=γv 等文字明确处除外）；坐标轴符号按 7.2.1 约定补全；Figures 8.11–8.28 为图形元素。
- 下一续接位置：同章 8.2.4 3D Fan Zones，从 p. 1423 开始。

### 批次 41：Part III / Ch.8 第 3 段——8.2.4–8.3（PDF pp. 1423–1442）

- 五批连续任务（批次 41–45）第 1 批，20 页：8.2.3.9 尾注与 8.2.3.10 多孔后处理（收尾）、8.2.4 3D Fan Zones、8.2.5 固定变量值、8.2.6 锁定固体/壳温度、8.2.7 源项、8.3 操作条件（浮力驱动流 8.3.1.1–8.3.1.6）。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：3D Fan（环形流体体积分布动量源 vs fan 边界、三方向源与拐点比、风机曲线缩放、几何/属性输入全流程、轴向源 constant/fan curve 两法、限制三条——不支持预混燃烧与 Eulerian 多相、fan curve 须开能量方程）；固定值（被固定单元不解方程不计残差、仅压力基可固定温度/组分/速度、全部速度分量固定则表压置零、径向 profile 坐标系、雷诺应力不能径向 profile）；温度锁定（与固定值的区别：方程仍解、仍计残差；BCGSTAB 不兼容）；源项（须单独成区、质量源须配套其他源且能量源自动按参考温度 0K/298.15K 补、末组分 = 总量减其余、P-1 源须配等量反号能量源、按单位体积折算）；操作条件（封闭域瞬态 vs Boussinesq、Boussinesq 限制、操作密度显式指定建议与可压气体填 0、PRESTO! 推荐、高 Rayleigh 数部分层流无稳态解）。
- 提取边界：Eq 8.56–8.69 公式体未提取，按周边文字记录结构与式号；湍流源单位串部分残缺按上下文可辨；Figures 8.29–8.33 为图形元素。
- 下一续接位置：同章 8.4 Boundary Conditions，从 p. 1443 开始（8.4 大节 130 页将分三批：8.4.1–8.4.9 / 8.4.10–8.4.15 / 8.4.16–8.4.22）。

### 批次 42：Part III / Ch.8 第 4 段——8.4 开头与 8.4.1–8.4.9（PDF pp. 1443–1494）

- 五批连续任务（批次 41–45）第 2 批，52 页：8.3.1.6.1 高 Rayleigh 数策略（8.3 收尾）、8.4 引导与分组、8.4.1–8.4.2 十二类进出口总览与入口湍流参数确定法（profile/均匀值、强度/长度尺度/黏度比定义与换算关系、SRS 入口脉动速度）、8.4.3 压力入口、8.4.4 速度入口、8.4.5 质量流入口、8.4.6 质量流出口（含 Exit Corrected Mass Flow Rate）、8.4.7 进口通风口、8.4.8 吸气风扇、8.4.9 压力出口（含径向平衡、平均压力规格 Strong/Weak、压力 profile 乘子、回流条件、Prevent Reverse Flow、Target Mass Flow Rate）。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：12 类进出口适用场景速查；湍流入口参数通用参考（各模型 specification method、I/ℓ/μt/μ 的定义、经验值与默认值、换算关系 8.74–8.82、参考系告诫、SRS 脉动速度）；多类入口共享要点（Supersonic/Initial Gauge Pressure 语义、静水压处理、方向向量与圆柱坐标系正方向、Local Cylindrical Swirl 禁忌、温度语义按相/可压性、Prevent Reverse Flow）；七类边界各自的输入清单、默认值与计算程序（含 choked 可压内流告诫、轴对称 2π/1 弧度惯例、Average Mass Flux 语义、混合面联动、ECMF 机制、径向平衡 bins、Strong/Weak Averaging、目标质量流限制与设置）。
- 提取边界：Eq 8.70–8.107 公式体未提取按周边文字记录（k=(3/2)(ūI)²、ECMF、dp/dr、Δp=K·½ρv_n²、α 混合语义等文字明确处除外）；ℓ–δ 换算、自由流 μt/μ 通常取值等个别数值缺失按上下文定性记录；Figures 8.34–8.44 为图形元素。
- 下一续接位置：同章 8.4.10 Pressure Far-Field Boundary Conditions，从 p. 1495 开始。

### 批次 45：Part III / Ch.8 第 7 段——8.5–8.8（PDF pp. 1573–1615）

- 五批连续任务（批次 41–45）第 5 批（收官），43 页：8.4.22 补遗（internal face 属性、solar 半透明、后处理指向）、8.5 Multi Edit 批量编辑、8.6 瞬态边界条件（标准/表格瞬态 profile 格式与 SI/小写/周期闭合规则、运动网格 profile 变量名）、8.7 边界声学波模型（turbo-specific NRBC、general NRBC、阻抗 IBC、transparent flow forcing 四类的适用/限制/机制/用法全览，含 sigma/sigma2、LRM、极点-留数近似与无源性约束、impedance 工具、CFL 最佳实践）、8.8 用户自定义风机模型（周期性重生成 profile 的外部可执行流程、fantest.f 示例、(update-user-fans) 初始化）。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：Multi Edit 图标语义与单面/耦合墙不可混选；瞬态 profile 三格式与命名规则；NRBC 四模型对照（求解器/流动/几何限制、Backflow Direction 选法、CFL 2.0/4.0 与先稳后开、sigma 0.15 / sigma2 5.0、混合面回流禁用、并行单分区要求）；IBC 的反射系数近似与 |R0|<1 无源性、cell acoustic CFL<1、连续性判据 1e-4、impedance 工具全参数；TFF 的入射波强 profile 机制；用户自定义风机的三参数与示例程序要点。
- 提取边界：Eq 8.153–8.214 公式体未提取按周边文字记录（文字明确处除外）；turbo NRBC 欠松弛默认值、TFF 波强式等数值/公式未提取；瞬态 profile、阻抗数据与 fantest.f 示例照录；Figures 8.82–8.95 为图形元素。
- 下一续接位置：同章 8.9 Profiles，从 p. 1616 开始；8.9–8.11 至章尾 p. 1650。

### 批次 46：Part III / Ch.8 第 8 段（末段）——8.9–8.11（PDF pp. 1616–1649），Ch.8 全章完成

- 十批连续任务（批次 46–55）第 1 批，34 页（p. 1650 为空白版权页）：8.9 Profiles（六类型与插值、标准/CSV 两种格式全规则、使用流程与三种点插值法、检查删除/查看/重定向/复制含复数模态）、8.10 GT-POWER 耦合（要求限制、用户输入、转矩-转速耦合）、8.11 WAVE 耦合。**Ch.8 全章（pp. 1347–1649）完成。**
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：六种 profile 类型（point/line/mesh/radial/axial/transient）与各自插值方式、轴确定规则；标准格式（≤64 字符全小写、SI、必含坐标字段）与 CSV 格式（节标识符、字段标签表、逗号分隔、SI 与单位规则、保留 X 轴标签）；三种点插值（Constant 默认/Inverse Distance/Least Squares SVD）及其 cell zone 不适用与容差回退；删除/替换 profile 的正确顺序；Orient 重定向（Euler 角旋转矩阵 + 平移向量）与 Replicate 复制（Full 360 deg.、扇区计数、Autofill、复数模态 harmonic index 与 Complex Pair 单对限制）；GT-POWER/WAVE 耦合的边界类型/20 区上限/面积 5% 校核/Mass Flux 要求/组分对应 Chemical Formula/50 组分上限、k-ε 自定义建议、WAVE 五组分 F1–F5 与同步保存间隔、转矩-转速耦合（GT-POWER v2017.2+、墙名=叶轮机名）。
- 提取边界：Eq 8.215–8.224 公式体未提取按周边文字记录（8.224 转速式按变量定义导出）；Figures 8.96–8.111 为图形元素；CSV/阻抗等示例照录（批次 45 已录）。
- 下一续接位置：Part III / Ch.9 Physical Properties，从 p. 1651 开始。

### 批次 55：Part III / Ch.14 第 2 段——14.6.2.2–14.6.2.5（PDF pp. 1901–1931）

- 十批连续任务（批次 46–55）第 10 批（收官），31 页：14.6.2.2 动态层化（Height/Ratio Based 分裂与 collapse 合并、适用条件、滑移界面过渡）、14.6.2.3 重划（Unified 默认与 Methods-Based 五法——local cell/local face/zone/face region/2.5D、尺寸函数标记机制与 Variation/Rate/Resolution、棱柱层体积分解建议、sizing controls 与 prism controls 全参数、各法与 adaption/光顺兼容性）、14.6.2.4 体积网格更新程序（自动选法、并行微差、shell conduction 耗时）、14.6.2.5 瞬态考量（重划事件回退一阶、verbosity 监控、网格交换触发）。
- 扩充 [[Fluent 滑移与动网格]]；14.6.2.1 边界层光顺补遗（平移为主、仅兼容弹簧光顺、不必分区）。
- 提取边界：Eq 14.15–14.24 公式体未提取按周边文字记录（层化阈值/尺寸函数参数语义明确处除外）；Figures 14.30–14.50 为图形元素。
- 下一续接位置：同章 14.6.3 Feature Detection，从 p. 1932 开始（14.6.3–14.6.11 至章尾 p. 1992，待后续批次）。

### 批次 56：Part III / Ch.14 第 3 段（末段）——14.6.3–14.6.11（PDF pp. 1932–1992），Ch.14 全章完成

- 十批连续任务（批次 56–65）第 1 批，61 页：14.6.3 特征检测（Feature Angle 0–180°，特征重划仅 face region remeshing 可用）、14.6.4 In-Cylinder 全节（曲轴角设置与默认 0.5° 步长、piston-full/piston-limit 与 Eq 14.25–14.27、缸内输出 8 列、网格拓扑三区划分、阀 profile angle/lift 字段、最小阀升程与滑移界面转换实现关阀）、14.6.5 Six DOF（属性组必填 Mass+惯量张量、One DOF 平移/转动、Hooke 弹簧、Constrained 限位）、14.6.6 隐式更新（Update Interval/Motion Relaxation/Residual Criteria；密度基 Explicit、稳态、In-Cylinder 禁用）、14.6.7 接触检测（Contact Zones 多孔区法 vs Contact Marks 零质量流法、限制与稳定化、Update Contact Marks）、14.6.8 动网格事件（20 种事件类型全列、缸内周期执行条件 Eq 14.30）、14.6.9 动区运动指定（Stationary/Rigid Body/Deforming/User-Defined/System Coupling/Intrinsic FSI 六类流程、各型边界条件默认行为差异、解稳定化 volume/coefficient-based、刚体运动学 Eq 14.34–14.39）、14.6.10 预览（Zone Motion 仅图形 / Mesh Motion 实改网格须先存 case）、14.6.11 稳态动网格（CG_MOTION UDF、dtime 默认 1、In-Cylinder/Implicit Update/Events 不可用）。
- 扩充 [[Fluent 滑移与动网格]] 至全章完成；恢复被插入覆盖的"证据与适用条件"标题；补记来源页关联页面缺漏的四个知识页链接（基本流动建模/运动参考系/运动定义与辅助几何/滑移与动网格）。
- 提取边界：Eq 14.25–14.39 公式体未提取按周边文字记录；Figures 14.51–14.96 为图形元素。
- 下一续接位置：Part III / Ch.15 Modeling Turbomachinery Flows 段 1（15.1–15.3），从 p. 1993 开始。

### 批次 57：Part III / Ch.15 第 1 段——15.1–15.3（PDF pp. 1993–2035）

- 十批连续任务（批次 56–65）第 2 批，43 页：15.1 Turbo Setup 引导工作流全 11 任务（部件描述/行范围/网格导入关联映射/CFD 模型/物理/区域与区合并/拓扑/iso 面/报告监视器/任务编辑规则/.wft 保存与偏好）、15.2 Frozen Gust/入口扰动（尾迹 profile 单排化两构型五步流程）、15.3 叶排干涉（GTI 三类 pitch-change：Pitch-Scale 节距比 < 2 / No Pitch-Scale 任意比与虚拟副本 / Mixing-Plane 周向平均 40 带；FR/TRS 由 zone motion 隐式判定；ensemble 整数节距比才可 TRS；Interface Check 六项；legacy 混合面设置与三守恒选项）。
- 新建知识页 [[Fluent 叶轮机械流动]]。
- 提取边界：Eq 15.1（legacy 欠松弛）公式体未提取按语义记录；Figures 15.1–15.8 为图形元素；表 15.1 为正文数值。
- 下一续接位置：同章 15.4 Aerodynamic Damping，从 p. 2036 开始。

### 批次 58：Part III / Ch.15 第 2 段——15.4–15.5（PDF pp. 2036–2076）

- 十批连续任务（批次 56–65）第 3 批，41 页：15.3.4.3 混合面求解策略（倒流处置、Area→Mass/Mixed-Out 切换、欠松弛）；15.4 气动阻尼/叶片颤振（共同六步设置、振型 .csv profile 格式与 Passage number、Mesh Motion 局部参考系要求、Run Calculation 频率基准推进、Periodic Displacement 与 Fast Mesh Smoothing、Amplitude 0.05% 弦长/Scaling 0.5、三类动网格区配置、TWM——IBPA = 节距 × 节径、能量法 Eq 15.2 正阻尼/负激发、每节径 FTW+BTW 两仿真、三构型、谐波导出 .csv 供 FEM、Aerodamping TWM 报告、Wall Work/Power Density；ICM——一次运行覆盖全节径、仅中间叶片振动叠加原理、仅实振型且叶数须奇数、Aerodamping ICM 与 Generalized/Modal Force 报告）；15.5 相位滞后法（时间 Fourier 分解避免整周期存储、三类场景、官方仅 k-ε/k-ω/SST/Wet Steam、tip-gap 须保形、界面创建两法与命令、谱描述 NumberSectors360 自动/手动命令、初始化两工作流、双精度建议）。
- 扩充 [[Fluent 叶轮机械流动]]；记录手册原文两处瑕疵（p. 2070 标题跨章残留编号 "21.2.3.6"、turbo-mode 命令路径疑误）。
- 提取边界：Eq 15.2–15.13 公式体未提取按周边文字记录；Figures 15.9–15.16 为图形元素。
- 下一续接位置：同章 15.6 Non-equilibrium Wet Steam Model，从 p. 2077 开始。

### 批次 59：Part III / Ch.15 第 3 段（末段）——15.6–15.10（PDF pp. 2077–2124），Ch.15 全章完成

- 十批连续任务（批次 56–65）第 4 批，48 页：15.6 湿蒸汽模型（两求解器 + phase-lag 支持）；15.7 叶片气膜冷却全节（Boundary Interface 虚拟孔——.csv 孔心 profile 与参考系语义、四类 BC 型、孔向/流向/孔形规格、radial-distribution 温度分布与焓通量守恒、Loss Coefficient factor-and-length-ratio、overlap/non-overlap 区生成、周期对孔位自动旋转、五条限制含瞬态转子孔位陷阱）；15.8 叶轮机械描述（create/list/delete 命令、路径 turbo-models/turbo-model 不一致记录）；15.9 TSN（压力基定常 + 伪时间 Global Time Step、HOTR Convection Only 0.1、Limiter Filter、动量显式欠松弛 0.5→0.1 备选）；15.10 后处理全节（拓扑八类边界与封闭域要求、零角线、七个专属变量、Turbo surface 与 Periodic Instancing、通用 Fourier 系数——移动平均与公共周期、两类场景、谱内容两创建法、图形谱欠松弛默认 1.0 与多行频率选择三算法、周向平均 profile、Turbo Report 十余量与效率式 15.19–15.44 语义、平均云图/2D 云图/平均 XY 图、Turbo Performance 命名表达式 EfficiencyIsentropic/Polytropic、MassFlowAveAbs 比值方向、/report/efficiency/use-in-turbo-report 切换）。
- 扩充 [[Fluent 叶轮机械流动]] 至全章完成；补记 15.5.3.4 第三种初始化流程与 phase-lag 后开定常 .dat 报错的 Important。
- 提取边界：Eq 15.14–15.44 公式体未提取按周边文字记录；Figures 15.17–15.39 为图形元素。
- 下一续接位置：Part III / Ch.16 Modeling Turbulence 段 1（16.1–16.9），从 p. 2125 开始。

### 批次 60：Part III / Ch.16 第 1 段——16.1–16.9（PDF pp. 2125–2166）

- 十批连续任务（批次 56–65）第 5 批，42 页：16.1 引言与全模型清单（RANS/SRS 两条路线）；16.2 选型指南全节（默认 k-ω SST 与 Preferences 改默认；SA/k-ε/k-ω/GEKO/RSM/转捩四模型逐个定位；GEKO 四系数 Csep/Cnw/Cmix/Cjet 语义与 2024 版默认；曲率/角隅/生成限制器/Sarkar/浮力增强项取舍；壁面处理与网格分辨率要求；LES/WMLES/混合模型 SAS-DES-DDES-IDDES-SDES-SBES-ELES 原理与层级建议；SRS 网格（LES 缩放、WMLES δ 缩放、octree 5×5×5、剪切层 10–20 单元）与数值设置（CFL~1、BCD 首选、NITA/SIMPLEC/PISO/耦合、连续性每步 2 量级、Extrapolate 省 40%））；16.3 使用步骤（Viscous Model 对话框、近壁处理清单、LES 近壁三选）；16.4 SA 选项；16.5 k-ε（Standard/Realizable/RNG 选项）；16.6 k-ω（Standard/GEKO 含 TUI 全菜单/BSL/SST/WJ-BSL-EARSM）；16.7–16.9 转捩模型设置（k-kl-ω、Transition SST 含 DEFINE_TRANS 关联 UDF、Intermittency/Alg-γ 的挂接范围）。
- 新建知识页 [[Fluent 湍流模型设置]]；记录提取文本希腊字母系统性丢失的处理方式（按标准名补全、TUI 核实系数名）。
- 提取边界：Eq 16.1–16.3 公式体未提取按语义记录；Figures 16.1–16.17 为图形元素。
- 下一续接位置：同章 16.10 Setting Up the Reynolds Stress Model，从 p. 2167 开始。

### 批次 61：Part III / Ch.16 第 2 段（末段）——16.10–16.20（PDF pp. 2167–2220），Ch.16 全章完成

- 十批连续任务（批次 56–65）第 6 批，54 页：16.9 尾段（Alg-γ/γ 转捩选项与自定义临界雷诺数关联式、Include Crossflow Transition）；16.10 RSM（ε 基/ω 基两组子模型、墙反射项标定范围告警）；16.11 SAS 组合方式；16.12 DES 五种底层模型设置（Cdes 0.65/0.61、屏蔽函数 F1/F2/DDES/IDDES）；16.13 LES（五个亚格子模型、WALE 默认、动态选项、Near Wall RANS Layer、近壁三处理）；16.14 模型常数；16.15 ELES 全流程（SA 不兼容、冻结/被动模式、rans-les-interface、涡数 ≥ 面数 1/4、无倒流要求）；16.16 通用选项 27 小节（浮力三档、曲率/角隅修正系数、两种生成限制器、RNG 专属、湍流阻尼因子 10、SBES 挂接与 Update Interval k-omega 最优 5）；16.17 湍流边界条件（粗糙壁不可用清单、层流区置零、RSM 各向同性/直接分量两法）；16.18 初值估算（I 1–10%、TVR 1–100）；16.19 求解策略（RSM 先 k-ε 后切换、LES 五步含 init-turb-vel-fluctuations 与统计清零）；16.20 后处理变量清单（各模型专属量、ELES 双涡黏注意、统计后处理与壁面均值告警、排错三查）。
- 扩充 [[Fluent 湍流模型设置]] 至全章完成；经 LES 设置节核实补全批次 60 存疑的 WMLES ω 基变体名为 WMLES S-Omega。
- 提取边界：Eq 16.4–16.8 公式体未提取按语义记录；Figures 16.18–16.36 为图形元素。
- 下一续接位置：Part III / Ch.17 Modeling Thermal Energy 段 1（17.1–17.3.5），从 p. 2221 开始。

### 批次 62：Part III / Ch.17 第 1 段——17.1–17.3.6（PDF pp. 2221–2276）

- 十批连续任务（批次 56–65）第 7 批，56 页：17.2 导热对流全节（能量方程开启、viscous work、温度限 5000 K/1 K、双隔离流体区告诫、能量欠松弛 0.8–1.0、焓参考温度 298.15 K、分步求解；CHT 专节——固体时间步整倍数要求与自动估算、Loosely Coupled CHT 两耦合方法与七条限制、时间平均显式热耦合 Moving Average、各向异性固体三热流法与 local-neighbors 提速 2–3 倍；换热量后处理含 custom-heat-flux 导出格式；shell conduction 七小节——物理处理/13 条限制/Conduction Manager CSV/命名与读法/Node Values 告警；CCS 各向异性导热三步流程）；17.3 辐射前半（六模型总流程、Rosseland 仅压力基；非灰 P-1 带数；DTRM 光线/聚类/ray file 重建规则；S2S 全节——环境辐射、FPSC Manual/Automatic、分裂角 20°、Face/Cluster 基、Ray Tracing vs Hemicube 三假设、Blocking、参与区流程、CRF 格式、MPI/OpenMP、GPU Cromwell 与 MIS 聚类；DO 角度离散/像素化/非灰带 n·λ 换算/DO-Energy 耦合光学厚度 > 10；MC 目标历程 100,000 与网格粗化）。
- 新建知识页 [[Fluent 热能模拟]]（文件名笔误 Fulent 当即改回）。
- 提取边界：Eq 17.1–17.3 公式体未提取按语义记录；Figures 17.1–17.28 为图形元素。
- 下一续接位置：同章 17.3.7 Defining Material Properties for Radiation，从 p. 2277 开始。

### 批次 63：Part III / Ch.17 第 2 段——17.3.7–17.4（PDF pp. 2277–2340）

- 十批连续任务（批次 56–65）第 8 批，64 页：17.3.7 辐射材料属性（各模型所需系数、非灰逐带限制与 WSGGM）；17.3.8 辐射边界条件全节（进出口发射率与黑体温度及 cooler-outside 告诫、DO/MC 的 opaque/transparent/semi-transparent 全套参数——Diffuse Fraction/Beam Width/Beam Direction/Polar Distribution/边界源、半透明墙内部发射率告戒、Participates In Radiation）；17.3.9 求解策略（P-1 光学厚度 0.01–10、DTRM/S2S 迭代 5 次/判据 0.001、MC Poisson 统计与 30% 标准差阈值、求解频率定常 10/瞬态两基、暂停辐射更新两法）；17.3.10 后处理（变量清单、DTRM 热平衡与光线数、DTRM Graphics、S2S Information 与 .sif）；17.3.11 Solar Load 全节（Ray Tracing——两带光谱/阴影算法/quad-tree/内部散射、Solar Irradiation——beam 方向符号相反、Solar Calculator——ASHRAE/NREL 两法与负荷分配、BC 设置含多孔跳板估算法、仅 TUI 命令七项、动画三命令）；17.4 周期传热全节（约束、理论缩放、两段式顺序求解、体温度比监视、温度场不周期说明）；触及 17.5 节引言（p. 2340）。
- 扩充 [[Fluent 热能模拟]]。
- 提取边界：Eq 17.4–17.21 公式体未提取按语义记录；Figures 17.29–17.62 为图形元素；Beam Width 默认值等三个数值符号未提取已在证据节标注。
- 下一续接位置：同章 17.5 Modeling Heat Exchangers，从 p. 2341 开始。

### 批次 64：Part III / Ch.17 第 3 段（末段）——17.5–17.6（PDF pp. 2341–2392），Ch.17 全章完成

- 十批连续任务（批次 56–65）第 9 批，52 页：17.5 换热器模型全节（选型决策树与表 17.1 NTU vs 简效率能力矩阵；dual cell——重叠网格限制与守恒告诫、Fluid Zones/Heat Rejection/Performance Data（Raw vs NTU）/Frontal Area/Coupling 五页设置与多行程串联耦合；macro——NTU 与 simple effectiveness 特性与 13 条限制、ungrouped 六步（平面工具三节点精确贴合、宏整除要求、DEFINE_SOURCE 焓 UDF、Core Porosity Model 三法与样例文件）、grouped（Primary Flow Direction、Upstream 连接不可改须重建、补充辅助流、温度初始化传播）、后处理（重叠区选择告戒、Heat Exchanger Report 四报告、Volume Report 的 Heat Exchanger Source）、TUI）；17.6 PCB 热分析（SIWave DC IR 功率图、ECAD .aedb/edb.def 与 Board Configuration 两工作流、Multizone 网格要求、subst 材料三属性、By Count/By Size 分辨率、后处理与四条限制）。
- 扩充 [[Fluent 热能模拟]] 至全章完成。
- 提取边界：批次 64 段无编号公式（引 Theory Guide Eqs 6.x 仅作定位）；Figures 17.63–17.98 为图形元素。
- 下一续接位置：Part III / Ch.18 Modeling Hypersonic Flow，从 p. 2393 开始。

### 批次 65：Part III / Ch.18 Modeling Hypersonic Flow 全章（PDF pp. 2393–2426），十批收官

- 十批连续任务（批次 56–65）第 10 批（收官），34 页（p. 2426 为章尾空白页）：18.1 引言（Mach 5 分界、热化学非平衡现象、DBNS 定位）；18.2 HSN（adaptive 默认/expert 0–5 档 Mach、Roe-FDS/AUSM/CASM 兼容、Pressure Discontinuity Sensor、不可压不支持）；18.3 有限速率化学（Damkohler 数、空气离解温度、11 种预定义混合物清单与电离选择、求解器推荐）；18.4 Gupta 曲线拟合（≤30,000 K、仅四种 air 混合物、电子压修正）；18.5 双温度模型（需许可、13 步设置、Cp/输运方法、非平衡边界、Control Exponent、后处理 11 变量）；18.6–18.7 稀薄气体（Maxwell 滑移与 Knudsen 三区分类、Knudsen 计算器、温度跳变自动联动与限制）；18.8 部分催化壁（γ 语义、一般材料/TPS 三经验式）；18.9 壁面烧蚀（需许可、仅瞬态、Vielle/Surface Reaction 两模型、动网格自动设置与 RBF 告诫、先定常后瞬态）；18.10 最佳实践（按温度三档选物理、求解器设置七条、FMG 初始化参数与检查、监视量清单与后处理五查）。
- 新建知识页 [[Fluent 高超声速流动]]；记录图 18.25 标题误印瑕疵。
- 提取边界：Eq 18.1–18.13 公式体未提取按语义记录；Figures 18.1–18.25 为图形元素。
- 下一续接位置：Part III / Ch.19 Fluent's Virtual Blade Model，从 p. 2427 开始。**批次 56–65 十批任务全部完成。**

### 批次 54：Part III / Ch.14 第 1 段——14.1–14.6.2.1（PDF pp. 1861–1900）

- 十批连续任务（批次 46–55）第 9 批，40 页：14.1 引言（滑移 vs 动网格选择准则、同 zone 不兼容）、14.2 滑移示例、14.3 滑移网格技术、14.4 界面形状、14.5 使用滑移网格（要求约束含 periodic repeats 限制与匹配选项、设置七步含 mrf-to-sliding-mesh 与两 Important、求解策略含 MRF 初始化与预览、case/data 同存规则、时间周期解判定与时间步 20% 规则、后处理关节点值与时间平均）、14.6 动网格设置 13 步、14.6.1 模型参数选项、14.6.2.1 光顺方法族总则与七种（扩散[边界距离/单元体积扩散率、α 0–2 旋转 1.5、CG/GMRES/BCGSTAB]、弹簧[Spring Constant Factor 0–1]、线弹性固体[Poisson −1.0–0.5、可不指定变形几何]、RBF[旋转最佳、唯一支持保形周期/动墙固体、Local Smoothing]、参考位置[自动启用条件与 legacy case 告诫]、Laplacian[仅偏斜改进才移动]、边界层[Deform Adjacent Boundary Layer]）。
- 新建知识页 [[Fluent 滑移与动网格]]。提取边界：Eq 14.1–14.14 公式体未提取按周边文字记录（扩散方程/Hook 定律/Laplacian 等语义明确处除外；14.3/14.4 幂律扩散率具体形式未提取）；数值（5%、20%、α 0–2 与 1.5、CG 50→200–500、Poisson −1.0–0.5）为原文正文数值；Figures 14.1–14.29 为图形元素。
- 下一续接位置：同章 14.6.2.2 Dynamic Layering，从 p. 1901 开始。

### 批次 52–53：Part III / Ch.12 + Ch.13（PDF pp. 1851–1860），两章完成

- 十批连续任务（批次 46–55）第 7、8 批。两章均极短（4+6 页）且相邻，一次提取读完；登记与完成仍按两批分别记录。批次 52 = Ch.12 Managing Motion Definitions 全章（pp. 1851–1853；p. 1854 空白）；批次 53 = Ch.13 Managing Auxiliary Geometry Definitions 全章（pp. 1855–1860）。
- 新建知识页 [[Fluent 运动定义与辅助几何]]（两章合页）：运动定义（名称+参考帧+平移+旋转四元组；Rigid Body Motion 与 System Coupling Motion 两型；各字段支持常数/表达式/输入参数/命名表达式）；辅助几何（三用途：PUMA 自适应投影/变形动网格投影/滑移网格边界投影；四类型 Primitive[Cone/Plane/Sphere/Frustum/Cylinder——Frustum 与 Cylinder 只含曲面]/User-Defined[DEFINE_GEOMETRY]/Surface Mesh[STL 等]/Reconstruction[尖锐特征边需分区定义]；Display Options 分辨率控制）。
- 提取边界：无公式；Figures 12.1–12.2、13.1–13.5 为图形元素。
- 下一续接位置：Part III / Ch.14 Modeling Flows Using Sliding and Dynamic Meshes，从 p. 1861 开始。

### 批次 51：Part III / Ch.11 Moving Reference Frames（PDF pp. 1831–1849），Ch.11 全章完成

- 十批连续任务（批次 46–55）第 6 批，19 页（p. 1850 空白）：11.1 引言（SRF/MRF/SMM 三路线）、11.2 SRF（壁面与周期边界要求、网格坐标约束、设置六步、速度公式选择 Absolute/Relative 及切换告诫、求解策略含 transient-frame-motion-numerics、渐进升速、相对量后处理）、11.3 MRF（frozen rotor 近似与适用场景、七项限制含界面取向/DPM/轴对称旋流/时变速度禁止/mixture 公式互斥/耦合界面拆分/mrf-to-sliding-mesh 命令、网格保形与非保形两法、设置八步含初始化必须 Absolute、干涉振荡改滑移网格、周向平均后处理）。
- 新建知识页 [[Fluent 运动参考系]]。提取边界：Ch.11 无编号公式（Theory Guide 引用式 2.16 未提取）；坐标轴符号按约定补全；Figures 11.1–11.8 为图形元素。
- 下一续接位置：Part III / Ch.12 Managing Motion Definitions，从 p. 1851 开始。

### 批次 50：Part III / Ch.10 Modeling Basic Fluid Flow（PDF pp. 1799–1829），Ch.10 全章完成

- 十批连续任务（批次 46–55）第 5 批，31 页（p. 1830 空白）：10.1 UDS 输运方程（单相/多相理论、50 条上限从 0 编号、Flux/Unsteady Function、源项/扩散率/边界条件设置、收敛手段）、10.2 流向周期流动（不可压限制、单周期对质量流限制、压力基质量流/压力梯度与密度基压降、β 子迭代与松弛）、10.3 旋流与旋转流（五分类、旋流数与湍流模型选择 RSM、轴对称旋流设置与五步分步求解/渐进升速）、10.4 可压流动（Mach 分区、良定边界组合、浮动操作压力机制与限制、滞止初始化与 URF 策略）、10.5 无黏流动（滑移壁、初场用途）。
- 新建知识页 [[Fluent 基本流动建模]]。提取边界：Eq 10.1–10.22 公式体未提取按周边文字记录（Mach/声速/临界压比等明确处除外）；Figures 10.1–10.12 为图形元素。
- 下一续接位置：Part III / Ch.11 Moving Reference Frames，从 p. 1831 开始。

### 批次 49：Part III / Ch.9 第 3 段（末段）——9.11–9.17（PDF pp. 1735–1797），Ch.9 全章完成

- 十批连续任务（批次 46–55）第 4 批，63 页：9.10.4 热扩散系数输入收尾、9.11 标准态焓、9.12 标准态熵、9.13 未燃热扩散率、9.14 动能理论参数、9.15 操作压力（三种压力关系、Table 9.1 设置建议）、9.16 参考压力（连通/不连通分组、reference-pressure-method 2）、9.17 真实气体模型全节（选择指南、立方 EOS 四模型与限制、偏离函数、伪临界混合规则、Vapor/Liquid 状态选择与 spinodal、DPM 联用与 Table 9.2 液滴温度限、NIST REFPROP 152 流体与查找表/二元饱和表、UDRGM C 函数库与 RealGasFunctionList 顺序、RGP 表与饱和属性及连续性线性化）。**Ch.9 全章（pp. 1651–1797）完成**；p. 1798 空白。
- 扩充 [[Fluent 物理属性]]。提取边界：Eq 9.72–9.114 公式体未提取按周边文字记录（文字明确处除外）；Table 9.2/9.3 照录；UDRGM 代码清单照录；Figures 9.38–9.52 为图形元素。
- 下一续接位置：Part III / Ch.10 Modeling Basic Fluid Flow，从 p. 1799 开始。

### 批次 48：Part III / Ch.9 第 2 段——9.5–9.10（PDF pp. 1700–1734）

- 十批连续任务（批次 46–55）第 3 批，35 页：9.4.6.5.1 Herschel-Bulkley 输入（9.4 收尾）、9.5 导热系数（含固体各向异性六法及其压力基限制、后处理零值与分量变量）、9.6 UDS 扩散率（各向同性两法/各向异性四法、双求解器可用、后处理仅各向同性单元）、9.7 电导率（含固体各向异性三法）、9.8 热容（NASA-9、mixing-law、动能理论模式数）、9.9 辐射属性（按辐射模型的属性需求、WSGGM 三选项与颗粒/烟灰交互、相函数四选、折射率）、9.10 质量扩散系数（Fickian vs 完整多组分、七种 Mass Diffusivity 方法、湍流 Schmidt 默认 0.7、多孔各向异性组分扩散、热扩散系数三法）。
- 扩充 [[Fluent 物理属性]]。提取边界：Eq 9.45–9.71 公式体未提取按周边文字记录（Lambert 定律等文字明确处除外）；各向同性 UDS 默认扩散系数值未提取；Figures 9.22–9.37 为图形元素。
- 下一续接位置：同章 9.11 Standard State Enthalpies，从 p. 1735 开始（先补记热扩散系数输入延续步骤）。

### 批次 47：Part III / Ch.9 第 1 段——9.1–9.4（PDF pp. 1651–1699）

- 十批连续任务（批次 46–55）第 2 批，49 页：9.1 材料定义（六类材料、Fluent 库 675 种/GRANTA MDS 700+ 固体需单独许可/用户自定义 .scm 库、Create/Edit Materials 全操作、纯流体与 mixture species 独立对象告诫）、9.2 温度函数四型（多项式/分段线性 50 点上限与外推规则/分段多项式 3 区间/NASA-9 仅 Cp 8 区间；温度单位按 K/R 输入系数；解限值保证物理有效）、9.3 密度全选项（流态选型、多区混用限制、Boussinesq、compressible-liquid Tait 方程与密度比限值及 TUI 默认值、表观/不可压理想气体/理想气体/组分依赖五法与混合公式）、9.4 黏度全选项（Sutherland 两/三系数与空气系数值、幂律、动能理论、Gupta、组分混合律、四种非牛顿模型与 Arrhenius 温度因子及湍流不可用告诫）。
- 新建知识页 [[Fluent 物理属性]]。提取边界：Eq 9.1–9.44 公式体未提取、按周边文字与变量定义记录（Sutherland/幂律/Carreau/Cross/Herschel-Bulkley 标准形式按文字描述与空气系数值对应给出；Tait 与动能理论混合式仅记语义）；空气物性数值为原文正文数值；.scm 格式示例照录；Figures 9.1–9.21 为图形元素。
- 下一续接位置：同章 9.5 Thermal Conductivity，从 p. 1700 开始。

### 批次 44：Part III / Ch.8 第 6 段——8.4.16–8.4.22（PDF pp. 1535–1572），8.4 大节完成

- 五批连续任务（批次 41–45）第 4 批，38 页：8.4.15.15.6 流体侧换热系数（8.4.15 收尾）、8.4.16 多孔壁（Uniform/Discrete 两法、动态/静态注入、CHT 耦合、输入文件格式、后处理变量）、8.4.17 Symmetry、8.4.18 Periodic（无压降型）、8.4.19 Axis、8.4.20 Fan（压跃升、旋周速度、示例、后处理）、8.4.21 Radiator（压损/换热系数推导与示例）、8.4.22 Porous Jump。**8.4 大节 22 小节全部完成**。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：多孔壁全流程（注入/抽出侧守恒机制、动态按局部压力 vs 静态指定、CHT 的 Cho-Goldstein 关联与线性壁温假设、松弛因子、Injection Angles 局部柱坐标、Use Dynamic Cd UDF、输入文件关键字表）；symmetry 的零法向速度/零法向梯度语义与反例；periodic 默认 Translational、旋转角自动计算与网格周期性核查；axis 必须在 y=0；fan 的 Zone Average Direction/Reverse 选项、限速只限压跃升、profile 升序、Hub Radius 防除零、后处理关节点值；radiator 的 K 线性递减示例与 h 二阶拟合示例、绝对零度技巧；porous jump 的公式语义、耦合求解器收敛告诫、默认值代表无阻力模型。
- 提取边界：Eq 8.131–8.152 公式体未提取按周边文字记录（文字明确处除外）；fan Hub Radius 默认数值未提取；Tables 8.2–8.3 提取完整；Figures 8.60–8.81 为图形元素。
- 下一续接位置：同章 8.5 Editing Multiple Boundary Conditions at Once，从 p. 1573 开始。

### 批次 43：Part III / Ch.8 第 5 段——8.4.10–8.4.15（PDF pp. 1495–1534）

- 五批连续任务（批次 41–45）第 3 批，40 页：8.4.9 目标质量流策略收尾、8.4.10 压力远场（含 Flux-based 与切向修正）、8.4.11 Outflow（不可用情形、位置选择、质量流分流权重归一陷阱）、8.4.12 出口通风口、8.4.13 排气风扇、8.4.14 Degassing、8.4.15 Wall 边界条件全节（粗糙度与结冰模型、壁面运动、四种剪切条件、热条件七型与薄壁/双面墙/壳导热/System Coupling/Mapped Interface、二次梯度限制、边界对流、组分与表面反应、辐射/DPM/接触角/UDS/液膜/结构、默认值与剪切/换热计算程序）。
- 扩充 [[Fluent Cell Zone 与边界条件设置]]：far-field 的理想气体限制、20 倍弦长经验、Riemann 不变量机制、flux-based 与切向修正开关；outflow 的"计算过程中任一回流都影响收敛"告诫与权重归一；degassing 的质量汇机制与"必须开重力"；Wall 全节（粗糙壁不兼容模型清单、K_s/C_s 标定语义、结冰 y+≤1 限制、壁面运动法向分量被忽略与双面墙固体邻接限制、Marangoni 须能量方程、零剪切壁湍流处理开关、薄壁仅常数导热系数、Coupled 阻力参数自动赋予 shadow、解耦与壳导热互斥、二次梯度限制 0.7–0.9 可调、detect-boundary-advection 的 2° 判据、System Coupling 未接收数据时表现为绝热、mapped interface 禁壳导热、washcoat 因子、各热条件计算式语义）。
- 提取边界：Eq 8.108–8.130 公式体未提取按周边文字记录（文字明确处除外）；结冰关联式与换热公式仅定性记录；Figures 8.45–8.59 为图形元素。
- 下一续接位置：同章 8.4.16 Perforated Wall Boundary Conditions，从 p. 1535 开始。
