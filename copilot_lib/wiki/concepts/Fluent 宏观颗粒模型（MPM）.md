---
type: concept
created: 2026-10-19
updated: 2026-10-19
tags:
  - Ansys Fluent
  - mpm
  - macroscopic-particles
  - addon-module
  - solution-mode
sources:
  - "[[Ansys Fluent Users Guide 2026 R1]]"
---

# Fluent 宏观颗粒模型（MPM）

## 摘要

User's Guide 2026 R1 Part III / Chapter 26 "Modeling Macroscopic Particles"（PDF pp. 3005–3026，共 4 节）讲大颗粒宏观模型。**本页全章完成（批次 82，pp. 3005–3026）**：MPM 是基于 UDF 套件的 add-on 模块——模拟直径跨多个流体单元的大颗粒的输运、颗粒-颗粒/颗粒-壁相互作用；适用 Re << 1、密度比 ≈ 1；七页设置对话框（追踪/拖曳/碰撞/沉积/注入/场力/初始化）。

## 26.1 概览与限制（p. 3005）

- 传统 Lagrangian DPM 只适用于颗粒小到可视为单元内点质量、总体积可忽略的情形；**颗粒尺寸大于若干流体单元时必须计及其体积效应——MPM 预测大颗粒行为及其与流动、壁面、其他颗粒的相互作用**。
- add-on 模块（UDF 套件）；**设计目标：颗粒直径被 20–30 个流体单元解析**。**非通用模型**——验证良好的工况：**Re_p << 1 且流体/颗粒密度比 ρ_f/ρ_p ≈ 1**；其他取值下拖曳预测可能不准（拖曳不重要时仍可用）。
- **限制**：①不能模拟传质与辐射；②**不兼容运动/变形网格**；③不支持密堆积颗粒仿真（**每颗粒时间步只处理一次碰撞事件**）；④与 DPM 颗粒**无直接碰撞交互**；⑤可与多相模型耦合但**源项（质量/动量/热）需手动设置**；⑥不支持一个时间步内 MPM 颗粒轨迹子迭代；⑦**不兼容网格界面**。

## 26.2 加载 add-on 模块（p. 3006）

- 随标准安装提供（`addons/mpm` 目录）；**须先设置或读入有效 case 才能加载**；**仅 3D 可用**。两种加载方式：①Physics ribbon → Models 组 More → **Macroscopic Particle Model...**；②TUI `define/models/addon-module` → 输模块号 **10**（列表：0 none / 1 MHD / 2 Fiber / 3 Fuel Cell and Electrolysis / 4 SOFC with Unresolved Electrolyte / 5 Population Balance / 6 Adjoint Solver / 7 Single-Potential Battery / 8 Dual-Potential MSMD Battery / 9 PEM Fuel Cell / 10 Macroscopic Particle Model）。加载时自动装入 Scheme 库（GUI/TUI）与 UDF 库；Models 树出现 Macroscopic Particles（**默认已启用**）。

## 26.3 仿真设置流程（p. 3007）

11 步概要：Launcher 选 Solution 工作区 → 选 3D 网格 → 必要时缩放网格 → **除水泥固结（cemented）颗粒仿真外选 Transient** → 常规定义边界条件与物性 →（可选）先算收敛流场（宏观颗粒对流动影响强时提升稳定性）→ MPM 对话框设参 → 初始化 MPM 或流场 → 运行 → 存 case/data → 后处理。

## 26.4 宏观颗粒建模（pp. 3007–3025）

- 对话框七页：**Particle Tracking / Drag / Collision / Deposition / Injections / Attraction Forces / Initialize MPM**。**Note：默认参数未必适合——必须提供具体材料参数**。
- **26.4.1 Particle Tracking 页**：Particle Zones（可用 MPM 的 cell zone 列表）；**Enable Interaction with Continuous Phase**（双向耦合）；**Particle Sub-Timesteps within each Flow Timestep**；**Under-Relaxation Factor to Velocities in Touched Cells**（默认 1）；**Solve Heat Transfer**（启用后 Create/Modify Injection 需给 Initial Temperature 与 Specific Heat）。**Note：颗粒时间步应使宏观颗粒不跨超过一个 CFD 网格单元**。
- **26.4.2 Drag 页**：可 **Disable Drag Calculations**。四种拖曳公式：**Momentum Deficit Rate（MDR，默认）**——动量交换系数由拖曳函数与 MPM 时间步计算（公式体未提取）；**精度取决于组成宏观颗粒的单元数，更适合大颗粒**；**Morsi-Alexander（MA）**——按流体相 Re 计算的关联式（Re = ρ_f·u_rel·d_p/μ_f；公式体未提取），**适合较小颗粒**；**Constant Drag Coefficient (Cd)**——恒定拖曳系数（适合以指定速度/加速度运动的颗粒）；**Size Based MA/MDR**——按 **Critical Diameter** 自动在 MA（小于临界直径）与 MDR 之间切换——**单仿真含宽粒径范围时最佳**。可按 X/Y/Z 方向定义 drag factor（1 = 虚拟质量力在一个流动时间步内平衡颗粒所触单元的流体动量差）——**颗粒子时间步须约为动量弛豫时间 τ = ρ_p·d_p²/(18·μ_f) 的四分之一**（公式体未提取）；**拖曳精度依赖颗粒跨越的单元数——直径方向至少 20–30 个单元**。多相流的 **Multiphase: Drag Based On**：Primary Phase Velocity / Secondary Phase Velocity / Volume-Weighted Mixture Velocity。
- **26.4.3 Collision 页**：**Enable Particle-Particle Collision**——参数：Coefficient of Restitution (Normal/Tangential Dir)（Theory Guide Eqs 13.6/13.7）、**Substeps For Collision**（每追踪步内检测碰撞的子步数）、Coefficient of Friction（Eq 13.8）。**Enable Particle-Wall Collision**——选 Participating Zones For Collision 壁面；壁面恢复系数之外另有 **Coefficient of Friction (Sliding)** 与 **Coefficient of Friction (Rolling)**（滚动摩擦系数计入摩擦系数）。
- **26.4.4 Deposition 页**：**Enable Particle-Wall Deposition**——Zones for Deposition 选粘附壁面；参数：**Minimum Drag Force for Particle Detachment**（达到及以上的力使已沉积颗粒脱落）、**Max Normal/Tangential Velocity for Particle Deposition**（低于该法向/切向逼近速度才沉积）；**Write Particle Deposition File**（ASCII 沉积历史）；**Enable Particle-Particle Deposition**（颗粒间团聚——撞到已沉积颗粒即附着；沿用壁面沉积参数）。
- **26.4.5 Injections 页**：Create/Edit/Copy/Delete/Write All Injections.../Read...（控制与 DPM Injections 对话框类似；**Write All Injections 不支持稳态 + cemented 颗粒**；同名导入自动加 _d 后缀）。**Create/Modify Injection**：①命名（默认 injection-id）；②注入类型四种——**point**（单点）/ **plane**（平面上均匀或随机分布）/ **packing**（盒或圆柱内堆积）/ **from-file**（文本文件定义）；③**Cemented Particle(s)**（固定颗粒；**Important：稳态仿真全部颗粒必须 cemented**）；④物理参数 Diameter 与 Density（**Note：不能给颗粒指派 Fluent 材料**）；⑤类型专设（下）；⑥**Enable Continuous Injection**（Set... 打开 Define Continuous Injection：Injection start/stop/interval times——按间隔从 start 到 stop 持续注入；（可选）**Moving Injection**——注入点绕轴旋转（原点 XYZ + 轴向 X/Y/Z + Angular Velocity）与平移（Translational Velocity XYZ）——每步按上一步位置与平移速度确定新注入位置）；⑦Create/Modify。
  - **point 注入**：直径、密度、（换热仿真）材料比热与初温；释放位置（笛卡尔 XYZ 或**圆柱坐标 Radius/Angle/Axial**）；初速（笛卡尔 XYZ 或圆柱 Radial/Tangential/Axial）；初始角速度。**局部圆柱坐标系**：勾 Cylindrical Coordinates 并定义原点与轴方向。
  - **plane 注入**：初速与位置仅笛卡尔；注入面两种——**Rectangular**（距坐标面偏移 X/Y/Z Position + Extents of Rectangular Plane 范围）或 **Circular**（垂直于所选坐标方向；Center Location/Radius of Circular Plane）；释放分布两种——**Random**（Total # of Particles）或 **Uniform**（两轴向各自 # of Particles 矩形阵列）。
  - **packing 注入**：堆积区域——**Box**（Box Extents 最小/最大 XYZ）或 **Cylinder**（轴向、高度最小/最大坐标、原点、内外径）；分布 **Random** 或 **Uniform**。
  - **from-file 注入**：读文本文件定义注入。
- **26.4.6 Attraction Forces 页（场力/吸引力）**：**Enable Particle-Particle Forces** + 模型常数 **n1、n2、n3、G_p**（Theory Guide Eq 13.9）；**Enable Particle-Wall Forces** + Participating Zones + 常数 **n4、n5、G_w**（Eq 13.10）。
- **26.4.7 Initialize MPM 页**：施加 MPM 源项到连续相、初始化颗粒、显示轨迹；选项：**Field View 和/或 ASCII 格式保存颗粒数据**、控制台颗粒追踪警告打印。步骤：①**Initialize MPM Functions**——建立 MPM 相关源项并挂接全部 UDF；自动向求解器添加两条 execute 命令：**mpm1**（每迭代显示颗粒位置）与 **mpm3**（每迭代 PNG 输出颗粒位置）——可在 Execute Command 对话框禁用或改频率（Solution/Calculation Activities/Execute Commands）；可自定义 execute 命令监视其他量。**耦合仿真中点 Initialize MPM Functions 后压力离散格式自动切到 PRESTO!**（更稳健）。②**Initialize Particles** 初始化颗粒或按常规初始化流场（颗粒在下一时间步进入流动）。③运行。完成后 **Display Injections...** → Display Particles 对话框显示轨迹；着色变量：diameter / mass / particle ID / velocity magnitude（可设速度范围 Min/Max）。

## 证据与适用条件

- 页码：pp. 3005–3025 为正文；**p. 3026 为空白版权页**。目录范围 pp. 3005–3026 全部覆盖，**Ch.26 全章完成**。
- **公式**：MDR 动量交换系数式、MA 雷诺数式、动量弛豫时间式及 Theory Guide Eqs 13.6–13.10（恢复系数/摩擦/吸引力）公式体未提取，按周边文字记录结构、变量与语义。
- Figures 26.1–26.7（对话框截图）为图形元素未摄取。
- 数值（20–30 单元解析、子步约弛豫时间 1/4、模块号 10、MPM 仅 3D 与瞬态（除 cemented））为 2026 R1 手册记载，随版本可能变化。

## 关联页面

- [[Ansys Fluent Users Guide 2026 R1]]
- [[Part III - Solution Mode]]
- [[Fluent 离散相模型（DPM）]]（点质量 Lagrangian 对照；Ch.25）
- [[Fluent 多相流模型]]（Euler-Euler 对照与源项手动耦合；Ch.27）
- [[index]]
